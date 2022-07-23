# ModernCV from JSONResume

## About this converter
This converter allows for generating PDF files using [moderncv](https://github.com/moderncv/moderncv) and 
[JSON Resume schema](https://github.com/jsonresume/resume-schema). A full documentation may be written at a later point
but is not deemed necessary right now, as the usage will be explained in this README.

## Usage
To use this converter, clone this repository using ```git clone``` or just download the ZIP file. This converter 
does not require any tools outside of the vanilla Python 3.x. That being said, it is not built to be compatible
with Python 2.x. 

After downloading the repository, substitute the default (resume.json)[resume.json] file with your own file. 
Then, run `python main.py`, or execute the main class in the 
[IDE](https://en.wikipedia.org/wiki/Integrated_development_environment) of your choice.
Now, the script should generate a `resume.pdf` file, which is your beautiful new resume.

As long as your file is compliant with the JSON Resume schema, 
and you have [Latexmk](https://mg.readthedocs.io/latexmk.html), it should work without any issues. 

### External pictures
The software handles external pictures automatically. All picture descriptions starting with "http://" or "https://" are 
firstly downloaded to the local directory, and then the external URLs are converted to local, relative URIs,
which can be easily retrieved by LaTeX.

## Customization
To customize the output, edit the [main.py](main.py) file.

Available customizations are: *(default values in **bold**)*

|  Color  |  Font  |  Font size  |  Paper size  |  Style  |
|:-------:|:------:|:-----------:|:------------:|:-------:|
|blue     |roman   |10pt         |**a4paper**   |**fancy**|
|**green**|**sans**|**11pt**     |a5paper       |classic  |
|red      |        |12pt         |b5paper       |casual   |
|orange   |        |             |letterpaper   |         |
|grey     |        |             |legalpaper    |         |
|         |        |             |executive-paper|        |
|         |        |             |landscape     |         |
### Customization examples

To override default values, run [main.py](main.py) with arguments for which you want non-default values, eg.,
for orange color, roman font, 12pt, letter paper, and casual style:
```shell
python main.py --color orange --font roman --font_size 12 --paper_size letterpaper --style casual
```

Any omitted values will take default values. To display possible values in the console, run:
```shell
python main.py --help
```

**nb!** It is possible that your ``python`` command refers to a python version 2.x. In that case run ``python3``
to force python version 3.x. 

## Further development

There are currently no further development plans. However, should either JSONResume or ModernCV undergo breaking
changes, the repository will be updated to fix compatibility. 
