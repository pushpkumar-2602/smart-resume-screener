import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Resume Screener", layout="wide")

st.title("📄 Smart Resume Screener")
st.write("Upload resumes and match them against a job description.")

st.header("1. Upload a Resume")
uploaded_file = st.file_uploader("Choose a PDF resume", type="pdf")

if uploaded_file is not None:
    if st.button("Upload and Process"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_URL}/resumes/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Uploaded! Resume ID: {data['resume_id']}")
        else:
            st.error(f"Upload failed: {response.text}")

st.header("2. Match Against a Job Description")
jd_text = st.text_area("Paste the job description here", height=150)

if st.button("Find Matches"):
    if not jd_text.strip():
        st.warning("Please paste a job description first.")
    else:
        with st.spinner("Scoring resumes... this may take a moment (local LLM is thinking)"):
            response = requests.post(f"{API_URL}/match", json={"text": jd_text})

        if response.status_code == 200:
            results = response.json()["results"]

            if not results:
                st.info("No resumes found. Upload some first.")
            else:
                for r in results:
                    with st.container(border=True):
                        st.subheader(f"{r['filename']} — Score: {r['score']}/10")
                        st.write(f"**Matched skills:** {', '.join(r['matched_skills']) or 'None'}")
                        st.write(f"**Justification:** {r['justification']}")
        else:
            st.error(f"Matching failed: {response.text}")
