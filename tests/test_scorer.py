from app.parser.pdf_extractor import extract_text_from_pdf
from app.matcher.scorer import compute_match_score

def test_scorer():
    resume_text = extract_text_from_pdf("data/resumes/sample_resume.pdf")

    jd_text = """
    We are looking for a Backend Engineer with experience in Python,
    FastAPI, SQL databases, and machine learning. Familiarity with
    Git and cloud platforms like AWS is a plus.
    """

    result = compute_match_score(resume_text, jd_text)
    print(result)

if __name__ == "__main__":
    test_scorer()
