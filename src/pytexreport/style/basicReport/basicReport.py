import os

from pylatex import Command, Document, NoEscape
from pylatex.base_classes import Arguments, Options

from pytexreport import pytexreport

from loguru import logger

class basicReport(pytexreport.PyTexReport):
    def __init__(
        self,
        title: str,
        subtitle: str,
        logo: str,
        department: str,
        organization: str,
        authors: list,
    ):
        # Create the custom docclass and initialize the pytexreport base class
        doc = Document('basic')
        doc.documentclass = Command(
            "documentclass",
            options=Options("pytexreport"),
            arguments=[NoEscape(r"pytexreport")],
        )
        self.classFile = os.path.normpath(
            rf"{os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'class/pytexreport.cls'))}"
        )
        self.classFileName = "pytexreport"

        # Set up the custom document title page parameters
        self.title = title
        self.subtitle = subtitle
        self.logo = logo
        self.department = department
        self.organization = organization
        self.authors = authors

        # Allow captioning of equations
        doc.preamble.append(NoEscape(r"\DeclareCaptionType{equ}[][]"))

        # Define geometry of pages
        doc.preamble.append(NoEscape(r"\usepackage[top = 0.8in, bottom = 0.8in, left = 0.6in, right = 0.6in]{geometry}"))

        # Format the section style
        doc.preamble.append(NoEscape(r"\titleformat{\section}{\normalfont\Large\bfseries}{\thesection}{1em}{}"))
        
        # Load Bibliography
        doc.preamble.append(NoEscape(r"\usepackage[style=numeric]{biblatex}"))
        doc.preamble.append(NoEscape(r"\addbibresource{References.bib}"))

        # Add title page
        doc.append(NoEscape(r"\thispagestyle{empty}"))
        doc.append(NoEscape(r"\begin{center}"))
        doc.append(NoEscape(r"\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}"))
        doc.append(NoEscape(r"\def\smallskip{\vspace{6pt}\\}"))
        doc.append(NoEscape(r"\def\medskip{\vspace{24pt}\\}"))
        doc.append(NoEscape(r"\def\bigskip{\vspace{48pt}\\}"))
        doc.append(NoEscape(r"\begin{figure} [h]"))
        doc.append(NoEscape(r"    \centering"))
        doc.append(NoEscape(r"    \includegraphics [scale=0.50]{" + self.logo + "} "))
        doc.append(NoEscape(r"\end{figure}"))
        doc.append(NoEscape(r"\textsc{\LARGE Delft University of Technology}"))
        doc.append(NoEscape(r"\medskip"))
        doc.append(NoEscape(r"\textsc{\Large System Engineering $\&$ Aerospace Design AE3211-I}"))
        doc.append(NoEscape(r"\smallskip"))
        doc.append(NoEscape(r"\HRule"))
        doc.append(NoEscape(r"\vspace{12pt} "))
        doc.append(NoEscape(r"{ \huge \bfseries Aircraft Tutorial - Group: 22 }"))
        doc.append(NoEscape(r"\smallskip"))
        doc.append(NoEscape(r"\HRule"))
        doc.append(NoEscape(r"\normalsize"))
        doc.append(NoEscape(r"\\ \textsc{In partial fulfillment of the bachelor curriculum of Aerospace Engineering} \bigskip"))
        doc.append(NoEscape(r"\begin{minipage}{0.4\textwidth}"))
        doc.append(NoEscape(r"\begin{flushleft} \large"))
        doc.append(NoEscape(r"\emph{Authors:}\\"))
        doc.append(NoEscape(r"    Emilie Bessette (4534921)\\"))
        doc.append(NoEscape(r"    Nicolas Kalis (4537130)\\"))
        doc.append(NoEscape(r"\end{flushleft}"))
        doc.append(NoEscape(r"\end{minipage}"))
        doc.append(NoEscape(r"\vspace{\fill}"))
        doc.append(NoEscape(r"\begin{center}"))
        doc.append(NoEscape(r"\begin{minipage}[b]{0.5\textwidth}"))
        doc.append(NoEscape(r"    \vspace{\fill}"))
        doc.append(NoEscape(r"    \begin{center}"))
        doc.append(NoEscape(r"        {\large 10 December 2012}"))
        doc.append(NoEscape(r"    \end{center} "))
        doc.append(NoEscape(r"\end{minipage}%"))
        doc.append(NoEscape(r"\end{center} "))
        doc.append(NoEscape(r"\end{center} "))
        doc.append(NoEscape(r"\newpage"))

        # Headers and footers
        doc.append(NoEscape(r"\pagestyle{fancy}"))
        doc.append(NoEscape(r"\fancyhead[R]{\slshape \rightmark}"))
        doc.append(NoEscape(r"\fancyhead[L]{ \textbf{AE3211-I -- Aircraft Tutorial}}"))
        doc.append(NoEscape(r"\fancyfoot[R]{ \fbox{\textbf{DRAFT}}}"))
        doc.append(NoEscape(r"\setlength{\headheight}{14pt}"))

        # Table of contents
        doc.append(NoEscape(r"\section*{Table of Contents}"))
        doc.append(NoEscape(r"\pagenumbering{gobble}"))
        doc.append(NoEscape(r"\makeatletter"))
        doc.append(NoEscape(r"\@starttoc{toc}"))
        doc.append(NoEscape(r"\makeatother"))
        doc.append(NoEscape(r"\newpage"))

        # Roman or Arabic numbering
        doc.append(NoEscape(r"\pagenumbering{roman}"))
        doc.append(NoEscape(r"\pagenumbering{arabic}"))

        # Inherit all the base class functionality
        self.doc = doc
        super().__init__()

