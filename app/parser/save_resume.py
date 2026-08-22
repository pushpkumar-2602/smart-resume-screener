import hashlib
from app.parser.pdf_extractor import extract_text_from_pdf
from app.parser.structured_extractor import extract_skills, extract_section
from app.models.resume import Resume, Session

def compute_content_hash(text: str) -> str:
    """
    Produces a unique fingerprint of the resume's text.
    Identical resume content always produces the same hash,
    which lets us detect duplicates.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def process_and_save_resume(pdf_path: str, filename: str) -> int:
    """
    Full pipeline: reads a PDF, extracts skills/education,
    checks for duplicates, saves to the database if new,
    and returns the resume's id either way.
    """
    text = extract_text_from_pdf(pdf_path)
    content_hash = compute_content_hash(text)

    session = Session()

    existing = session.query(Resume).filter_by(content_hash=content_hash).first()
    if existing:
        existing_id = existing.id
        session.close()
        return existing_id

    skills = extract_skills(text)
    education = extract_section(text, "EDUCATION")

    resume = Resume(
        filename=filename,
        raw_text=text,
        skills=", ".join(skills),
        education=education,
        content_hash=content_hash,
    )
    session.add(resume)
    session.commit()
    resume_id = resume.id
    session.close()

    return resume_id
