from app.parser.pdf_extractor import extract_text_from_pdf
from app.matcher.embedding_matcher import compute_similarity, similarity_to_score

def test_matcher():
    resume_text = extract_text_from_pdf("data/resumes/sample_resume.pdf")

    jd_text = """
    We are looking for a Backend Engineer with experience in Python,
    FastAPI, SQL databases, and machine learning. Familiarity with
    Git and cloud platforms like AWS is a plus.
    """

    similarity = compute_similarity(resume_text, jd_text)
    score = similarity_to_score(similarity)

    print(f"Raw similarity: {similarity:.3f}")
    print(f"Match score (1-10): {score}")

if __name__ == "__main__":
    test_matcher()
