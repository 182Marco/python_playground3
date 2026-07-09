from pypdf import PdfReader
from .base import Document

def load_pdf(path: str) -> list[Document]:
    pages = PdfReader(path).pages
    docs = []
    for i, page in enumerate(pages):
        text = page.extract_text() or ""
        docs.append(Document(
            text=text, 
            metadata={"source": path, "type": "pdf", "page": i +1}
        ))
    return docs
