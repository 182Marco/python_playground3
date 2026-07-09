"""Il "primo giro" — la demo guida del docente (CANOVACCIO: si scrive dal vivo).

⚠️ Questo file è volutamente quasi vuoto: si riempie DURANTE la demo, non prima.

Un solo file, tutto il metodo del giorno. Il docente lo costruisce a schermo su
`faq_prodotto.html`; tu replica pure qui mentre guardi. Nel Lab 1 applicherai
lo stesso ciclo a tutto il dataset (`triage.py`).

    python primo_giro.py
"""
import sys
from pathlib import Paths
sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import load

PATH = Path(__file__).parent.parent / "dataset" / "faq_prodotto.html"

# 1 · CARICA
docs = load(str(PATH))


# 2 · GUARDA — mai fidarsi del "nessun errore": quanti caratteri? che aspetto ha?
testo = "\n".join(d.text for d in docs)
print("___ inizio testo___\n")
print(testo[:400])
print("\n___ testo interrotto___")

# 3 · DIAGNOSTICA — che cosa c'è nell'output che NON vorresti dare al chatbot?


# 4 · CORREGGI — un primo fix mirato (quello sistematico è il Lab 2)
senza_cookies = "\n".join(l for l in testo.split() if "cookie" not in l.lower())
print(f"Dopo il primo fix: {len(senza_cookie)} caratteri")
print(f"con cookie: {len(testo)} - senza:{len(senza_cookie)}")