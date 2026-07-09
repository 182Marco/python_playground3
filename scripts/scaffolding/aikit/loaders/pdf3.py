from pypdf import PdfReader
from .base import Document

def load_pdf(path: str) -> list[Document]:
    docs = []
    pages = PdfReader(path).pages
    for i, page in enumerate(pages):
        text = page.extract_text()
        docs.append(
            Document(
                text=text,
                metadata={
                    "page": i +1,
                    "type": "pdf",
                    "source": path
                }
            )
        )
    return docs