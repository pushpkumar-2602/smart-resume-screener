from app.parser.pdf_extractor import extract_text_from_pdf

def test_extraction():
    text = extract_text_from_pdf("data/resumes/sample_resume.pdf")
    assert len(text) > 0, "Extracted text should not be empty"
    print("✅ PDF extraction test passed")
    print(f"Extracted {len(text)} characters")

if __name__ == "__main__":
    test_extraction()
