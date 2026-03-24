import xmltodict
import subprocess

from modules.utils import AutoCV

INPUT = 'input/curriculum.xml'
OUTPUT = 'output/curriculum.tex'

def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        curriculumDict = xmltodict.parse(f.read())
    
    category = curriculumDict['category']

    # Create CV
    latex = AutoCV(category)
    latex.fit()
    content = latex.result

    with open(OUTPUT, 'w') as f:
        f.write(content)
    
    print("LaTeX file generated with success!")

    # Make PDF
    try:
        subprocess.run(['pdflatex', '-output-directory=output', OUTPUT], check=True)
        print("PDF generated with success!")
    except subprocess.CalledProcessError as e:
        print(f"Error as generating PDF: {e}")

if __name__ == "__main__":
    main()
