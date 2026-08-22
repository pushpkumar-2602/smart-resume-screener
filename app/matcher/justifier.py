import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"

def generate_justification(resume_text: str, jd_text: str, match_result: dict) -> str:
    """
    Asks the local LLM to explain, in plain English, why the resume
    got the score it did — grounded in the skills we already matched,
    not left to invent its own opinion.
    """
    matched = ", ".join(match_result["matched_skills"]) or "none of the JD's key skills"

    prompt = f"""You are helping a recruiter understand a candidate match score.

Score: {match_result['score']}/10
Skills matched from the job description: {matched}

Write a short, 2-3 sentence justification for this score, based only on
the matched skills above. Do not invent skills or experience not listed.

Justification:"""

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
    )
    response.raise_for_status()
    return response.json()["response"].strip()
