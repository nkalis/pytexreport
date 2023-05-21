import os
from typing import Union

from pylatex import Command, Document, NoEscape
from pylatex.base_classes import Arguments, Options

from pytexreport import pytexreport


class ieeeConference(pytexreport.PyTexReport):
    def __init__(
        self,
        title: str,
        authors: dict,
        thanks: Union[str, None] = None,
        title_note: Union[str, None] = None,
    ):
        self.title = title
        self.authors = authors
        self.thanks = thanks
        self.title_note = title_note

        doc = Document()
        doc.documentclass = Command(
            "documentclass",
            options=Options("conference"),
            arguments=[NoEscape(r"IEEEtran")],
        )

        self.classFile = os.path.normpath(
            rf"{os.path.dirname( __file__ )}\ieeeConference.cls"
        )
        self.classFileName = "ieeeConference"

        # Preamble things
        if title_note is not None:
            doc.preamble.append(NoEscape(r"\IEEEoverridecommandlockouts"))
        doc.packages.append(Command("usepackage", arguments=Arguments("cite")))
        doc.packages.append(
            Command("usepackage", arguments=Arguments("amsmath,amssymb,amsfonts"))
        )
        doc.packages.append(Command("usepackage", arguments=Arguments("algorithmic")))
        doc.packages.append(Command("usepackage", arguments=Arguments("graphicx")))
        doc.packages.append(Command("usepackage", arguments=Arguments("textcomp")))
        doc.preamble.append(
            NoEscape(r"\def\BibTeX{{\rm B\kern-.05em{\sc i\kern-.025em b}\kern-.08em")
        )
        doc.preamble.append(
            NoEscape(r"    T\kern-.1667em\lower.7ex\hbox{E}\kern-.125emX}}")
        )

        # Make Title Page
        doc.append(NoEscape(r"\title{" + self.title))
        if self.title_note is not None:
            doc.append(
                NoEscape(
                    r"\\{\footnotesize \textsuperscript{*}" + self.title_note + r"}"
                )
            )
        if self.thanks is not None:
            doc.append(NoEscape(r"\thanks{" + self.thanks + r"}"))
        doc.append(NoEscape(r"}"))

        i = 1

        doc.append(NoEscape(r"\author{"))
        for author, attribute in self.authors.items():
            if i > 1:
                doc.append(NoEscape(r"\and"))
            doc.append(
                NoEscape(
                    r"\IEEEauthorblockN{"
                    + str(i)
                    + r"\textsuperscript{st}"
                    + attribute["fullname"]
                    + r"}"
                )
            )
            doc.append(
                NoEscape(
                    r"\IEEEauthorblockA{\textit{" + attribute["department"] + r"} \\"
                )
            )
            doc.append(NoEscape(r"\textit{" + attribute["affiliation"] + r"}\\"))
            doc.append(
                NoEscape(attribute["city"] + "," + attribute["country"] + r" \\")
            )
            doc.append(NoEscape(attribute["contact"] + r"}"))
            i += 1
        doc.append(NoEscape(r"}"))

        doc.append(NoEscape(r"\maketitle"))

        self.doc = doc
        super().__init__()

    def createAbstract(self, abstract: str):
        self.doc.append(NoEscape(r"\begin{abstract}"))
        self.doc.append(NoEscape(abstract))
        self.doc.append(NoEscape(r"\end{abstract}"))

    def createKeywords(self, keywords: list):
        self.doc.append(NoEscape(r"\begin{IEEEkeywords}"))
        self.doc.append(NoEscape(", ".join(keywords)))
        self.doc.append(NoEscape(r"\end{IEEEkeywords}"))
