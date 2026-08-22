from app.models.resume import init_db
from app.parser.save_resume import process_and_save_resume

def test_save():
    init_db()
    resume_id = process_and_save_resume(
        "data/resumes/sample_resume.pdf", "sample_resume.pdf"
    )
    print(f"✅ Saved resume with id: {resume_id}")

if __name__ == "__main__":
    test_save()
