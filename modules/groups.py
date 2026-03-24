from .latex import tex, toList

# Author
def author(data: dict) -> str:
    return tex(data['head']['@author'])

# Career
def career(data: dict) -> str:
    return tex(data['head']['@career'])

# Contact
def contact(data: dict) -> str:
    contactData = []
    contacts = toList(data['head']['contact'])

    for contact in contacts:
        icon = tex(contact.get('@icon', ''))
        link = tex(contact.get('@link', ''))
        name = tex(contact.get('@name', ''))

        piece = ''
        if icon:
            piece += r'\fa%s \hspace{0.1cm} ' % (icon)
        if link:
            piece += r'\href{%s}{\underline{%s}}' % (link, name)
        else:
            piece += r'{%s}' % (name)

        contactData.append(piece)
    
    return ' | '.join(contactData)

# Summary
def summary(data: dict) -> str:
    if 'summary' not in data:
        return

    summaryStr = ''
    summaryName = 'Summary'
    summaryReplace = tex(data.get('@summary', ''))

    if summaryReplace:
        summaryName = summaryReplace

    summaryStr += r'\customsection{%s}' % (summaryName)
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

    experienceStr += r'\customsection{%s}' % (experiencesName)
    experienceStr += '\n\n'
    experienceStr += r'\begin{itemize}[leftmargin=*]'
    experienceStr += '\n'

    experiences = toList(data['experiences']['experience'])

    for experience in experiences:
        roleExperience = tex(experience['@role'])
        companyExperience = tex(experience['@company'])
        dateExperience = tex(experience['@date'])
        experienceStr += '\t'
        experienceStr += r'\item \textbf{%s} ' % (roleExperience)
        experienceStr += r'( \faInstitution \hspace{0.05cm} %s | \faCalendar \hspace{0.1cm} %s )' % (companyExperience, dateExperience)
        experienceStr += r'\vspace{0.5em} \\'
        experienceStr += '\n'

        infos = toList(experience['info'])

        for i, info in enumerate(infos):
            infoExperience = tex(info['@text'])
            experienceStr += r'%s' % (infoExperience)
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

    projectStr += r'\customsection{%s}' % (projectsName)
    projectStr += '\n\n'
    projectStr += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
    projectStr += '\n'

    projects = toList(data['projects']['project'])

    for project in projects:
        nameProject = tex(project['@name'])
        projectStr += '\t'
        projectStr += r'\item \textbf{%s} ( ' % (nameProject)

        refs = project['refs']['ref']
        if not isinstance(refs, list):
            refs = [refs]
        for i, ref in enumerate(refs):
            iconRef = tex(ref['@icon'])
            linkRef = tex(ref['@link'])
            nameRef = tex(ref['@name'])
            if iconRef != '':
                projectStr += r'\fa%s \hspace{0.1cm} ' % (iconRef)
            projectStr += r'\href{%s}{\underline{%s}} ' % (linkRef, nameRef)
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
            projectStr += r'%s' % (textInfo)
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
        
    educationStr += r'\customsection{%s}' % (educationsName)
    educationStr += '\n\n'
    educationStr += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
    educationStr += '\n'

    educations = toList(data['educations']['education'])

    for education in educations:
        field = tex(education['@field'])
        institution = tex(education['@institution'])
        date = tex(education['@date'])
        grade = tex(education['@grade'])

        educationStr += r'\item \textbf{%s} | \textbf{%s}' %(field, institution)

        educationStr += r'\hfill \faCalendar\ \textit{%s} \\[10pt]' % date

        educationStr += r'\textbf{Grade}: %s' % grade
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

    skillStr += r'\customsection{%s}' % (skillsName)
    skillStr += '\n\n'
    skillStr += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
    skillStr += '\n\t'
    fields = toList(data['skills']['field'])

    for i, field in enumerate(fields):
        nameField = tex(field['@name'])
        skillStr += r'\item \textbf{%s}: ' % (nameField)

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