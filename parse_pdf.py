from pdfminer.high_level import extract_text
import re

def parse_pdf(path: str) -> str:
    raw = extract_text(path)
    text = re.sub(r"\bPage \d+ of \d+\b", "", raw)
    text = re.sub(r"\s{3,}", " ", text)
    return text.strip()
