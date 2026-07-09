from .base import Document
from pypdf import PdfReader


def load_pdf(path: str) -> list[Document]:
    docs = []
    pages = PdfReader(path).pages
    for i, page in enumerate(pages):
        txt = page.extract_text() or ""
        docs.append(Document(
            text=txt,
            metadata=(
                {
                    "source" : path,
                    "type" : "pdf",
                    "page" : i + 1
                }
            )
        ))
    return docs 


