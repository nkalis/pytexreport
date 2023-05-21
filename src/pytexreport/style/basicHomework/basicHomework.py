import os

from pylatex import Command, Document, NoEscape
from pylatex.base_classes import Arguments, Options

from pytexreport import pytexreport


class basicHomework(pytexreport.PyTexReport):
    def __init__(self, title: str, subtitle: str, author: str, author_id: str):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.author_id = author_id

        docclass = Command(
            "documentclass",
            options=Options(
                "PyTexReport",
            ),
            arguments=Arguments("basicHomework"),
        )

        doc = Document("documentclass", documentclass=docclass)

        self.classFile = os.path.normpath(
            rf"{os.path.dirname( __file__ )}\basicHomework.cls"
        )
        self.classFileName = "basicHomework"

        doc.packages.append(Command("usepackage", arguments=Arguments("lipsum")))
        doc.preamble.append(NoEscape(r"\newcommand*{\name}{" + self.author + r"}"))
        doc.preamble.append(NoEscape(r"\newcommand*{\id}{" + self.author_id + r"}"))
        doc.preamble.append(NoEscape(r"\newcommand*{\course}{" + self.title + "}"))
        doc.preamble.append(
            NoEscape(r"\newcommand*{\assignment}{" + self.subtitle + "}")
        )

        doc.append(NoEscape(r"\maketitle"))

        self.doc = doc
        super().__init__()
