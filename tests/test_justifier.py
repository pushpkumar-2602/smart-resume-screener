from app.parser.pdf_extractor import extract_text_from_pdf
from app.matcher.scorer import compute_match_score
from app.matcher.justifier import generate_justification

def test_justifier():
    resume_text = extract_text_from_pdf("data/resumes/sample_resume.pdf")

    jd_text = """
    We are looking for a Backend Engineer with experience in Python,
    FastAPI, SQL databases, and machine learning. Familiarity with
    Git and cloud platforms like AWS is a plus.
    """

    result = compute_match_score(resume_text, jd_text)
    justification = generate_justification(resume_text, jd_text, result)

    print(f"Score: {result['score']}/10")
    print(f"Justification: {justification}")

if __name__ == "__main__":
    test_justifier()
