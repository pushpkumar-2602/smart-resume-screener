from app.parser.structured_extractor import extract_skills
from app.matcher.embedding_matcher import compute_similarity

def compute_skill_overlap(resume_text: str, jd_text: str) -> float:
    """
    Finds which skills mentioned in the JD are also in the resume.
    Returns the fraction matched, from 0.0 to 1.0.
    """
    jd_skills = set(extract_skills(jd_text))
    resume_skills = set(extract_skills(resume_text))

    if not jd_skills:
        return 0.0  # JD mentioned no skills we recognize, can't score this way

    matched = jd_skills & resume_skills  # set intersection: skills in both
    return len(matched) / len(jd_skills)


def compute_match_score(resume_text: str, jd_text: str) -> dict:
    """
    Combines skill overlap and semantic similarity into one 1-10 score.
    Returns a dict with the final score plus the individual signals,
    so we can show our work in the justification later.
    """
    skill_overlap = compute_skill_overlap(resume_text, jd_text)
    semantic_similarity = compute_similarity(resume_text, jd_text)

    combined = (skill_overlap * 0.6) + (semantic_similarity * 0.4)
    score = round(combined * 10)
    score = max(1, min(10, score))

    return {
        "score": score,
        "skill_overlap": round(skill_overlap, 2),
        "semantic_similarity": round(semantic_similarity, 2),
        "matched_skills": list(set(extract_skills(resume_text)) & set(extract_skills(jd_text))),
    }
