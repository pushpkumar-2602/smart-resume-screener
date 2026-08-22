import re
from app.parser.skills_list import KNOWN_SKILLS

def extract_skills(text: str) -> list[str]:
    """
    Checks the resume text for any known skill names.
    Returns a list of skills that were found (case-insensitive).
    """
    text_lower = text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_section(text: str, section_name: str) -> str:
    """
    Finds a section like 'EDUCATION' or 'EXPERIENCE' in the resume
    and returns the text until the next all-caps section header.
    """
    pattern = rf"{section_name}\s*\n(.*?)(?=\n[A-Z][A-Z ]{{3,}}\n|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()
    return ""
