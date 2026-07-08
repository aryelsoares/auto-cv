from .latex import tex, toList

# Author
def author(data: dict) -> str:
    return tex(data['head']['@author'])

# Career
def career(data: dict) -> str:
    return tex(data['head']['@career'])

# Contact
def contact(data: dict) -> str:
    contacts = toList(data['head']['contact'])
    lines = {}
    
    for contact in contacts:
        icon = tex(contact.get('@icon', ''))
        link = tex(contact.get('@link', ''))
        name = tex(contact.get('@name', ''))
        piece = ''
        
        if icon:
            piece += rf'\fa{icon} \hspace{{0.1cm}} '
        if link:
            piece += rf'\href{{{link}}}{{\underline{{{name}}}}}'
        else: piece += rf'{{{name}}}'
        
        line = int(contact.get('@line', 1))
        lines.setdefault(line, []).append(piece)
    
    orderedLines = []
    for line in sorted(lines.keys()):
        content = ' | '.join(lines[line])
        orderedLines.append(rf'\centerline{{{content}}}')
    
    return '\n'.join(rf'{line}\vspace{{0.3em}}' for line in orderedLines)

# Summary
def summary(data: dict) -> str:
    if 'summary' not in data:
        return ''

    summaryStr = ''
    summaryName = 'Summary'
    summaryReplace = tex(data.get('@summary', ''))

    if summaryReplace:
        summaryName = summaryReplace

    summaryStr += rf'\customsection{{{summaryName}}}'
    summaryStr += '\n\n'
    summaryStr += r'\vspace{1.5em}'
    summaryStr += '\n\n'
    summaryStr += data['summary']['@area']
    
    return summaryStr

# Experiences
def experience(data: dict) -> str:
    if 'experiences' not in data:
        return ''

    experienceStr = ''
    experiencesName = 'Work Experience'
    experiencesReplace = tex(data.get('@experiences', ''))

    if experiencesReplace:
        experiencesName = experiencesReplace

    experienceStr += rf'\customsection{{{experiencesName}}}'
    experienceStr += '\n\n'
    experienceStr += r'\begin{itemize}[leftmargin=*]'
    experienceStr += '\n'

    experiences = toList(data['experiences']['experience'])

    for experience in experiences:
        roleExperience = tex(experience['@role'])
        companyExperience = tex(experience['@company'])
        dateExperience = tex(experience['@date'])
        experienceStr += '\t'
        experienceStr += rf'\item \textbf{{{roleExperience}}} '
        experienceStr += rf'( \faInstitution \hspace{{0.05cm}} {companyExperience} | \faCalendar \hspace{{0.1cm}} {dateExperience} )'
        experienceStr += r'\vspace{0.5em} \\'
        experienceStr += '\n'

        infos = toList(experience['info'])

        for i, info in enumerate(infos):
            infoExperience = tex(info['@text'])
            experienceStr += infoExperience
            if i < len(infos) - 1:
                experienceStr += r' \\'
                experienceStr += '\n\t'
            else:
                experienceStr += '\n'

    experienceStr += r'\end{itemize}'

    return experienceStr

# Projects
def project(data: dict) -> str:
    if 'projects' not in data:
        return ''

    projectStr = ''
    projectsName = 'Featured Projects'
    projectsReplace = tex(data.get('@projects', ''))

    if projectsReplace:
        projectsName = projectsReplace

    projectStr += rf'\customsection{{{projectsName}}}'
    projectStr += '\n\n'
    projectStr += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
    projectStr += '\n'

    projects = toList(data['projects']['project'])

    for project in projects:
        nameProject = tex(project['@name'])
        projectStr += '\t'
        projectStr += rf'\item \textbf{{{nameProject}}} ( '

        refs = project['refs']['ref']
        if not isinstance(refs, list):
            refs = [refs]
        for i, ref in enumerate(refs):
            iconRef = tex(ref['@icon'])
            linkRef = tex(ref['@link'])
            nameRef = tex(ref['@name'])
            if iconRef != '':
                projectStr += rf'\fa{iconRef} \hspace{{0.1cm}} '
            projectStr += rf'\href{{{linkRef}}}{{\underline{{{nameRef}}}}} '
            if i < len(refs) - 1:
                projectStr += ' | '
            else:
                projectStr += r')\vspace{0.5em} \\'
                projectStr += '\n\t'

        description = toList(project['description']['info'])
        projectDesc = '- '

        for i, info in enumerate(description):
            textInfo = tex(info['@text'])
            projectStr += projectDesc
            projectStr += textInfo
            if i < len(description) - 1:
                projectStr += r' \\'
                projectStr += '\n\t'
            else:
                projectStr += '\n'

    projectStr += r'\end{itemize}'

    return projectStr

# Educations
def education(data: dict) -> str:
    if 'educations' not in data:
        return ''
    
    educationStr = ''
    educationsName = 'Education'
    educationsReplace = tex(data.get('@educations', ''))

    if educationsReplace:
        educationsName = educationsReplace
        
    educationStr += rf'\customsection{{{educationsName}}}'
    educationStr += '\n\n'
    educationStr += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
    educationStr += '\n'

    educations = toList(data['educations']['education'])

    for education in educations:
        field = tex(education['@field'])
        institution = tex(education['@institution'])
        date = tex(education['@date'])
        grade = tex(education['@grade'])

        educationStr += rf'\item \textbf{{{field}}} | \textbf{{{institution}}}'

        educationStr += rf'\hfill \faCalendar\ \textit{{{date}}} \\[10pt]'

        educationStr += rf'\textbf{{grade}}: {grade}'
        educationStr += '\n'

    educationStr += r'\end{itemize}'

    return educationStr

# Skills
def skill(data: dict) -> str:
    if 'skills' not in data:
        return ''

    skillStr = ''
    skillsName = 'Technical Skills'
    skillsReplace = tex(data.get('@skills', ''))

    if skillsReplace:
        skillsName = skillsReplace

    skillStr += rf'\customsection{{{skillsName}}}'
    skillStr += '\n\n'
    skillStr += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
    skillStr += '\n\t'
    fields = toList(data['skills']['field'])

    for i, field in enumerate(fields):
        nameField = tex(field['@name'])
        skillStr += rf'\item \textbf{{{nameField}}}: '

        skillData = []
        skillList = toList(field['skill'])

        for skill in skillList:
            nameSkill = tex(skill['@name'])
            skillData.append(nameSkill)
        skillStr += ', '.join(skillData)

        if i < len(fields) - 1:
            skillStr += '\n\t'

    skillStr += '\n'
    skillStr += r'\end{itemize}'

    return skillStr

# Languages
def language(data: dict) -> str:
    if 'languages' not in data:
        return ''

    languageStr = ''
    languagesName = 'Languages'
    languagesReplace = tex(data.get('@languages', ''))

    if languagesReplace:
        languagesName = languagesReplace
    
    languageStr += rf'\customsection{{{languagesName}}}'
    languageStr += '\n\n'
    languageStr += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
    languageStr += '\n\t'
    languages = toList(data['languages']['language'])

    for language in languages:
        name = tex(language['@name'])
        level = tex(language['@level'])
        desc = "(" + tex(language.get('@desc', '')) + ")"

        if desc == "()":
            desc = ""

        languageStr += rf'\item \textbf{{{name}}}: '
        languageStr += rf'\textit{{{level}}} '
        languageStr += desc

    languageStr += '\n'
    languageStr += r'\end{itemize}'

    return languageStr
