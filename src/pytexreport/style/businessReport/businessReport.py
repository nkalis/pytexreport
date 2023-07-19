import os

from pylatex import Command, Document, NoEscape
from pylatex.base_classes import Options

from pytexreport import pytexreport


class businessReport(pytexreport.PyTexReport):
    def __init__(
        self,
        title: str,
        subtitle: str,
        authors: dict,
        logo: str,
    ):
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.logo = logo

        self.doc = Document()
        super().__init__()

        self.doc.documentclass = Command(
            "documentclass",
            options=Options("a4paper", "12pt"),
            arguments=[NoEscape(r"businessReport")],
        )

        self.classFile = os.path.normpath(
            rf"{os.path.dirname( __file__ )}\businessReport.cls"
        )
        self.classFileName = "businessReport"

        # Preamble things
        self.doc.preamble.append(
            NoEscape(r"\addbibresource{sample.bib} % BibLaTeX bibliography file")
        )
        self.doc.preamble.append(
            NoEscape(r"\usepackage{mathpazo} % Use Palatino for math")
        )

        self.doc.preamble.append(
            NoEscape(
                r"\usepackage[sfdefault]{plex-sans} % Use IBM Plex Sans as the sans font and make it the default"
            )
        )
        self.doc.preamble.append(
            NoEscape(r"\usepackage{plex-serif} % Use IBM Plex Serif as the serif font")
        )
        self.doc.preamble.append(
            NoEscape(r"\usepackage{plex-mono} % Use IBM Plex Mono as the mono font")
        )

        self.doc.preamble.append(
            NoEscape(
                r"\newcommand{\textel}[1]{{\fontseries{el}\selectfont #1}} % Define a simple command for using the ExtraLight weight"
            )
        )
        self.doc.preamble.append(
            NoEscape(
                r"\newcommand{\textl}[1]{{\fontseries{l}\selectfont #1}} % Define a simple command for using the Light weight"
            )
        )
        self.doc.preamble.append(
            NoEscape(
                r"\newcommand{\textsb}[1]{{\fontseries{sb}\selectfont #1}} % Define a simple command for using the SemiBold weight"
            )
        )

        # Set Up Title Page
        self.doc.preamble.append(NoEscape(r"\reporttitle{" + self.title + "}"))
        self.doc.preamble.append(NoEscape(r"\reportsubtitle{" + self.subtitle + "}"))
        self.doc.preamble.append(NoEscape(r"\reportauthors{Reeport created by:"))
        self.doc.preamble.append(
            NoEscape(r"\\\smallskip " + "".join([author for author in authors]) + r"}")
        )
        self.doc.preamble.append(NoEscape(r"\reportdate{\today}"))
        self.doc.preamble.append(
            NoEscape(
                r"\rightheadercontent{\includegraphics[width=3cm]{" + self.logo + r"}}"
            )
        )

        self.doc.append(NoEscape(r"\thispagestyle{empty} \\"))
        self.doc.append(NoEscape(r"\begin{fullwidth} % Use the whole page width"))
        self.doc.append(NoEscape(r"	\vspace*{-0.075\textheight} \\"))
        self.doc.append(
            NoEscape(r"	\hfill\includegraphics[width=5cm]{" + self.logo + r"} \\")
        )
        self.doc.append(NoEscape(r"	\vspace{0.15\textheight} \\"))
        self.doc.append(
            NoEscape(
                r"	\parbox{0.9\fulltextwidth}{\fontsize{50pt}{52pt}\selectfont\raggedright\textbf{\reporttitle}\par} \\"
            )
        )
        self.doc.append(NoEscape(r"	\vspace{0.03\textheight} \\"))
        self.doc.append(
            NoEscape(r"    {\LARGE\textit{\textbf{\reportsubtitle}}\par} \\")
        )
        self.doc.append(NoEscape(r"	\vfill \\"))
        self.doc.append(NoEscape(r"	{\Large\reportauthors\par} \\"))
        self.doc.append(NoEscape(r"	\vfill\vfill\vfill \\"))
        self.doc.append(NoEscape(r"	{\large\reportdate\par} \\"))
        self.doc.append(NoEscape(r"\end{fullwidth} \\"))
        self.doc.append(NoEscape(r"\newpage"))

        # Create Table of Contents
        self.doc.append(
            NoEscape(
                r"\begin{twothirdswidth} % Content in this environment to be at two-thirds of the whole page width"
            )
        )
        self.doc.append(
            NoEscape(
                r"    \tableofcontents % Output the table of contents, automatically generated from the section commands used in the document"
            )
        )
        self.doc.append(NoEscape(r"\end{twothirdswidth}"))

        self.doc.append(NoEscape(r"\newpage"))

    def addFullWidthText(self, text, color=None, new_paragraph=True):
        self.content.append(NoEscape(r"\begin{fullwidth}"))
        self.content.append(NoEscape(text))
        self.content.append(NoEscape(r"\end{fullwidth}"))
        if new_paragraph:
            self.createNewLine()

    def addSideNote(self, text, numbering=True, symbol="", location="0cm"):
        if numbering is True:
            self.content.append(
                NoEscape(r"\sidenote{[" + symbol + rf"][{location}]" + "}")
            )
        else:
            self.content.append(NoEscape(r"\sidenote{" + rf"[{location}]" + "}"))

    def addQuote(self, quote, quoted):
        self.content.append(NoEscape(r"\begin{quote}"))
        self.content.append(NoEscape(r"    \textbf{\LARGE ``}"))
        self.content.append(NoEscape(quote + r".\textbf{''}"))
        self.content.append(NoEscape(""))
        self.content.append(NoEscape(r"\hfill--- " + quoted))
        self.content.append(NoEscape(r"\end{quote}"))

    def addCode(self, code):
        self.content.append(NoEscape(r"\begin{lstlisting}"))
        self.content.append(NoEscape(code))
        self.content.append(NoEscape(r"\end{lstlisting}"))

    def addAppendix(self, text):
        if hasattr(self, "businessReportAppendix"):
            self.content.append(NoEscape(r"\section{Appendix Section}"))
            self.content.append(NoEscape(text))
        else:
            self.content.append(NoEscape(r"\newpage"))
            self.content.append(NoEscape(r"\section*{Appendices}"))
            self.content.append(NoEscape(r"\begin{appendices}"))
            self.content.append(NoEscape(r"\section{Appendix Section}"))
            self.content.append(NoEscape(text))
            self.businessReportAppendix = True
