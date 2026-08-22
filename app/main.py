import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File

from app.models.resume import init_db
from app.parser.save_resume import process_and_save_resume

app = FastAPI(title="Smart Resume Screener")

RESUME_DIR = Path("data/resumes")
RESUME_DIR.mkdir(parents=True, exist_ok=True)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/resumes/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Accepts a PDF resume, saves it, parses it, stores it in the
    database, and returns the new resume's id.
    """
    save_path = RESUME_DIR / file.filename

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_id = process_and_save_resume(str(save_path), file.filename)

    return {"resume_id": resume_id, "filename": file.filename}


from pydantic import BaseModel
from app.models.resume import Session, Resume
from app.matcher.scorer import compute_match_score
from app.matcher.justifier import generate_justification

class JobDescription(BaseModel):
    text: str

@app.post("/match")
def match_resumes(jd: JobDescription):
    """
    Scores every stored resume against the given job description,
    returns them ranked highest-score first, with justifications.
    """
    session = Session()
    all_resumes = session.query(Resume).all()

    results = []
    for resume in all_resumes:
        match_result = compute_match_score(resume.raw_text, jd.text)
        justification = generate_justification(resume.raw_text, jd.text, match_result)

        results.append({
            "resume_id": resume.id,
            "filename": resume.filename,
            "score": match_result["score"],
            "matched_skills": match_result["matched_skills"],
            "justification": justification,
        })

    session.close()

    results.sort(key=lambda r: r["score"], reverse=True)
    return {"results": results}
