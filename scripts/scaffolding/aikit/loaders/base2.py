from dataclasses import dataclass, field

@dataclass
class Document:
    text: str
    metadata: dict = field(default_factory=dict) # per non avere un punto condiviso in memoria per ogni oggetto di quest' istanza

    def __repr__(self):
        anteprima = " ".join(self.text.split())[:60]
        return f"Document ({self.metadata}, text={anteprima!r}...)"
