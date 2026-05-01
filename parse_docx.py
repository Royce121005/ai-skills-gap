from docx import Document

def parse_docx(path: str) -> str:
    doc = Document(path)
    return " ".join(p.text for p in doc.paragraphs if p.text.strip())