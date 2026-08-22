# Smart Resume Screener

Parses PDF resumes, extracts skills and education, and scores candidates
against a job description using a hybrid of skill-matching and semantic
similarity — with a local LLM generating a plain-English justification
for each score.

## Architecture

```
[Streamlit Dashboard]  --HTTP-->  [FastAPI Backend]
                                        |
                    ------------------------------------------
                    |                   |                   |
                    v                   v                   v
            [PDF Parser]         [Matcher/Scorer]     [SQLite DB]
          (pdfplumber, regex)   (sentence-transformers  (SQLAlchemy)
                                  + local LLM via Ollama)
```

**Flow:**
1. User uploads a resume PDF via the dashboard (or directly via the API)
2. `pdfplumber` extracts raw text; regex-based section splitting and a
   known-skills list extract structured skills/education
3. A SHA-256 hash of the extracted text prevents duplicate uploads
4. Parsed data is saved to a local SQLite database
5. When a job description is submitted, every stored resume is scored
   against it and results are returned ranked highest-first

## Why a hybrid scoring approach (not pure LLM scoring)

The brief suggests asking an LLM directly to "rate fit 1-10." In practice,
small local models (needed here since no paid API is used) are inconsistent
at producing reliable numeric scores and can hallucinate skills that aren't
actually in the resume.

Instead, this project computes the score deterministically:

- **Skill overlap (60% weight):** what fraction of the JD's recognized
  skills are also present in the resume -- exact, reproducible, explainable
- **Semantic similarity (40% weight):** cosine similarity between
  sentence-transformer embeddings of the resume and JD, to capture
  broader contextual relevance beyond an exact skill list

The local LLM (`phi3:mini`, via Ollama) is used **only** to write a
natural-language justification for the already-computed score -- not to
decide the score itself. This keeps the numeric output trustworthy while
still using the LLM for what it's genuinely good at: fluent explanation.

## LLM prompt used

```
You are helping a recruiter understand a candidate match score.

Score: {score}/10
Skills matched from the job description: {matched_skills}

Write a short, 2-3 sentence justification for this score, based only on
the matched skills above. Do not invent skills or experience not listed.

Justification:
```

The prompt deliberately hands the LLM the already-computed score and
matched skills, rather than the raw resume and JD, to keep its output
grounded and prevent it from inventing its own judgment.

## Tech stack

- **Backend:** Python, FastAPI
- **Parsing:** pdfplumber, regex
- **Matching:** sentence-transformers (`all-MiniLM-L6-v2`) for semantic
  similarity, custom skill-overlap logic
- **LLM:** Ollama running `phi3:mini` locally (no paid API)
- **Database:** SQLite via SQLAlchemy
- **Frontend:** Streamlit

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Ollama and pull the model (macOS)
brew install ollama
brew services start ollama
ollama pull phi3:mini
```

## Running locally

You need two processes running at once, in separate terminals:

```bash
# Terminal 1 -- backend
python3 -m uvicorn app.main:app --reload

# Terminal 2 -- frontend
python3 -m streamlit run frontend/dashboard.py
```

Then open `http://localhost:8501` in your browser.

## API endpoints

- `POST /resumes/upload` -- upload a PDF resume (multipart form, field `file`)
- `POST /match` -- submit `{"text": "<job description>"}`, returns all
  stored resumes ranked by score with matched skills and justification

## Known limitations

- Skill extraction relies on a fixed known-skills list (`app/parser/skills_list.py`),
  so uncommon or newly-named skills won't be detected
- Section extraction (education, etc.) assumes reasonably standard resume
  formatting; heavily stylized or multi-column PDFs may parse imperfectly
- No authentication -- intended as a local/internal tool, not public-facing
