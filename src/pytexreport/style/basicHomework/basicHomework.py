import os

from pylatex import Command, Document, NoEscape
from pylatex.base_classes import Arguments, Options

from pytexreport import pytexreport


class basicHomework(pytexreport.PyTexReport):
    def __init__(
        self, title: str, subtitle: str, author: str, author_id: str, logo: str
    ):
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

        # Set up the custom document title page parameters
        self.title = title
        self.subtitle = subtitle
        self.logo = logo
        self.author = author
        self.author_id = author_id

        # Allow captioning of equations
        doc.preamble.append(NoEscape(r"\DeclareCaptionType{equ}[][]"))

        # Define geometry of pages
        doc.preamble.append(
            NoEscape(
                r"\usepackage[top = 1in, bottom = 1in, left = 0.8in, right = 0.8in]{geometry}"
            )
        )

        # Add packages unique to class
        doc.packages.append(Command("usepackage", arguments=Arguments("listings")))

        # Customize lists using the listings package
        doc.preamble.append(NoEscape(r"\usepackage{titlesec}"))
        doc.preamble.append(NoEscape(r"\lstdefinestyle{mystyle}{"))
        doc.preamble.append(NoEscape(r" backgroundcolor=\color{backcolour},"))
        doc.preamble.append(NoEscape(r" commentstyle=\color{codegreen},"))
        doc.preamble.append(NoEscape(r" keywordstyle=\color{magenta},"))
        doc.preamble.append(NoEscape(r" numberstyle=\tiny\color{codegray},"))
        doc.preamble.append(NoEscape(r" stringstyle=\color{codepurple},"))
        doc.preamble.append(NoEscape(r" basicstyle=\footnotesize,"))
        doc.preamble.append(NoEscape(r" breakatwhitespace=false,"))
        doc.preamble.append(NoEscape(r" breaklines=true,"))
        doc.preamble.append(NoEscape(r" captionpos=b,"))
        doc.preamble.append(NoEscape(r" keepspaces=true,"))
        doc.preamble.append(NoEscape(r" numbers=left,"))
        doc.preamble.append(NoEscape(r" numbersep=5pt,"))
        doc.preamble.append(NoEscape(r" showspaces=false,"))
        doc.preamble.append(NoEscape(r" showstringspaces=false,"))
        doc.preamble.append(NoEscape(r" showtabs=false,"))
        doc.preamble.append(NoEscape(r" tabsize=2"))
        doc.preamble.append(NoEscape(r"}"))
        doc.preamble.append(Command("lstset", arguments=Arguments("style=mystyle")))

        # Create the title page
        doc.preamble.append(NoEscape(r"\renewcommand\maketitle{"))
        doc.preamble.append(NoEscape(r" \begin{flushleft}"))
        doc.preamble.append(NoEscape(r"     Student Name: {" + self.author + "}"))
        doc.preamble.append(NoEscape(r"     \par Student ID: {" + self.author_id + "}"))
        doc.preamble.append(NoEscape(r" \end{flushleft}"))
        doc.preamble.append(NoEscape(r" \begin{center}"))
        doc.preamble.append(
            NoEscape(r"     \par \textbf{\large {" + self.title + "} }")
        )
        doc.preamble.append(NoEscape(r"     \par {" + self.subtitle + "}"))
        doc.preamble.append(NoEscape(r" \end{center}"))
        doc.preamble.append(NoEscape(r" \rule{\linewidth}{0.1mm}"))
        doc.preamble.append(NoEscape(r" \bigskip"))
        doc.preamble.append(NoEscape(r" \bigskip"))
        doc.preamble.append(NoEscape(r"}"))

        # Set up footers/headers
        doc.preamble.append(NoEscape(r"\pagestyle{fancy}"))
        doc.preamble.append(NoEscape(r"\fancyhead[R]{Assignment 1}"))
        doc.preamble.append(NoEscape(r"\fancyhead[L]{Amin Bashiri}"))
        doc.preamble.append(NoEscape(r"\fancyfoot[R]{ \fbox{\textbf{DRAFT}}}"))
        doc.preamble.append(NoEscape(r"\setlength{\headheight}{15pt}"))

        # Add right after '\begin{document}'
        doc.append(NoEscape(r"\thispagestyle{empty}"))
        doc.append(NoEscape(r"\AddToShipoutPicture*"))
        doc.append(
            NoEscape(
                r"  {\put(490,750){\includegraphics[height=3cm]{" + self.logo + "}}}"
            )
        )
        doc.append(NoEscape(r"\maketitle"))

        # Inherit all the base class functionality
        self.doc = doc
        super().__init__()
