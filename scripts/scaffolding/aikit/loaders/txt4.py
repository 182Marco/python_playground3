from .base import Document


def load_text(path: str) ->list[Document]:
    with open(path, encoding="utf-8") as t:
        text = t.read()
    return [Document(text, {"source": path, "type": "txt"})]