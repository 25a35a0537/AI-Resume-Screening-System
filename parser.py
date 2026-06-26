import fitz
import re

# Supported Skills
SKILLS = [
    "Python", "Java", "C", "C++", "HTML", "CSS", "JavaScript",
    "Flask", "Django", "React", "Node.js", "SQL", "MySQL",
    "MongoDB", "Bootstrap", "Git", "GitHub", "Machine Learning",
    "Data Science", "AI", "Pandas", "NumPy", "TensorFlow",
    "PyTorch", "Linux"
]


def extract_text(pdf_path):

    text = ""

    pdf = fitz.open(pdf_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def find_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:

            if not any(word.lower() in line.lower() for word in
                       ["resume", "curriculum", "vitae", "email", "@"]):

                return line

    return "Unknown"


def find_email(text):

    email = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    if email:
        return email.group()

    return ""


def find_phone(text):

    phone = re.search(
        r'(\+91[\s-]?)?[6-9]\d{9}',
        text
    )

    if phone:
        return phone.group()

    return ""


def find_skills(text):

    found = []

    lower = text.lower()

    for skill in SKILLS:

        if skill.lower() in lower:
            found.append(skill)

    return sorted(list(set(found)))


def find_education(text):

    education = []

    keywords = [
        "B.Tech",
        "B.E",
        "Bachelor",
        "Diploma",
        "M.Tech",
        "MCA",
        "BCA",
        "Intermediate",
        "SSC"
    ]

    for line in text.split("\n"):

        for key in keywords:

            if key.lower() in line.lower():

                education.append(line.strip())

                break

    return education


def find_experience(text):

    exp = re.search(
        r'(\d+)\+?\s*(year|years|month|months)',
        text,
        re.I
    )

    if exp:
        return exp.group()

    return "Fresher"


def extract_resume_data(pdf_path):

    text = extract_text(pdf_path)

    return {

        "name": find_name(text),

        "email": find_email(text),

        "phone": find_phone(text),

        "skills": find_skills(text),

        "education": find_education(text),

        "experience": find_experience(text)

    }