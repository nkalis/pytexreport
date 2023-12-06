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
    NewLine,
    NewPage,
    NoEscape,
    Section,
    Subsection,
    Subsubsection,
    Table,
)
from pandas import DataFrame
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
        """
        Initializes a new instance of the class.
        """

        # Default colours
        self.doc.add_color('TODOblue', 'HTML', '0099ff')
        self.doc.add_color('TODOgreen', 'HTML', '00cc00')
        self.doc.add_color('TODOorange', 'HTML', 'ffcc00')
        self.doc.add_color('TODOred', 'HTML', 'ff0000')

        pass

    def flush(self, level=0):
        """
        Flushes the content of the object based on the given level.
        Args:
            level (int, optional): The level at which to flush the content. Defaults to 0.
        Returns:
            None
        """

        print(self.content)

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

    def createNewPage(self):
        """
        Creates a new page.
        This function appends a new page to the `content` list.
        
        Parameters:
            self (ClassName): The instance of the class.
        
        Returns:
            None
        """
        self.content.append(NewPage())

    def createNewLine(self):
        self.content.append(r"\par")

    def addLineBreak(self):
        self.content.append(LineBreak())

    def addVSpace(self, size="medium"):
        if size == "small":
            self.content.append(NoEscape(r"\smallskip "))
        if size == "medium":
            self.content.append(NoEscape(r"\medskip "))
        if size == "large":
            self.content.append(NoEscape(r"\largelskip "))

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

    def addText(self, text, color=None, new_paragraph=False):
        if text[0] == "#":
            text = text[1:]
            if text[0] == "!":
                text = NoEscape(r"{\color{TODOred}{" + rf"{text}" + r"}}")
            if text[0] == "*":
                text = NoEscape(r"{\color{TODOgreen}{" + rf"{text}" + r"}}")
            if text[0] == "?":
                text = NoEscape(r"{\color{TODOblue}{" + rf"{text}" + r"}}")
            if text[0:4] == "TODO":
                text = NoEscape(r"{\color{TODOorange}{" + rf"{text}" + r"}}")
            
        if new_paragraph:
            text = r"\medskip \par " + text

        if color is not None:
            text = NoEscape(r"\textcolor{" + color + "}{" + text + "}")

        self.content.append(NoEscape(f"{text} "))

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
    
    def addDataFrame(self, dataframe=DataFrame, caption=None, label=None):
        data = dataframe.to_numpy().tolist()
        data.insert(0, list(dataframe.columns))
        tdata = {
            "data": data,
            "nrow": dataframe.shape[0] + 1,  # Add 1 for the header row
            "ncol": dataframe.shape[1]
        }
        print(tdata)
        self.addTable(caption=caption, label=label, data=tdata["data"], nrow=tdata["nrow"], ncol=tdata["ncol"])

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

    def addFigure(
        self, file=None, caption=None, label=None, width=NoEscape(r"0.8\textwidth")
    ):
        fig = Figure(position="H")
        fig.add_image(file, width=width)
        if caption is not None:
            fig.add_caption(caption)
        if label is not None:
            fig.append(Label(f"fig: {label}"))
        self.content.append(fig)

    def addMatplot(
        self,
        plt,
        caption=None,
        label=None,
        dpi=300,
        extension="pdf",
        width=NoEscape(r"0.8\textwidth"),
    ):
        fig = Figure(position="H")
        fig.add_plot(width=NoEscape(width), dpi=dpi, extension=extension)
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
            self.content.append(NoEscape(r"\begin{equ}[!ht]"))
            self.content.append(NoEscape(r"\begin{equation}"))
            self.content.append(NoEscape(equation))
            self.content.append(NoEscape(r"\end{equation}"))
            if caption is not None:
                self.content.append(NoEscape(r"\caption{" + caption + r"}"))
            if label is not None:
                self.content.append(NoEscape(r"\label{eq:" + label + r"}"))
            self.content.append(NoEscape(r"\end{equ}"))

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

        # End Appendix for businessReport
        if hasattr(self, "businessReportAppendix"):
            self.doc.append(NoEscape(r"\end{appendices}"))

        # Copy classfile to output folder
        if hasattr(self, "classFile"):
            inputpath = os.path.join(
                self.doc._select_filepath(filepath=None), self.classFile
            )
            outputpath = self.classFileName + ".cls"
            shutil.copyfile(inputpath, outputpath)

        self.doc.generate_pdf(self.filename, clean=True, clean_tex=False, silent=True)

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
