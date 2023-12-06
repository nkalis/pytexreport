import os
from typing import Callable

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

        # Create the custom docclass and initialize the pytexreport base class
        doc = Document("basic")
        doc.documentclass = Command(
            "documentclass",
            options=Options("pytexreport"),
            arguments=[NoEscape(r"pytexreport")],
        )
        self.classFile = os.path.normpath(
            rf"{os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'class/pytexreport.cls'))}"
        )
        self.classFileName = "pytexreport"

        # Allow captioning of equations
        doc.preamble.append(NoEscape(r"\DeclareCaptionType{equ}[][]"))

        # Define geometry of pages
        doc.preamble.append(
            NoEscape(
                r"\usepackage[top = 0.8in, bottom = 1.5in, left = 0.8in, right = 0.8in]{geometry}"
            )
        )

        # define colors
        doc.add_color("color1", "HTML", "000060")
        doc.add_color("color2", "HTML", "333333")

        # Format the page style
        doc.preamble.append(NoEscape(r"\pagestyle{fancy}"))
        doc.preamble.append(NoEscape(r"\linespread{1.2}"))

        # format image/plot caption style
        doc.preamble.append(
            NoEscape(r"\DeclareCaptionFormat{upper}{#1#2\uppercase{#3}\par}")
        )
        doc.preamble.append(
            NoEscape(
                r"\captionsetup{labelfont={bf,color=color2},textfont={normalsize,color=color2},format = upper,figurename=FIGURE,tablename=TABLE}"
            )
        )

        # fancy sections
        doc.preamble.append(
            NoEscape(
                r"\titleformat{\section}{\color{color1}\Large\bfseries\uppercase}{\thesection}{1em}{}[\titlerule]"
            )
        )
        doc.preamble.append(
            NoEscape(
                r"\titleformat{\subsection}{\color{color1}\large\bfseries\uppercase}{\thesubsection}{1em}{}"
            )
        )
        doc.preamble.append(
            NoEscape(
                r"\titleformat{\subsubsection}{\color{color1}\bfseries\uppercase}{\thesubsubsection}{1em}{}"
            )
        )

        # format the headers and footers
        doc.preamble.append(NoEscape(r"\fancyhf{}"))
        doc.preamble.append(NoEscape(r"\renewcommand{\headrulewidth}{0pt}"))
        doc.preamble.append(
            NoEscape(r"\fancyhead[R]{\color{color2}{\large 10 December 2012}}")
        )
        doc.preamble.append(NoEscape(r"\setlength{\footskip}{60pt}"))
        doc.preamble.append(
            NoEscape(
                r"\fancyfoot[L]{\raisebox{-1\baselineskip}{\includegraphics[scale=0.2]{"
                + self.logo
                + r"}}}"
            )
        )
        doc.preamble.append(NoEscape(r"\fancyfoot[R]{\thepage}"))
        doc.preamble.append(NoEscape(r"\fancyfoot[C]{Template for business reports}"))
        doc.preamble.append(NoEscape(r"\setlength{\headheight}{15.2pt}"))
        doc.preamble.append(NoEscape(r""))

        # fancy boxes :)
        doc.preamble.append(NoEscape(r"\def\fullboxbegin{"))
        doc.preamble.append(NoEscape(r"    \bigskip"))
        doc.preamble.append(
            NoEscape(
                r"    \begin{tcolorbox}[colback=color1,colframe=color1,coltext=white,arc=0mm,boxrule=0pt]"
            )
        )
        doc.preamble.append(NoEscape(r"}"))
        doc.preamble.append(NoEscape(r"\def\fullboxend{\end{tcolorbox}\medskip}"))

        doc.preamble.append(NoEscape(r"\def\leftboxbegin{"))
        doc.preamble.append(NoEscape(r"    \setlength{\intextsep}{1pt}"))
        doc.preamble.append(NoEscape(r"    \begin{wrapfigure}{l}{0.5\textwidth}"))
        doc.preamble.append(
            NoEscape(
                r"    \begin{tcolorbox}[colback=color1,colframe=color1,coltext=white,arc=0mm,boxrule=0pt]"
            )
        )
        doc.preamble.append(NoEscape(r"}"))
        doc.preamble.append(NoEscape(r"\def\leftboxend{"))
        doc.preamble.append(NoEscape(r"\end{tcolorbox}"))
        doc.preamble.append(NoEscape(r"\end{wrapfigure}"))
        doc.preamble.append(NoEscape(r"}"))

        doc.preamble.append(NoEscape(r"\def\rightboxbegin{"))
        doc.preamble.append(NoEscape(r"    \setlength{\intextsep}{1pt}"))
        doc.preamble.append(NoEscape(r"    \begin{wrapfigure}{r}{0.5\textwidth}"))
        doc.preamble.append(
            NoEscape(
                r"    \begin{tcolorbox}[colback=color1,colframe=color1,coltext=white,arc=0mm,boxrule=0pt]"
            )
        )
        doc.preamble.append(NoEscape(r"}"))
        doc.preamble.append(NoEscape(r"\def\rightboxend{"))
        doc.preamble.append(NoEscape(r"\end{tcolorbox}"))
        doc.preamble.append(NoEscape(r"\end{wrapfigure}"))
        doc.preamble.append(NoEscape(r"}"))

        doc.preamble.append(NoEscape(r"\newcounter{frames}"))
        doc.preamble.append(NoEscape(r"\def\frameboxbegin#1{"))
        doc.preamble.append(NoEscape(r"    \bigskip"))
        doc.preamble.append(NoEscape(r"    \refstepcounter{frames}"))
        doc.preamble.append(
            NoEscape(
                r"    \begin{tcolorbox}[colback=white,colframe=color1,arc=0mm,title={\MakeUppercase{\textbf{Frame \arabic{frames}}: #1}}]"
            )
        )
        doc.preamble.append(NoEscape(r"}"))
        doc.preamble.append(NoEscape(r"\def\frameboxend{"))
        doc.preamble.append(NoEscape(r"    \end{tcolorbox}"))
        doc.preamble.append(NoEscape(r"}"))

        # title page
        doc.preamble.append(NoEscape(r"\title{Template for business reports}"))
        doc.preamble.append(
            NoEscape(r"\author{Karol Kozioł \newline / Company Name / Company Address}")
        )
        doc.preamble.append(NoEscape(r"\date{\today}"))

        doc.preamble.append(NoEscape(r"\newcommand\BackgroundPic{%"))
        doc.preamble.append(NoEscape(r"\put(0,0){%"))
        doc.preamble.append(NoEscape(r"\parbox[b][\paperheight]{\paperwidth}{%"))
        doc.preamble.append(NoEscape(r"\vfill"))
        doc.preamble.append(NoEscape(r"\centering"))
        doc.preamble.append(
            NoEscape(
                r"\includegraphics[width=\paperwidth,height=\paperheight,keepaspectratio]{cover.png}%"
            )
        )
        doc.preamble.append(NoEscape(r"\vfill"))
        doc.preamble.append(NoEscape(r"}}}"))
        doc.preamble.append(NoEscape(r"\makeatletter"))
        doc.preamble.append(NoEscape(r"\renewcommand{\maketitle}{"))
        doc.preamble.append(NoEscape(r"\thispagestyle{empty}"))
        doc.preamble.append(NoEscape(r"\AddToShipoutPicture*{\BackgroundPic}"))
        doc.preamble.append(NoEscape(r"\ClearShipoutPicture"))
        doc.preamble.append(NoEscape(r"\phantom{a}"))
        doc.preamble.append(NoEscape(r"\vfill"))
        doc.preamble.append(NoEscape(r"\phantom{a}\hfill"))
        doc.preamble.append(NoEscape(r"\begin{tabular}[c]{@{}p{0.7\textwidth}@{}}"))
        doc.preamble.append(NoEscape(r"      \color{white}\LARGE\@title\\[1em]"))
        doc.preamble.append(NoEscape(r"      \color{white}\Large\@author\\[2em]"))
        doc.preamble.append(NoEscape(r"\end{tabular}"))
        doc.preamble.append(NoEscape(r"\clearpage"))
        doc.preamble.append(NoEscape(r"\makeatother"))

        # Make title page
        doc.append(NoEscape(r"\maketitle"))
        doc.append(NoEscape(r"\tableofcontents"))
        doc.append(NoEscape(r"\clearpage"))

        # Inherit all the base class functionality
        self.doc = doc
        super().__init__()

    def addFullBox(self, func: Callable, *args, **kwargs):
        self.content.append(NoEscape(r"\fullboxbegin"))
        func(*args, **kwargs)
        self.content.append(NoEscape(r"\fullboxend"))
