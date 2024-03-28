"""
This example shows the functionality of the PyLaTeX library.

It creates a sample report with 2 tables, one containing images and the other
containing data. It also creates a complex header with an image.

..  :copyright: (c) 2023 by nkalis
    :license: MIT, see License for more details.
"""

# begin-doc-include
import matplotlib.pyplot as plt
import numpy as np
from PyTexReport.style import ieeeConference

report = ieeeConference(
    title="Conference Paper Title*",
    authors={
        "author1": {
            "fullname": "Given Name, Surname",
            "department": "dept. name of organization (of Aff.)",
            "affiliation": "name of organization (of Aff.)",
            "city": "City",
            "country": "Country",
            "contact": "email address or ORCID",
        },
        "author2": {
            "fullname": "Given Name, Surname",
            "department": "dept. name of organization (of Aff.)",
            "affiliation": "name of organization (of Aff.)",
            "city": "City",
            "country": "Country",
            "contact": "email address or ORCID",
        },
        "author3": {
            "fullname": "Given Name, Surname",
            "department": "dept. name of organization (of Aff.)",
            "affiliation": "name of organization (of Aff.)",
            "city": "City",
            "country": "Country",
            "contact": "email address or ORCID",
        },
    },
    thanks="Identify applicable funding agency here. If none, omit this.",
    title_note="*Note: Sub-titles are not captured in Xplore and should not be used",
)

report.createAbstract(
    "This document is a model and instructions for LATEX. This and the IEEEtran.cls file define the components of your paper [title, text, heads, etc.]. *CRITICAL: Do Not Use Symbols, Special Characters, Footnotes, or Math in Paper Title or Abstract."
)
report.createKeywords(["component", "formatting", "style", "styling", "insert"])

report.createSection("Introduction")
# report.addText('Text goes here.')

report.createSubSection("No Line Breaks")
report.addText("Text goes here.")
report.addText("Text goes here.")
report.addText("Text goes here.", new_paragraph=False)

report.createSubSection("Line Breaks")
report.addText("Text goes here.")
report.createNewLine()
report.addText("More Text goes here")

report.createSubSection("Special text")
report.createSubSubSection("Referencing")
report.addText("#TODO: Add referencing")
report.createSubSubSection("Citing")
report.addText("#TODO: Add citations")
report.createSubSubSection("Special Text")
report.addText("You can add comments so you dont forget to ad")
report.addText("#TODO : Add TODOs")
report.addText("#! : Add warnings")
report.addText("#* : Add information")
report.addText("#? : Add highlighted questions")

report.createSection("Lists and Tables")
# report.addText('Text goes here.')

report.createSubSection("Lists")
report.addText("You can make an itemized list")
report.addList(
    [
        "Here is an item.",
        "And another one.",
        "One more for good luck.",
    ]
)

report.addVSpace()
report.addText("You can make an enumerated list")
report.addList(
    [
        "Here is an item.",
        "And another one.",
        "One more for good luck.",
    ],
    type=2,
)

report.addVSpace()
report.addText("Or a desciption list")
report.addList(
    [
        ["Here is an item description", "item1"],
        ["Here is an item description", 12],
        ["Here is an item description", "item3"],
    ],
    type=3,
)

report.createSubSection("Tables")
report.addText("Tables are very easy to make.")
tdata = {
    "data": [
        ["Table Header 1", "Table Header 2", "Table Header 3"],
        ["75%", "56.61", "58.94"],
    ],
    "nrow": 2,
    "ncol": 3,
}
report.addTable(
    data=tdata["data"],
    nrow=tdata["nrow"],
    ncol=tdata["ncol"],
    caption="Test Table 1 Caption",
    label="testtable1",
)

report.createSection("Plotting and Figures")
report.createSubSection("Matplotlib.pyplot plots")
x = [0, 1, 2, 3, 4, 5, 6]
y = [15, 2, 7, 1, 5, 6, 9]
plt.plot(x, y)
report.addMatplot(plt, caption="Test Plot 1", label="testplot1")

report.createSubSection("Figures")
report.addFigure(file="logo.png", caption="University Logo", label="unilogo")

report.createSection("Math")
report.createSubSection("Inputting (and automatically generating) functions")
# See more here: https://colab.research.google.com/drive/1MuiawKpVIZ12MWwyYuzZHmbKThdM5wNJ?usp=sharing#scrollTo=4IPGyu2dFH6T

report.createSubSection("Here are some generated functions", numbering=False)


def solve(a, b, c):
    return (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)


report.addEquation(solve, caption="Generated Function", label="function1")


def solve(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)


report.addEquation(solve, caption="Generated Function (if and or)", label="function2")

report.createSubSection("Here is a handmade function", numbering=False)
report.addEquation(
    r"\oint \sqrt{x^2+1}", caption="Handmade Function", label="function3"
)

report.createSection("Math and matrixes")

report.createSubSection("Standard Matrix")
M = np.matrix([[2, 3, 4], [0, 0, 1], [0, 0, 2]])
report.addMatrix(matrix_equation="M", matrix_data=M, matrix_type="b")

report.createSubSection("Formatting to look like a vector")
a = np.array([[100, 10, 20]]).T
report.addMatrix(matrix_equation=r"\boldsymbol{\alpha}", matrix_data=a, matrix_type="p")

report.createSubSection("Showing how easy it is to combine two")
matrix_product = M * a
report.addMatrix(
    matrix_equation=r"M\boldsymbol{\alpha}", matrix_data=matrix_product, matrix_type="b"
)

report.flush()
report.output()
