import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Opens a PDF file and pulls out all the readable text.
    Returns one big string containing everything found.
    """
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    return full_text
