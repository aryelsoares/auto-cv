import pytest
import xmltodict
from modules.utils import begin, AutoCV

# Input Example Size
INPUT_SIZE = 1818

# Util Test
@pytest.fixture
def cv() -> dict:
    with open('input/example.xml', 'r', encoding='utf-8') as f:
        example = xmltodict.parse(f.read())
    
    return example['category']

# Begin
def test_begin(cv):
    assert len(begin(cv).replace(" ", "")) == INPUT_SIZE

# AutoCV
def test_autocv(cv):
    curr = AutoCV(cv)
    curr.fit()
    assert len(curr.result.replace(" ", "")) == INPUT_SIZE