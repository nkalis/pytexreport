import os

from pylatex import Command, Document, NoEscape
from pylatex.base_classes import Arguments, Options

from pytexreport import pytexreport


class basicHomework(pytexreport.PyTexReport):
    def __init__(self, title: str, subtitle: str, author: str, author_id: str):
        # Create the custom docclass and initialize the pytexreport base class
        docclass = Command(
            "documentclass",
            options=Options(
                "PyTexReport",
            ),
            arguments=Arguments("basicHomework"),
        )
        self.doc = Document("documentclass", documentclass=docclass)
        self.classFile = os.path.normpath(
            rf"{os.path.dirname( __file__ )}\basicHomework.cls"
        )
        self.classFileName = "basicHomework"
        
        super().__init__()

        # Set up the custom document title page parameters
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.author_id = author_id

        self.doc.packages.append(Command("usepackage", arguments=Arguments("lipsum")))
        self.doc.preamble.append(NoEscape(r"\newcommand*{\name}{" + self.author + r"}"))
        self.doc.preamble.append(NoEscape(r"\newcommand*{\id}{" + self.author_id + r"}"))
        self.doc.preamble.append(NoEscape(r"\newcommand*{\course}{" + self.title + "}"))
        self.doc.preamble.append(
            NoEscape(r"\newcommand*{\assignment}{" + self.subtitle + "}")
        )

        self.doc.append(NoEscape(r"\maketitle"))