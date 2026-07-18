import matcher

ROLE_REQUIREMENTS = {

    "Frontend Developer": {
        "required": [
            "html","css","javascript","react","git","rest"
        ],
        "preferred": [
            "next.js","typescript","redux","jest"
        ],
        "slots": 8
    },

    "Backend Developer": {
        "required": [
            "python","java","node.js","sql",
            "mysql","postgresql","mongodb",
            "git","rest","api"
        ],
        "preferred": [
            "docker","jwt","oauth","aws","cloud"
        ],
        "slots":10
    },

    "Full Stack Developer": {
        "required":[
            "react","node.js","sql",
            "mongodb","firebase",
            "git","rest"
        ],
        "preferred":[
            "graphql","docker","aws","cloud"
        ],
        "slots":7
    },

    "Database Developer": {
        "required":[
            "mysql","postgresql","sql","mongodb"
        ],
        "preferred":[
            "redis","indexing"
        ],
        "slots":3
    },

    "API Integration Developer": {
        "required":[
            "api","rest","json","postman"
        ],
        "preferred":[
            "swagger","oauth","jwt"
        ],
        "slots":2
    }

}


def score_resume(text, role):

    info = ROLE_REQUIREMENTS.get(role)

    required = info["required"]
    preferred = info["preferred"]

    name = matcher.extract_name(text)
    email = matcher.extract_email(text)
    phone = matcher.extract_phone(text)
    cgpa = matcher.extract_cgpa(text)
    skills = matcher.extract_skills(text)
    projects = matcher.count_projects(text)
    parse_quality = matcher.get_parse_quality(text)
    college = matcher.extract_college(text)
    degree = matcher.extract_degree(text)
    graduation_year = matcher.extract_graduation_year(text)

    required_matches = []
    preferred_matches = []

    score = 0

    # -------------------
    # Required Skills (60)
    # -------------------

    if len(required):

        marks = 60 / len(required)

        for skill in required:

            if skill in skills:

                score += marks
                required_matches.append(skill)

    # -------------------
    # Preferred Skills (20)
    # -------------------

    if len(preferred):

        marks = 20 / len(preferred)

        for skill in preferred:

            if skill in skills:

                score += marks
                preferred_matches.append(skill)

    # -------------------
    # CGPA (10)
    # -------------------

    if cgpa >= 8.5:
        score += 10

    elif cgpa >= 7.5:
        score += 8

    elif cgpa >= 6.5:
        score += 6

    elif cgpa >= 6:
        score += 4

    # -------------------
    # Projects (10)
    # -------------------

    if projects >= 4:
        score += 10

    elif projects == 3:
        score += 8

    elif projects == 2:
        score += 6

    elif projects == 1:
        score += 3

    score = min(round(score),100)

    # -------------------
    # Confidence
    # -------------------

    if parse_quality == "🔴 Failed":
        confidence = "🔴 Low"

    elif score >= 80:
        confidence = "🟢 High"

    elif score >= 60:
        confidence = "🟡 Medium"

    else:
        confidence = "🔴 Low"

    # -------------------
    # Reason
    # -------------------

    reason = []

    if required_matches:
        reason.append(
            f"✔ Required Skills : {len(required_matches)}"
        )

    if preferred_matches:
        reason.append(
            f"✔ Preferred Skills : {len(preferred_matches)}"
        )

    reason.append(
        f"✔ CGPA : {cgpa}"
    )

    reason.append(
        f"✔ Projects : {projects}"
    )

    return {

    "Name": name,

    "Email": email,

    "Phone": phone,

    "College": college,

    "Degree": degree,

    "Graduation Year": graduation_year,

    "CGPA": cgpa,

        "Skills": ", ".join(skills),

        "Projects": projects,

        "Score": score,

        "Confidence": confidence,

        "Parse Quality": parse_quality,

        "Required Skills": ", ".join(required_matches),

        "Preferred Skills": ", ".join(preferred_matches),

        "Reason": "\n".join(reason),

        "Status": "Reserve"

    }