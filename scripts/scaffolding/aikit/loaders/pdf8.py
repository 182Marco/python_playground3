from pypdf import PdfReader
from .base import Document

def load_pdf(path:str) -> list[Document]:
    docs= []
    pages = PdfReader(path).pages
    for i, p in enumerate(pages):
        txt = p.extract_text()
        docs.append(Document(txt, {"source": path, "type": "pdf", "page": i + 1 }))
    return docs
