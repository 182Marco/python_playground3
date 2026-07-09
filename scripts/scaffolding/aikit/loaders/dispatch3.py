from pathlib import Path
from base import Document
from .pdf import load_pdf

def loader(path: str) -> list[Document]:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return load_pdf(path)