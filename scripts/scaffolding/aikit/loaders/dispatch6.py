from .base import Document
from pathlib import Path
from .pdf import load_pdf
from .txt import load_txt
from .docx import load_docx




def loader(path: str) -> list[Document]:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return load_pdf(path)
    if ext == ".txt":
        return load_txt(path)
    if ext == ".docx":
        return load_docx(path)
    raise ValueError(f"Fromato non supportato: {ext}")