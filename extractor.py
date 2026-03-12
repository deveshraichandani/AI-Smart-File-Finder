import pdfplumber
from docx import Document

def extract_text(file_path):
    try:

        if file_path.endswith(".pdf"):
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text

        if file_path.endswith(".docx"):
            doc = Document(file_path)
            text = ""
            for p in doc.paragraphs:
                text += p.text + " "
            return text

        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

    except:
        return ""

    return ""