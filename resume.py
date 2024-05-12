import json
from urllib.request import Request, urlopen
from datetime import datetime


def tag_processor(tag, element):
    output = ""
    if tag is not None:
        if type(tag) is list:
            output += "{"
            for subtag in tag:
                output += f"{element[subtag]}, "
            output = output[:-2] + "}"
        else:
            output += f"{{{element[tag]}}}"
    else:
        output += "{}"
    return output


class Resume:
    def __init__(self, style="fancy", color="green", fontsize="11pt", papersize="a4paper",
                 font="sans", basics=None, work=None, volunteer=None, education=None, projects=None, certificates=None, awards=None, publications=None,
                 skills=None, languages=None, interests=None, references=None):
        self.documentclass = [fontsize, papersize, font]
        self.style = style
        self.color = color
        self.basics = basics
        self.work = work
        self.volunteer = volunteer
        self.education = education
        self.projects = projects
        self.certificates = certificates
        self.awards = awards
        self.publications = publications
        self.skills = skills
        self.languages = languages
        self.interests = interests
        self.references = references

    def load_json(self, json_file: str):
        with open(json_file) as json_file:
            data = json.load(json_file)
            new_skills = {}
            for entry in data['skills']:
                new_skills.setdefault(entry['level'], []).append({k: v for k, v in entry.items() if k != 'level'})
            data['skills'] = [{'level': k, 'entries': v} for k, v in new_skills.items()]
            if 'basics' in data.keys():
                self.basics = Basics().load_dict(data['basics'])
            if 'work' in data.keys():
                if 'company' in data['work'][0].keys():
                    self.work = Section(title="Experience", content=data['work'],
                                    tags=['position', 'company', None, None, 'summary'])
                else:
                    self.work = Work(data["work"])
            if "volunteer" in data.keys():
                self.volunteer = Subsection(
                    title="Volunteer",
                    content=data["volunteer"],
                    tags=["position", "organization", None, None, "summary"],
                )
            if "education" in data.keys():
                self.education = Section(
                    title="Education",
                    content=data["education"],
                    tags=[["studyType", "area"], "institution", None, None, None],
                )
            if "publications" in data.keys():
                self.publications = Section(
                    title="Publications",
                    content=data["publications"],
                    tags=["name", "publisher", None, None, "summary"],
                )
            if "projects" in data.keys():
                self.projects = Section(
                    title="Projects",
                    content=data["projects"],
                    tags=["name", "entity", None, None, "description"],
                )
            if "certificates" in data.keys():
                self.certificates = Certificates(data["certificates"])
            if "languages" in data.keys():
                self.languages = Languages(data["languages"])
            if "skills" in data.keys():
                self.skills = Skills(data["skills"])
            if "awards" in data.keys():
                self.awards = Awards(data["awards"])
            if "interests" in data.keys():
                self.interests = Interests(data["interests"])
            if "references" in data.keys():
                self.references = Section(
                    title="References",
                    content=data["references"],
                    tags=["name", None, None, None, "reference"],
                )
            for param in self.__dict__:
                if self.__dict__[param] is None:
                    self.__dict__[param] = ""
        return self

    def __str__(self):
        output = (
            f"\\documentclass[{','.join(self.documentclass)}]{{moderncv}}\n\\moderncvstyle{{{self.style}}}\n"
            f"\\moderncvcolor{{{self.color}}}\n\\usepackage[utf8x]{{inputenc}}\n"
            f"\\usepackage[scale=0.9]{{geometry}}\n\\recomputelengths\n\n"
            f"\\usepackage{{textgreek}}"
        )
        output += str(self.basics)
        output += "\\begin{document}\n\\maketitle"
        output += str(self.work)
        output += str(self.volunteer)
        output += str(self.education)
        output += str(self.projects)
        output += str(self.certificates)
        output += str(self.languages)
        output += str(self.skills)
        output += str(self.awards)
        output += str(self.interests)
        output += str(self.publications)
        output += str(self.references)
        output += "\\end{document}"
        return output


class Basics:
    def __init__(self, name: str = "", label: str = "", picture: str = "", email: str = "", phone: str = "",
                 website: str = "", summary: str = "", location: dict = "", profiles: list = ""):
        self.name = name
        self.label = label
        self.picture = picture
        self.email = email
        self.phone = phone
        self.website = website
        self.summary = summary
        self.location = location
        self.profiles = profiles

    def load_dict(self, dictionary):
        for name in self.__dict__:
            if name in dictionary.keys():
                if len(dictionary[name]) > 0:
                    self.__dict__[name] = dictionary[name]
        if self.picture.startswith("http://") or self.picture.startswith("https://"):
            req = Request(
                self.picture,
                headers={'User-Agent': 'Mozilla/5.0'})
            with open("profile.jpg", "wb") as output_file:
                output_file.write(urlopen(req).read())
            self.picture = 'profile.jpg'
        if self.__dict__['website'] == "":
            if 'url' in dictionary.keys():
                self.__dict__['website'] = dictionary['url']
        return self

    def __str__(self):
        for address_part in ["address", "postalCode", "city"]:
            if address_part not in self.location.keys():
                self.location[address_part] = ""
        output = (
            f"\\firstname{{{self.name.split(' ')[0]}}}\n\\familyname{{{self.name.split(' ')[1]}}}\n"
            f"\\title{{Resum\\'e}}\n"
            f"\\address{{{self.location['address']}}}{{{self.location['postalCode']+' '+self.location['city']}}}\n"
            f"\\mobile{{{self.phone}}}\n\\email{{{self.email}}}\n"
            + (f"\\photo[64pt]{{{self.picture}}}\n" if self.picture else "")
            + f"\\quote{{{self.summary}}}"
        )
        for profile in self.profiles:
            output += f"\\social[{profile['network'].lower()}]{{{profile['username']}}}\n"

        return output


class Awards:
    def __init__(self, content: list = None):
        self.content = content

    def __str__(self):
        output = "\\section{Awards}\n"
        for award in self.content:
            output += f"\\cventry{{{award['date'].split('-')[0]}}}{{{award['title']}}}{{{award['awarder']}}}{{}}{{}}{{{award['summary']}}}"
        return output


class Publications:
    """To be implemented"""


class Skills:
    def __init__(self, content: list):
        self.content = content

    def __str__(self):
        output = "\n\\section{Skills}\n"
        for level in self.content:
            output += f"\\subsection{{{level['level']}}}\n"
            for entry in level['entries']:
                output += f"\\cvlanguage{{{entry['name']}}}{{"
                for keyword in entry['keywords']:
                    output += f"{keyword}, "
                output = output[:-2] + "}{}\n"
            output += "\n"
        return output


class Interests:
    def __init__(self, content: list):
        self.content = content

    def __str__(self):
        output = "\n\\section{Interests}\n"
        for interest in self.content:
            output += f"\cvlanguage{{{interest['name']}}}{{"
            for keyword in interest['keywords']:
                output += f"{keyword}, "
            output = output[:-2] + "}{}\n"
        output += "\n"
        return output


class References:
    """To be implemented"""


class Certificates:
    def __init__(self, content: list = None):
        self.content = content

    def __str__(self):
        output = "\n\\section{Certificates}\n"
        for certificate in self.content:
            output += f"\\cventry{{{datetime.strptime(certificate['date'], '%Y-%m-%d').strftime('%b %Y')}}}"
            output += "{\href" + f"{{{certificate['url']}}}{{{certificate['name']}}}}}{{{certificate['issuer']}}}"
            output += "{}{}{}\n"
        output += "\n"
        return output


class Section:
    def __init__(self, title: str = None, language: bool = False, content: list = None, tags: list = None,
                 subsection: bool = False, subsections: list = None):
        self.title = title
        self.language = language
        self.content = content
        self.tags = tags
        self.subsection = subsection
        self.subsections = subsections

        # Set the url
        for element in self.content:
            if "url" in element and "name" in element:
                element["name"] = (
                    f"\\href{{ {element['url']} }}{{{element['name']} \\faExternalLink*}}"
                )

    def __str__(self):
        if self.subsection:

            output = f"\\subsection{{{self.title}}}\n"
        else:
            output = f"\n\n\\section{{{self.title}}}\n"
        if self.content is not None:
            if self.language:
                for element in self.content:
                    output += "\\cvlanguage"
                    for tag in self.tags:
                        output += tag_processor(tag, element)
                    output += "\n"
            else:
                for element in self.content:
                    if 'startDate' in element.keys():
                        output += f"\\cventry{{{datetime.strptime(element['startDate'], '%Y-%m-%d').strftime('%b %Y')}-"
                        if 'endDate' not in element.keys() or element['endDate'] == "":
                            output += "current}"
                        else:
                            output += (
                                datetime.strptime(
                                    element["endDate"], "%Y-%m-%d"
                                ).strftime("%b %Y")
                                + "}"
                            )
                    elif "releaseDate" in element.keys():
                        output += f"\\cventry{{{datetime.strptime(element['releaseDate'], '%Y-%m-%d').strftime('%b %Y')}}}"
                    else:
                        output += "\\cventry{}"
                    for tag in self.tags:
                        output += tag_processor(tag, element)
                    output += "\n"
        if type(self.subsections) is list:
            for subsection in self.subsections:
                output += str(subsection)
        return output

    def load_list(self, lst):
        self.content = lst
        return self


class Languages(Section):
    def __init__(self, content: list = None):
        super().__init__("Languages", True, content, ['language', 'fluency', None], False)


class Subsection(Section):
    def __init__(self, title: str = None, language: bool = False, content: list = None, tags: list = None):
        super().__init__(title, language, content, tags, True)


class Work(Section):
    def __init__(self, content: list = None):
        super().__init__(title="Experience", content=content, tags=['position', 'name', None, None, 'summary'])

    def __str__(self):
        if self.subsection:

            output = f"\\subsection{{{self.title}}}\n"
        else:
            output = f"\n\n\\section{{{self.title}}}\n"
        if self.content is not None:
            for element in self.content:
                if 'startDate' in element.keys():
                    output += f"\\cventry{{{datetime.strptime(element['startDate'], '%Y-%m-%d').strftime('%b %Y')}-"
                    if 'endDate' not in element.keys() or element['endDate'] == "":
                        output += "current}"
                    else:
                        output += datetime.strptime(element['endDate'], '%Y-%m-%d').strftime('%b %Y')+'}'
                else:
                    output += "\\cventry{}"
                output += f"{{{element['position']}}}{{{element['name']}}}{{}}{{}}{{{element['summary']}"
                if 'highlights' in element.keys():
                    output += "\n%\n%\n\\begin{itemize}"
                    for highlight in element['highlights']:
                        output += "\\item " + highlight + "\n"
                    output += "\\end{itemize}\n%\n}\n"
                else:
                    output += "}\n"

        if type(self.subsections) is list:
            for subsection in self.subsections:
                output += str(subsection)
        return output
