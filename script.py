import xmltodict
import subprocess
import sys

input = 'input/curriculum.xml'
output = 'output/curriculum.tex'

def tex(string): # Avoids tex injection
    if '\\' in string:
        print(f"Violation access error: '{string}'")
        sys.exit(1)
    return string

def main():
    
    with open(input, 'r', encoding='utf-8') as f:
        curriculum_dict = xmltodict.parse(f.read())
    
    category = curriculum_dict['category']

    latex_template = r'''\documentclass[11pt,a4paper]{article}

\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{enumitem}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{fontawesome}

\usepackage[scaled]{helvet}
\renewcommand\familydefault{\sfdefault} 

\definecolor{darkpurple}{rgb}{0.5, 0.1, 0.35}
\definecolor{darkbrown}{rgb}{0.5, 0.3, 0.1}
\definecolor{darkred}{rgb}{0.35, 0, 0}
\definecolor{lightred}{rgb}{0.65, 0, 0}
\definecolor{darkorange}{rgb}{0.7, 0.4, 0.2}

\input{glyphtounicode}
\pdfgentounicode=1

\newcommand{\customsection}[1]{
    \section*{\textcolor{darkred}{{{\textbf{\textit{#1}}}}}}

    \vspace{-2em}
    \textcolor{darkred}{\rule{\textwidth}{0.4pt}}

}

\begin{document}

\pagestyle{empty}

\centerline{\textcolor{darkred}{\textbf{\huge %(author)s}}}

\bigskip

\centerline{%(contact)s}

%(summary)s

%(skill)s

%(experience)s

%(project)s

%(education)s

%(language)s

\end{document}'''

    ### author ###
    author = tex(category['head']['@author'])

    ### contact ###
    contact_str = ''
    contacts = category['head']['contact']

    if not isinstance(contacts, list):
        contacts = [contacts]
    for contact in contacts:
        icon = tex(contact['@icon'])
        link = tex(contact['@link'])
        name = tex(contact['@name'])
        if icon != '':
            contact_str += r'\fa%s \hspace{0.1cm} ' % (icon)
        contact_str += r'\href{%s}{\textcolor{blue}{\underline{%s}}} | ' % (link, name)
    
    contact_str = contact_str.rstrip(' | ')

    ### Summary ###
    summary_str = ''

    if 'summary' in category:
        summary_name = 'Summary'
        summary_replace = tex(category['@summary'])
        if summary_replace != '':
            summary_name = summary_replace
        summary_str += r'\customsection{%s}' % (summary_name)
        summary_str += '\n\n'
        summary_str += r'\vspace{1.5em}'
        summary_str += '\n\n'
        summary_str += category['summary']['@area']

    ### Skill ###
    skill_str = ''

    if 'skills' in category:
        skills_name = 'Technical Skills'
        skills_replace = tex(category['@skills'])
        if skills_replace != '':
            skills_name = skills_replace
        skill_str += r'\customsection{%s}' % (skills_name)
        skill_str += '\n\n'
        skill_str += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
        skill_str += '\n\t'
        fields = category['skills']['field']

        if isinstance(fields, list):
            for i, field in enumerate(fields):
                name_field = tex(field['@name'])
                skill_str += r'\item \textcolor{darkgray}{\textbf{%s}}: ' % (name_field)

                skill_list = field['skill']
                if not isinstance(skill_list, list):
                    skill_list = [skill_list]

                for skill in skill_list:
                    name_skill = tex(skill['@name'])
                    skill_str += r'%s, ' % (name_skill)
                skill_str = skill_str.rstrip(', ')
                if i < len(fields) - 1:
                    skill_str += '\n\t'
        else:
            name_field = tex(fields['@name'])
            skill_str += r'\item \textcolor{darkgray}{\textbf{%s}}: ' % (name_field)

            skill_list = fields['skill']
            if not isinstance(skill_list, list):
                skill_list = [skill_list]

            for skill in skill_list:
                name_skill = tex(skill['@name'])
                skill_str += r'%s, ' % (name_skill)
            skill_str = skill_str.rstrip(', ')
        skill_str += '\n'
        skill_str += r'\end{itemize}'
    
    ### Experience ###
    experience_str = ''

    if 'experiences' in category:
        experiences_name = 'Work Experience'
        experiences_replace = tex(category['@experiences'])
        if experiences_replace != '':
            experiences_name = experiences_replace
        
        experience_str += r'\customsection{%s}' % (experiences_name)
        experience_str += '\n\n'
        experience_str += r'\begin{itemize}[leftmargin=*]'
        experience_str += '\n'
        
        experiences = category['experiences']['experience']
        if isinstance(experiences, list):
            for experience in experiences:
                role_experience = tex(experience['@role'])
                company_experience = tex(experience['@company'])
                date_experience = tex(experience['@date'])
                experience_str += '\t'
                experience_str += r'\item \textcolor{darkpurple}{\textbf{%s}} ' % (role_experience)
                experience_str += r'( \faInstitution \hspace{0.05cm} %s | \faCalendar \hspace{0.1cm} %s )' % (company_experience, date_experience)
                experience_str += r'\vspace{0.5em} \\'
                experience_str += '\n'

                infos = experience['info']
                if not isinstance(infos, list):
                    infos = [infos]
                for i, info in enumerate(infos):
                    info_experience = tex(info['@text'])
                    experience_str += r'%s' % (info_experience)
                    if i < len(infos) - 1:
                        experience_str += r' \\'
                        experience_str += '\n\t'
                    else:
                        experience_str += '\n'
        else:
            role_experience = tex(experiences['@role'])
            company_experience = tex(experiences['@company'])
            date_experience = tex(experiences['@date'])
            experience_str += '\t'
            experience_str += r'\item \textcolor{darkpurple}{\textbf{%s}} ' % (role_experience)
            experience_str += r'( \faInstitution \hspace{0.05cm} %s | \faCalendar \hspace{0.1cm} %s )' % (company_experience, date_experience)
            experience_str += r'\vspace{0.5em} \\'
            experience_str += '\n'

            infos = experiences['info']
            if not isinstance(infos, list):
                infos = [infos]
            for i, info in enumerate(infos):
                info_experience = tex(info['@text'])
                experience_str += r'- %s' % (info_experience)
                if i < len(infos) - 1:
                    experience_str += r' \\'
                    experience_str += '\n\t'
                else:
                    experience_str += '\n'

        experience_str += r'\end{itemize}'

    ### Project ###
    project_str = ''

    if 'projects' in category:
        projects_name = 'Featured Projects'
        projects_replace = tex(category['@projects'])
        if projects_replace != '':
            projects_name = projects_replace

        project_str += r'\customsection{%s}' % (projects_name)
        project_str += '\n\n'
        project_str += r'\begin{itemize}[label=$\bullet$, leftmargin=*]'
        project_str += '\n'

        projects = category['projects']['project']
        if isinstance(projects, list):
            for project in projects:
                name_project = tex(project['@name'])
                project_str += '\t'
                project_str += r'\item \textcolor{darkbrown}{\textbf{%s}} ( ' % (name_project)

                refs = project['refs']['ref']
                if not isinstance(refs, list):
                    refs = [refs]
                for i, ref in enumerate(refs):
                    icon_ref = tex(ref['@icon'])
                    link_ref = tex(ref['@link'])
                    name_ref = tex(ref['@name'])
                    if icon_ref != '':
                        project_str += r'\fa%s \hspace{0.1cm} ' % (icon_ref)
                    project_str += r'\href{%s}{\textcolor{blue}{\underline{%s}}} ' % (link_ref, name_ref)
                    if i < len(refs) - 1:
                        project_str += ' | '
                    else:
                        project_str += r')\vspace{0.5em} \\'
                        project_str += '\n\t'

                description = project['description']['info']
                if not isinstance(description, list):
                    description = [description]
                for i, info in enumerate(description):
                    text_info = tex(info['@text'])
                    project_str += r'- %s' % (text_info)
                    if i < len(description) - 1:
                        project_str += r' \\'
                        project_str += '\n\t'
                    else:
                        project_str += '\n'
        else:
            name_project = tex(projects['@name'])
            project_str += '\t'
            project_str += r'\item \textcolor{darkbrown}{\textbf{%s}} ( ' % (name_project)

            refs = projects['refs']['ref']
            if not isinstance(refs, list):
                refs = [refs]
            for i, ref in enumerate(refs):
                icon_ref = tex(ref['@icon'])
                link_ref = tex(ref['@link'])
                name_ref = tex(ref['@name'])
                if icon_ref != '':
                    project_str += r'\fa%s \hspace{0.1cm} ' % (icon_ref)
                project_str += r'\href{%s}{\textcolor{blue}{\underline{%s}}} ' % (link_ref, name_ref)
                if i < len(refs) - 1:
                    project_str += ' | '
                else:
                    project_str += r')\vspace{0.5em} \\'
                    project_str += '\n\t'

            description = projects['description']['info']
            if not isinstance(description, list):
                description = [description]
            for i, info in enumerate(description):
                text_info = tex(info['@text'])
                project_str += r'- %s' % (text_info)
                if i < len(description) - 1:
                    project_str += r' \\'
                    project_str += '\n\t'
                else:
                    project_str += '\n'

        project_str += r'\end{itemize}'

    ### Education ###
    education_str = ''

    if 'educations' in category:
        educations_name = 'Education'
        educations_replace = tex(category['@educations'])
        if educations_replace != '':
            educations_name = educations_replace
        
        education_str += r'\customsection{%s}' % (educations_name)
        education_str += '\n\n'
        education_str += r'\begin{itemize}[leftmargin=*]'
        education_str += '\n'

        educations = category['educations']['education']
        if not isinstance(educations, list):
            educations = [educations]
        for education in educations:
            field = tex(education['@field'])
            institution = tex(education['@institution'])
            date = tex(education['@date'])
            local = tex(education['@local'])

            education_str += '\t'
            education_str += r'\item \textcolor{lightred}{\textbf{%s}} \\' %(field)
            education_str += '\n\t'

            education_str += r'\faInstitution \hspace{0.1cm} %s \\' % (institution)
            education_str += '\n\t'

            education_str += r'\hspace*{-0.1cm} \faCalendar \hspace{0.15cm} %s \\' % (date)
            education_str += '\n\t'

            education_str += r'\hspace*{-0.025cm} \faMapMarker \hspace{0.21cm} %s' % (local)
            education_str += '\n'
        education_str += r'\end{itemize}'

    ### Language ###
    language_str = ''

    if 'languages' in category:
        languages_name = 'Languages'
        languages_replace = tex(category['@languages'])
        if languages_replace != '':
            languages_name = languages_replace

        language_str += r'\customsection{%s}' % (languages_name)
        language_str += '\n\n'
        language_str += r'\begin{itemize}[leftmargin=*]'
        language_str += '\n'

        languages = category['languages']['language']
        if not isinstance(languages, list):
            languages = [languages]
        for language in languages:
            name = tex(language['@name'])
            level = tex(language['@level'])
            language_str += '\t'
            language_str += r'\item \textcolor{darkorange}{\textbf{%s}} (\textit{%s})' %(name, level)
            language_str += '\n'
        language_str += r'\end{itemize}'

    # Template
    latex_content = latex_template % {
        'author': author,
        'contact': contact_str,
        'summary': summary_str,
        'skill': skill_str,
        'experience': experience_str,
        'project': project_str,
        'education': education_str,
        'language': language_str
    }

    with open(output, 'w') as f:
        f.write(latex_content)
    
    print("LaTeX file generated with success!")

    # Make PDF
    try:
        subprocess.run(['pdflatex', '-output-directory=output', output], check=True)
        print("PDF generated with success!")
    except subprocess.CalledProcessError as e:
        print(f"Error as generating PDF: {e}")

if __name__ == "__main__":
    main()