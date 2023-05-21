"""
This example shows the functionality of the PyLaTeX library.

It creates a sample report with 2 tables, one containing images and the other
containing data. It also creates a complex header with an image.

..  :copyright: (c) 2016 by Vladimir Gorovikov
    :license: MIT, see License for more details.
"""

# begin-doc-include
import os
import re
import shutil
import types
from collections import deque

import latexify
import matplotlib
from loguru import logger
from pylatex import (
    Command,
    Figure,
    Label,
    LineBreak,
    Matrix,
    NewPage,
    NoEscape,
    Section,
    Subsection,
    Subsubsection,
    Table,
)
from pylatex.base_classes import Arguments, Options
from pylatex.lists import Description, Enumerate, Itemize
from pylatex.table import Tabular
from pylatex.utils import escape_latex

# Set the font to Computer Modern
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.serif"] = ["Computer Modern"]


class PyTexReport:
    presentSection = deque()
    content = []

    def __init__(self):
        # Adding Package to allow notes
        self.doc.packages.append(
            Command(
                "usepackage",
                arguments=Arguments("xcolor"),
                options=Options("table", "xcdraw", "dvipsnames"),
            )
        )
        # Captioning Equations
        self.doc.packages.append(Command("usepackage", arguments=Arguments("float")))
        self.doc.preamble.append(NoEscape(r"\usepackage{aliascnt}"))
        self.doc.preamble.append(NoEscape(r"\newaliascnt{eqfloat}{equation}"))
        self.doc.preamble.append(NoEscape(r"\newfloat{eqfloat}{h}{eqflts}"))
        self.doc.preamble.append(NoEscape(r"\floatname{eqfloat}{Equation}"))

        self.doc.preamble.append(NoEscape(r"\newcommand*{\ORGeqfloat}{}"))
        self.doc.preamble.append(NoEscape(r"\let\ORGeqfloat\eqfloat"))
        self.doc.preamble.append(NoEscape(r"\def\eqfloat{%"))
        self.doc.preamble.append(NoEscape(r"\let\ORIGINALcaption\caption"))
        self.doc.preamble.append(NoEscape(r"\def\caption{%"))
        self.doc.preamble.append(NoEscape(r"\addtocounter{equation}{-1}%"))
        self.doc.preamble.append(NoEscape(r"\ORIGINALcaption"))
        self.doc.preamble.append(NoEscape(r"}%"))
        self.doc.preamble.append(NoEscape(r"\ORGeqfloat"))
        self.doc.preamble.append(NoEscape(r"}"))

        # Enum Items
        self.doc.packages.append(
            Command("usepackage", arguments=Arguments("enumitem")),
        )

    def flush(self, level=0):
        logger.info(self.presentSection)
        logger.info(self.content)

        if len(self.content) < 1:
            return
        if len(self.presentSection) < 1:
            if len(self.content) > 0:
                for item in self.content:
                    self.doc.append(item)
        else:
            last = self.presentSection.pop()
            if len(self.content) > 0:
                for item in self.content:
                    last.append(item)
                self.content = []

            if len(self.presentSection) > level:
                for item in range(level, len(self.presentSection)):
                    current = self.presentSection.pop()
                    current.append(last)
                    last = current

            if level == 0:
                self.doc.append(last)
            else:
                self.presentSection[level - 1].append(last)

        logger.info(self.content)

    def createNewPage(self):
        self.content.append(NewPage())

    def createNewLine(self):
        self.content.append("")

    def addLineBreak(self):
        self.content.append(LineBreak())

    def addVSpace(self, size="medium"):
        if size == "small":
            self.content.append(NoEscape(r"\smallskip"))
        if size == "medium":
            self.content.append(NoEscape(r"\medskip"))
        if size == "large":
            self.content.append(NoEscape(r"\largelskip"))

    def createSection(self, title, numbering=None):
        self.flush(0)
        self.section = Section(title, numbering=numbering)
        self.presentSection.append(self.section)

    def createSubSection(self, title, numbering=None):
        self.flush(1)
        self.subsection = Subsection(title, numbering=numbering)
        self.presentSection.append(self.subsection)

    def createSubSubSection(self, title, numbering=None):
        self.flush(2)
        self.subsubsection = Subsubsection(title, numbering=numbering)
        self.presentSection.append(self.subsubsection)

    def addText(self, text, color=None, new_paragraph=True):
        if text[0] == "#":
            text = text[1:]
            if text[0] == "!":
                text = NoEscape(r"\textcolor{Bittersweet}{" + rf"{text}" + r"}")
            if text[0] == "*":
                text = NoEscape(r"\textcolor{LimeGreen}{" + rf"{text}" + r"}")
            if text[0] == "?":
                text = NoEscape(r"\textcolor{Cyan}{" + rf"{text}" + r"}")
            if text[0:4] == "TODO":
                text = NoEscape(r"\textcolor{YellowOrange}{" + rf"{text}" + r"}")

        if color is not None:
            text = NoEscape(r"\textcolor{" + color + "}{" + text + "}")

        self.content.append(NoEscape(text))

        if new_paragraph:
            self.createNewLine()

    def addList(self, lists, type=1):
        if type < 3:
            if type == 1:
                items = Itemize(options=Options("noitemsep"))
            if type == 2:
                self.content.append(NoEscape(r"\setlist{nolistsep}"))
                items = Enumerate(options=Options("noitemsep"))
            for item in lists:
                items.add_item(item)
        elif type == 3:
            items = Description(options=Options("noitemsep"))
            for item in lists:
                items.add_item(item[0], item[1])

        self.content.append(items)

    def addTable(self, caption=None, label=None, data=None, nrow=None, ncol=None):
        table = Table(position="H")

        tabsize = "|" + "|".join(["c"] * ncol) + "|"
        mtable = Tabular(tabsize)
        for i in range(nrow):
            mtable.add_hline()
            if i == 0:
                mtable.add_row(
                    tuple(
                        [
                            escape_latex(NoEscape(r"\textbf{" + item + r"}"))
                            for item in data[i]
                        ]
                    )
                )
            else:
                mtable.add_row(tuple([escape_latex(str(item)) for item in data[i]]))
        mtable.add_hline()

        if caption is not None:
            table.add_caption(caption)
        table.append(NoEscape(r"\centering"))
        table.append(mtable)

        if label is not None:
            table.append(Label(f"tab: {label}"))

        self.content.append(table)

    def addFigure(self, file=None, caption=None, label=None, width=None):
        fig = Figure(position="H")
        if width is not None:
            fig.add_image(file, width=width)
        else:
            fig.add_image(file)
        if caption is not None:
            fig.add_caption(caption)
        if label is not None:
            fig.append(Label(f"fig: {label}"))
        self.content.append(fig)

    def addMatplot(
        self, plt, caption=None, label=None, dpi=300, extension="pdf", width=None
    ):
        fig = Figure(position="H")
        if width is not None:
            fig.add_plot(width=NoEscape(width), dpi=dpi, extension=extension)
        else:
            fig.add_plot(dpi=dpi, extension=extension)
        if caption is not None:
            fig.add_caption(caption)
        if label is not None:
            fig.append(Label(f"fig: {label}"))
        self.content.append(fig)
        plt.clf()

    def addEquation(
        self,
        equation,
        caption=None,
        label=None,
        inline=False,
    ):
        if type(equation) is types.FunctionType:
            equation = latexify.get_latex(equation)

        if not inline:
            self.content.append(NoEscape(r"\begin{eqfloat}[H]"))
            self.content.append(NoEscape(r"\begin{equation}"))
            self.content.append(NoEscape(equation))
            self.content.append(NoEscape(r"\end{equation}"))
            if caption is not None:
                self.content.append(NoEscape(r"\caption{" + caption + r"}"))
            if label is not None:
                self.content.append(NoEscape(r"\label{eq:" + label + r"}"))

            self.content.append(NoEscape(r"\end{eqfloat}"))

        else:
            self.content.append(NoEscape(rf"${equation}$"))

    def addMatrix(self, matrix_equation, matrix_data, matrix_type="b"):
        # p = ( ), b = [ ], B = { }, v = | |, V = || ||
        matrix = Matrix(matrix_data, mtype=matrix_type)
        self.content.append(NoEscape(r"\["))
        self.content.append(NoEscape(rf"{matrix_equation} =" + rf"{matrix.dumps()}"))
        self.content.append(NoEscape(r"\]"))

    def output(self):
        filename = re.sub(r"[^\w\s]", "", self.title.lower())
        filename = " ".join(filename.split())
        self.filename = filename.replace(" ", "_")

        if hasattr(self, "classFile"):
            inputpath = os.path.join(
                self.doc._select_filepath(filepath=None), self.classFile
            )
            outputpath = self.classFileName + ".cls"
            shutil.copyfile(inputpath, outputpath)

        self.doc.generate_pdf(self.filename, clean_tex=False)

    def _flush(self):
        if len(self.presentSection) > 2:
            for item in self.content:
                self.presentSection["subsubsection"].append(item)
            self.presentSection["subsection"].append(
                self.presentSection["subsubsection"]
            )
            self.presentSection["section"].append(self.presentSection["subsection"])
            self.doc.append(self.presentSection["section"])
        elif len(self.presentSection) > 1:
            for item in self.content:
                self.presentSection["subsection"].append(item)
            self.presentSection["section"].append(self.presentSection["subsection"])
            self.doc.append(self.presentSection["section"])
        elif len(self.presentSection) > 0:
            for item in self.content:
                self.presentSection["section"].append(item)
            self.doc.append(self.presentSection["section"])
        else:
            for item in self.content:
                self.doc.append(item)

        self.content = []
