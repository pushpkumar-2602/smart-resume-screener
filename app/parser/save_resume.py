from app.parser.pdf_extractor import extract_text_from_pdf
from app.parser.structured_extractor import extract_skills, extract_section
from app.models.resume import Resume, Session

def process_and_save_resume(pdf_path: str, filename: str) -> int:
    """
    Full pipeline: reads a PDF, extracts skills/education,
    saves everything to the database, and returns the new row's id.
    """
    text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(text)
    education = extract_section(text, "EDUCATION")

    session = Session()
    resume = Resume(
        filename=filename,
        raw_text=text,
        skills=", ".join(skills),
        education=education,
    )
    session.add(resume)
    session.commit()
    resume_id = resume.id
    session.close()

    return resume_id
