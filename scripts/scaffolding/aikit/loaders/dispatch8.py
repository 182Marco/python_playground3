from .base import Document
from .pdf import load_pdf
from .docx import load_docx
from .txt import load_txt
from pathlib import Path



def loader(path: str) -> list[Document]:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return load_pdf(path)
    if ext == ".docx":
        return load_docx(path)
    if ext == ".txt":
        return load_txt(path)
    raise ValueError(f"File non supportato: {ext}")