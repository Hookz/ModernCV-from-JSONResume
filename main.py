from resume import Resume
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--json",
    type=str,
    help="JSONResume file location",
    default="resume.json"
)
parser.add_argument(
    "--color",
    type=str,
    help="Color scheme of the resume",
    default="green",
    choices=["blue", "green", "red", "orange", "grey", "black"],
)
parser.add_argument(
    "--style",
    type=str,
    help="Style of the resume",
    default="fancy",
    choices=["fancy", "classic", "casual", "banking"],
)
parser.add_argument(
    "--font",
    type=str,
    help="Roman or sans-serif font setting",
    default="sans",
    choices=['sans', 'roman']
)
parser.add_argument(
    "--font_size",
    type=str,
    help="Font size (in pts)",
    default="11",
    choices=['10','11','12']
)
parser.add_argument(
    "--paper_size",
    type=str,
    help="Paper size",
    default="a4paper",
    choices=['a4paper', 'a5paper', 'b5paper', 'letterpaper', 'legalpaper', 'executive-paper', 'landscape']
)

args = parser.parse_args()

res = Resume(args.style, args.color, args.font_size+"pt", args.paper_size, args.font).load_json(args.json)

print(res)

with open("resume.tex", "w") as output_file:
    output_file.write(str(res))
os.system("latexmk -pdf -pv resume.tex")
os.system("latexmk -c")
#os.system("pdflatex resume.tex")

