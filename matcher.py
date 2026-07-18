import re

# ==============================
# Master Skills Database
# ==============================

SKILLS = [
    "python","java","c","c++","javascript","typescript",
    "html","css","react","next.js","node.js","express",
    "mysql","postgresql","mongodb","firebase","sql",
    "git","github","docker","aws","azure","rest","api",
    "flutter","dart","django","flask","fastapi",
    "machine learning","deep learning","tensorflow",
    "pytorch","pandas","numpy","opencv",
    "redis","graphql","jwt","oauth",
    "postman","swagger","cloud"
]


# ==============================
# Name
# ==============================

def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if (
            len(line) > 3
            and len(line.split()) <= 4
            and "resume" not in line.lower()
            and "curriculum" not in line.lower()
        ):
            return line

    return "Unknown"


# ==============================
# Email
# ==============================

def extract_cgpa(text):

    # -------- CGPA /10 --------
    match = re.search(
        r'CGPA[:\s]*([0-9]\.?[0-9]?)',
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    match = re.search(
        r'([0-9]\.?[0-9]?)\s*/\s*10',
        text
    )

    if match:
        return float(match.group(1))

    # -------- Percentage --------
    match = re.search(
        r'([0-9]{2,3}\.?[0-9]?)\s*%',
        text
    )

    if match:
        percentage = float(match.group(1))
        return round(percentage / 9.5, 2)

    # -------- GPA /4 --------
    match = re.search(
        r'GPA[:\s]*([0-4]\.?[0-9]?)',
        text,
        re.IGNORECASE
    )

    if match:
        gpa = float(match.group(1))
        return round(gpa * 2.5, 2)

    match = re.search(
        r'([0-4]\.?[0-9]?)\s*/\s*4',
        text
    )

    if match:
        gpa = float(match.group(1))
        return round(gpa * 2.5, 2)

    return 0.0


# ==============================
# Skills
# ==============================

def extract_skills(text):

    found=[]

    lower=text.lower()

    for skill in SKILLS:

        if skill.lower() in lower:

            found.append(skill)

    return sorted(list(set(found)))


# ==============================
# Projects
# ==============================

def count_projects(text):

    keywords=[

        "project",

        "projects",

        "developed",

        "built",

        "implemented",

        "created",

        "designed"

    ]

    lower=text.lower()

    count=0

    for word in keywords:

        count+=lower.count(word)

    return count


# ==============================
# Parse Quality
# ==============================

def get_parse_quality(text):

    length = len(text.strip())

    words = len(text.split())

    if length == 0 or words < 20:
        return "🔴 Failed"

    elif words < 150:
        return "🟡 Partial"

    return "🟢 Clean"
def extract_college(text):

    patterns = [
        r'([A-Za-z ]+University)',
        r'([A-Za-z ]+College)',
        r'([A-Za-z ]+Institute)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return "Not Found"
def extract_degree(text):

    degrees = [
        "B.E",
        "B.Tech",
        "Bachelor of Engineering",
        "Bachelor of Technology",
        "Computer Science",
        "Information Science",
        "Artificial Intelligence",
        "Electronics"
    ]

    for degree in degrees:
        if degree.lower() in text.lower():
            return degree

    return "Not Found"
def extract_graduation_year(text):

    match = re.search(r'20(2[4-9]|3[0-5])', text)

    if match:
        return match.group()

    return "Not Found"
# ==============================
# Email
# ==============================

def extract_email(text):

    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    if match:
        return match.group()

    return ""
# ==============================
# Phone
# ==============================

def extract_phone(text):

    match = re.search(
        r'(\+91[\-\s]?)?[6-9]\d{9}',
        text
    )

    if match:
        return match.group()

    return ""