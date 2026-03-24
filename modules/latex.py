# Avoids tex injection
def tex(s: str) -> str:
    replacements = {
        '\\': r'\textbackslash{}',
        '{': r'\{',
        '}': r'\}',
        '$': r'\$',
        '&': r'\&',
        '#': r'\#',
        '%': r'\%',
        '_': r'\_',
        '^': r'\textasciicircum{}',
        '~': r'\textasciitilde{}'
    }

    return "".join(replacements.get(c, c) for c in s)

# Convert to list
def toList(data: list | dict) -> list:
    if isinstance(data, list):
        return data
    return [data]