from modules.latex import tex, toList

# Tex plain text
def test_tex_plain_text():
    assert tex("Hello World") == "Hello World"

# Tex injection
def test_tex_escapes_special_chars():
    chars = r"\\{}$&#%_^~"
    result = r"\textbackslash{}\textbackslash{}\{\}\$\&\#\%\_\textasciicircum{}\textasciitilde{}"

    assert tex(chars) == result

# Convert dict to list(dict)
def test_tolist_dict():
    data = {"A": 1, "B": 2, "C": 3}
    assert toList(data) == [{"A": 1, "B": 2, "C": 3}]

# Convert list to list
def test_tolist_list():
    data = [1, 2, 3]
    assert toList(data) == data