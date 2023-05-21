from datetime import date

from pylatex import Command, Document, Figure, MiniPage, NoEscape
from pylatex.base_classes import Arguments, Options

from pytexreport import pytexreport


class basicReport(pytexreport.PyTexReport):
    def __init__(
        self,
        title: str,
        subtitle: str,
        department: str,
        organization: str,
        authors: list,
    ):
        self.title = title
        self.subtitle = subtitle
        self.department = department
        self.organization = organization
        self.authors = authors

        docclass = Command(
            "documentclass",
            options=Options(
                "10pt",
                "a4paper",
            ),
            arguments=Arguments("article"),
        )

        geometry_options = {"margin": "0.7in"}

        # Start LaTex Doc
        doc = Document(documentclass=docclass, geometry_options=geometry_options)

        # Load Packages
        doc.packages.append(
            Command(
                "usepackage",
                arguments=Arguments("xcolor"),
                options=Options("table", "xcdraw", "dvipsnames"),
            )
        )
        doc.packages.append(Command("usepackage", arguments=Arguments("hyperref")))
        doc.packages.append(Command("usepackage", arguments=Arguments("amsfonts")))
        doc.packages.append(
            Command(
                "usepackage", arguments=Arguments("caption"), options=("labelfont=bf")
            )
        )
        doc.packages.append(Command("usepackage", arguments=Arguments("graphicx")))
        doc.packages.append(Command("usepackage", arguments=Arguments("fancyhdr")))
        doc.packages.append(Command("usepackage", arguments=Arguments("lastpage")))
        doc.packages.append(
            Command(
                "usepackage",
                arguments=Arguments("biblatex"),
                options=Options("style=apa"),
            )
        )
        doc.packages.append(Command("usepackage", arguments=Arguments("tocbibind")))
        doc.packages.append(Command("usepackage", arguments=Arguments("csquotes")))
        doc.packages.append(Command("usepackage", arguments=Arguments("comment")))
        doc.packages.append(Command("usepackage", arguments=Arguments("array")))
        doc.packages.append(
            Command(
                "usepackage",
                arguments=Arguments("adjustbox"),
                options=Options("export"),
            )
        )
        doc.packages.append(
            Command(
                "usepackage",
                arguments=Arguments("appendix"),
                options=Options("toc", "page"),
            )
        )
        doc.packages.append(
            Command(
                "usepackage", arguments=Arguments("tocloft"), options=Options("titles")
            )
        )
        doc.packages.append(Command("usepackage", arguments=Arguments("subfig")))
        doc.packages.append(Command("usepackage", arguments=Arguments("chngcntr")))
        doc.packages.append(Command("usepackage", arguments=Arguments("amsmath")))
        doc.packages.append(Command("usepackage", arguments=Arguments("tabularx")))
        doc.packages.append(Command("usepackage", arguments=Arguments("multirow")))
        doc.packages.append(Command("usepackage", arguments=Arguments("pdfpages")))
        doc.packages.append(Command("usepackage", arguments=Arguments("rotating")))
        doc.packages.append(Command("usepackage", arguments=Arguments("tikz")))
        doc.packages.append(Command("usepackage", arguments=Arguments("longtable")))
        doc.packages.append(Command("usepackage", arguments=Arguments("rotating")))
        doc.packages.append(
            Command("numberwithin", arguments=Arguments("equation", "section"))
        )

        # Some Preamble
        doc.append(NoEscape(r"\pagestyle{fancy}"))
        doc.preamble.append(
            NoEscape(r"\newcolumntype{P}[1]{>{\centering\arraybackslash}p{#1}}")
        )

        doc.packages.append(NoEscape(r"\usepackage{titlesec}"))
        doc.preamble.append(NoEscape(r"\titleformat{\section}"))
        doc.preamble.append(
            NoEscape(r"{\normalfont\Large\bfseries}{\thesection}{1em}{}")
        )

        doc.preamble.append(NoEscape(r"\setlength\parindent{0pt}"))
        doc.preamble.append(
            NoEscape(r"\setitemize{noitemsep,topsep=0pt,parsep=0pt,partopsep=5pt}")
        )

        doc.preamble.append(NoEscape(r"\addbibresource{sample.bib}"))

        # Counting figures and tables from section number
        doc.preamble.append(NoEscape(r"\counterwithin{figure}{section}"))
        doc.preamble.append(NoEscape(r"\counterwithin{table}{section}"))

        # Create Title Page
        doc.append(Command("begin", arguments=Arguments("titlepage")))
        doc.append(NoEscape(r"\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}"))
        doc.append(NoEscape(r"\center"))
        with doc.create(Figure(position="H")) as logo_icon:
            logo_icon.add_image(
                "logo.png", width="120px", placement=NoEscape(r"\centering")
            )

        doc.append(NoEscape(r"\textsc{\Large " + self.organization + r" }\\[1.5cm]"))
        doc.append(NoEscape(r"\textsc{\Large " + self.department + r" }\\[0.5cm]"))
        doc.append(NoEscape(r"\HRule \\[0.4cm]"))
        doc.append(NoEscape(r"{ \huge \bfseries " + self.title + r" }\\[0.4cm]"))
        doc.append(NoEscape(r"\HRule \\"))
        doc.append(NoEscape(r"\normalsize \textsc{" + self.subtitle + r"} \\[3cm]"))
        # doc.append(Section('Introduction', numbering=None, label='00'))

        with doc.create(MiniPage(width=r"0.4\textwidth")):
            doc.append(NoEscape(r"\begin{flushleft} \large"))

            doc.append(Command("emph", arguments=Arguments("Author(s):")))
            for author in authors:
                doc.append("\n")
                doc.append(str(author))
            doc.append(NoEscape(r"\end{flushleft}"))

        doc.append(NoEscape(r"\mbox{}"))
        doc.append(NoEscape(r"\vfill"))
        doc.append(NoEscape(rf"\large {date.today()}"))
        doc.append(Command("end", arguments=Arguments("titlepage")))

        # Fancy footers for other pages
        doc.append(NoEscape(r"\fancyhf{}"))
        doc.append(NoEscape(r"\fancyhead[R]{Page \thepage}"))
        doc.append(NoEscape(r"\fancyhead[L]{\slshape \rightmark}"))
        doc.append(NoEscape(r"\fancyfoot[R]{ \textbf{" + self.title + r"}}"))
        if len(authors) == 1:
            doc.append(NoEscape(r"\fancyfoot[L]{" + self.authors[0] + r"}"))
        else:
            doc.append(NoEscape(r"\fancyfoot[L]{" + self.department + r"}"))

        self.doc = doc
        super().__init__()
