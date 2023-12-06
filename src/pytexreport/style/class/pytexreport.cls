\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{pytexreport}[PyTexReport Base Class]

% Load base article class to build up on
\LoadClass[12pt, a4paper]{article}

% Load packages (no clashes hopefully)
% SEAD
\usepackage{amsfonts}
\usepackage{graphicx}
\usepackage{dblfloatfix}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{float}
\usepackage{tocbibind}
\usepackage{enumitem}
\usepackage{comment}
\usepackage[export]{adjustbox}
\usepackage[toc,page]{appendix}
\usepackage[titles]{tocloft}
\usepackage{subfig}
\usepackage{chngcntr}
\usepackage{amsmath}
\usepackage{tabularx}
\usepackage{multirow}
\usepackage{tcolorbox}
\usepackage{pdfpages}
\usepackage{rotating}
\usepackage{tikz}
\usepackage{longtable}
\usepackage{hyperref}
\usepackage{textcomp, gensymb}
\usepackage{titlesec}
\usepackage{calc}
\usepackage{booktabs}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{csquotes}
\usepackage{caption}
\usepackage{eso-pic}
\usepackage{wrapfig}
\usepackage{charter}

% Paragraph indentation
\setlength\parindent{0pt}

% Compress itemize to make it look more presentable
\setitemize{noitemsep,topsep=0pt,parsep=0pt,partopsep=5pt}

% Equations numbered according to section
\counterwithin{figure}{section}
\counterwithin{table}{section}
\counterwithin{equation}{section}
\numberwithin{equation}{section}

% tabularx settings
\newcolumntype{P}[1]{>{\centering\arraybackslash}p{#1}}

% generally useful math things
\DeclareMathOperator{\tr}{Tr}
\newcommand*{\op}[1]{\check{\mathbf#1}}
\newcommand{\bra}[1]{\langle #1 |}
\newcommand{\ket}[1]{| #1 \rangle}
\newcommand{\braket}[2]{\langle #1 | #2 \rangle}
\newcommand{\mean}[1]{\langle #1 \rangle}
\newcommand{\opvec}[1]{\check{\vec #1}}
\renewcommand{\sp}[1]{$${\begin{split}#1\end{split}}$$}