## Curriculum Generator

This project uses a prototype resume developed in LaTeX that can be edited using XML file, which can be used to create resume in PDF. I did this to automate formatting and simplify editing resumes for different scenarios. The formatting order is given by:

* Heading
* Summary
* Skills
* Experience
* Projects
* Education
* Languages

### How to Use

It requires python and tex packages on your operating system to run it. To create a resume, simply edit **curriculum.xml** file in the input folder and run script.py. The current file serves as an example of how the structure works. After that, tex and pdf files will be generated in the output folder if everything works correctly.

### Notes

It's not allowed to add the '\\' character in the parameters to avoid tex injection. Access violation error will occur if you do this.
