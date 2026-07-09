from .base import Document


def load_txt(path: str) -> list[Document]:
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    return [Document(txt, {"source": path, "type": "txt"})]