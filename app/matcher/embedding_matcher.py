from sentence_transformers import SentenceTransformer, util

# Loading the model takes a few seconds — we do it once, not per-call
_model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(resume_text: str, jd_text: str) -> float:
    """
    Converts both texts into embeddings and measures how similar
    they are. Returns a value roughly between 0 and 1.
    """
    resume_embedding = _model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = _model.encode(jd_text, convert_to_tensor=True)

    similarity = util.cos_sim(resume_embedding, jd_embedding)
    return float(similarity[0][0])


def similarity_to_score(similarity: float) -> int:
    """
    Converts a 0-1 similarity value into a 1-10 score,
    matching the brief's requested scale.
    """
    score = round(similarity * 10)
    return max(1, min(10, score))  # clamp between 1 and 10
