from pypdf import PdfReader
from .base import Document


def pdf_load(path: str) -> list[Document]:
    docs = []
    pages = PdfReader(path).pages
    for i, page in enumerate(pages):
        txt = page.extract_text()
        docs.append(Document(txt, {"source": path, "type": "pdf", "page": i +1}))
    return docs