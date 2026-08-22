from app.parser.pdf_extractor import extract_text_from_pdf
from app.parser.structured_extractor import extract_skills, extract_section

def test_extraction():
    text = extract_text_from_pdf("data/resumes/sample_resume.pdf")

    skills = extract_skills(text)
    print(f"Skills found: {skills}")

    education = extract_section(text, "EDUCATION")
    print(f"Education section:\n{education}\n")

if __name__ == "__main__":
    test_extraction()
