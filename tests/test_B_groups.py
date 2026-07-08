import pytest
import xmltodict
from modules import groups

INPUT = 'input/example.xml'

# Normalize
def normalize(s: str) -> str:
    return (
        s.replace("\t", "    ")
         .rstrip()
    )

# Group Test
@pytest.fixture
def cv() -> dict:
    with open(INPUT, 'r', encoding='utf-8') as f:
        example = xmltodict.parse(f.read())

    return example['category']

# Author
def test_author(cv):
    assert groups.author(cv) == 'Your Name'

# Career
def test_career(cv):
    assert groups.career(cv) == 'Profession'

# Contact
def test_contact(cv):
    data = '\\centerline{\\faEnvelope \\hspace{0.1cm} \\href{example@gmail.com}{\\underline{My Email}}}\\vspace{0.3em}\n\\centerline{\\faLinkedin \\hspace{0.1cm} \\href{https://www.linkedin.com/in/example/}{\\underline{My Linkedin}} | \\faGithub \\hspace{0.1cm} \\href{https://github.com/example}{\\underline{My Github}}}\\vspace{0.3em}'
    assert groups.contact(cv) == data

# Summary
def test_summary(cv):
    data = r'''\customsection{Summary}

\vspace{1.5em}

Your description.'''

    assert groups.summary(cv) == data

# Experience
def test_experience(cv):
    data = r'''\customsection{Work Experience}

\begin{itemize}[leftmargin=*]
    \item \textbf{Data Analyst} ( \faInstitution \hspace{0.05cm} Facebook | \faCalendar \hspace{0.1cm} 2010 - 2014 )\vspace{0.5em} \\
I did this. \\
    And also that.
\end{itemize}'''

    assert normalize(groups.experience(cv)) == normalize(data)

# Projects
def test_project(cv):
    data = r'''\customsection{Featured Projects}

\begin{itemize}[label=$\bullet$, leftmargin=*]
    \item \textbf{My Project} ( \faGlobe \hspace{0.1cm} \href{https://www.mypage.com/example/}{\underline{Webpage}}  | \faGithub \hspace{0.1cm} \href{https://github.com/name/myproject}{\underline{Github}} )\vspace{0.5em} \\
    - I did this. \\
    - And also that.
\end{itemize}'''

    assert normalize(groups.project(cv)) == normalize(data)

# Educations
def test_education(cv):
    data = r'''\customsection{Education}

\begin{itemize}[label=$\bullet$, leftmargin=*]
\item \textbf{Software Engineering} | \textbf{Harvard}\hfill \faCalendar\ \textit{2006 - 2010} \\[10pt]\textbf{grade}: Description.
\end{itemize}'''

    assert normalize(groups.education(cv)) == normalize(data)

# Skills
def test_skill(cv):
    data = r'''\customsection{Technical Skills}

\begin{itemize}[label=$\bullet$, leftmargin=*]
    \item \textbf{Backend}: Python, Rust, Java
    \item \textbf{Frontend}: HTML, CSS, Javascript
\end{itemize}
'''

    assert normalize(groups.skill(cv)) == normalize(data)