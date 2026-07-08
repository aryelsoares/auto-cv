from modules import groups

RENDERERS = {
    "author": groups.author,
    "career": groups.career,
    "contact": groups.contact,
    "summary": groups.summary,
    "experience": groups.experience,
    "project": groups.project,
    "education": groups.education,
    "skill": groups.skill,
    "language": groups.language
}

# Start latex
def begin(data: dict) -> str:
    rendered = {
        key: func(data)
        for key, func in RENDERERS.items()
    }

    return r'''\documentclass[11pt,a4paper]{article}

\usepackage[left=0.75in,right=0.75in,top=0.75in,bottom=0.75in]{geometry}
\usepackage{enumitem}
\usepackage[T1]{fontenc}
\usepackage{xcolor}
\usepackage[
    colorlinks=true,
    urlcolor=blue
]{hyperref}
\usepackage{fontawesome}

\usepackage[scaled]{helvet}
\renewcommand\familydefault{\sfdefault} 

\input{glyphtounicode}
\pdfgentounicode=1

\newcommand{\customsection}[1]{
    \section*{{{\textbf{\textit{#1}}}}}

    \vspace{-2em}
    \rule{\textwidth}{0.4pt}

}

\begin{document}

\pagestyle{empty}

\centerline{\textbf{\Huge %(author)s}}

\bigskip

\centerline{\textbf{\Large %(career)s}}

\bigskip

%(contact)s

%(summary)s

%(experience)s

%(project)s

%(education)s

%(skill)s

%(language)s

\end{document}''' % rendered

# CV Class
class AutoCV:
    def __init__(self, template: dict):
        self._template = template
        self._result: str | None = None

    def fit(self):
        self._result = begin(self._template)

    @property
    def result(self) -> str:
        if self._result is None:
            raise RuntimeError("CV not generated yet")
        return self._result