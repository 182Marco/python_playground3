"""check_lab18.py — verifica [OK]/[FAIL] per requisito.

Da lanciare dalla cartella scripts/:

    python scaffolding/check_lab18.py               # verifica working/ (istantanea, zero crediti)
    python scaffolding/check_lab18.py --live        # in più: un parse VERO via LlamaParse (~6 crediti)
    python scaffolding/check_lab18.py --solutions   # verifica solutions/ (per il docente)

La verifica base non chiama nessun servizio: è istantanea e deterministica,
quindi si lancia a ogni salvataggio. Il giro reale sta dietro --live.
"""
import os
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
DATASET = SCRIPTS / "dataset"
TARGET = SCRIPTS / ("solutions" if "--solutions" in sys.argv else "working")

sys.path.insert(0, str(Path(__file__).parent))   # aikit (scaffolding/)
sys.path.insert(0, str(TARGET))                  # triage, llamaparse, pulisci_corpus

CANDIDATI_LLAMAPARSE = {
    "verbale_scansionato.pdf", "fattura_scansionata.pdf", "rassegna_stampa.pdf",
    "listino_prezzi.pdf", "contratto_fornitura.docx",
}

FALLIMENTI = 0


def esito(ok: bool, msg: str) -> None:
    global FALLIMENTI
    print(("[OK]  " if ok else "[FAIL]") + " " + msg)
    if not ok:
        FALLIMENTI += 1


def check_triage() -> None:
    print("\n— Lab 1 · triage.py")
    try:
        import triage
        risultati = triage.triage_dataset()
    except NotImplementedError as e:
        esito(False, f"triage non ancora implementato ({e})")
        return
    except Exception as e:
        esito(False, f"triage_dataset() solleva {type(e).__name__}: {e}")
        return

    attesi = {p.name for p in DATASET.iterdir()}
    esito(set(risultati) == attesi,
          f"il triage copre tutti i {len(attesi)} file del dataset")

    def stato(nome):
        return risultati.get(nome, ("?", "", ""))[0]

    esito(stato("report_trimestrale.pdf") == "ERRORE",
          "il PDF corrotto è classificato ERRORE (e non fa crashare il triage)")
    scansioni = ("verbale_scansionato.pdf", "fattura_scansionata.pdf",
                 "rassegna_stampa.pdf")
    esito(all(stato(s) == "VUOTO" for s in scansioni),
          "le 3 scansioni sono classificate VUOTO (0 testo estratto)")
    esito(stato("note_interne.txt") == "OK",
          "il .txt latin-1 è OK: l'encoding è gestito (carica_robusto)")
    esito(stato("guida_smartworking.pdf") == "OK",
          "il PDF di testo è classificato OK")

    triage.scrivi_report(risultati)
    esito((TARGET / "triage.md").exists(), "la tabella di triage è scritta in triage.md")


def check_llamaparse() -> None:
    print("\n— LlamaParse · llamaparse.py")
    try:
        from llamaparse import TIERS, load_llamaparse
    except ImportError as e:
        esito(False, f"load_llamaparse non importabile: {e}")
        return

    esito(set(TIERS) == {"fast", "cost_effective", "agentic", "agentic_plus"},
          "TIERS elenca i 4 tier con i costi per pagina")

    try:
        load_llamaparse(str(DATASET / "listino_prezzi.pdf"), tier="turbo")
        esito(False, "un tier inesistente dovrebbe sollevare ValueError")
    except ValueError:
        esito(True, "tier inesistente → ValueError PRIMA di qualunque chiamata")
    except NotImplementedError as e:
        esito(False, f"load_llamaparse non ancora implementato ({e})")
    except Exception as e:
        esito(False, f"tier inesistente solleva {type(e).__name__} invece di ValueError")

    chiave_salvata = os.environ.pop("LLAMA_CLOUD_API_KEY", None)
    try:
        load_llamaparse(str(DATASET / "listino_prezzi.pdf"))
        esito(False, "senza chiave dovrebbe fermarsi con un messaggio chiaro")
    except SystemExit as e:
        esito("LLAMA_CLOUD_API_KEY" in str(e),
              "senza chiave si ferma SUBITO con un messaggio chiaro (niente rete)")
    except NotImplementedError as e:
        esito(False, f"load_llamaparse non ancora implementato ({e})")
    except Exception as e:
        esito(False, f"senza chiave solleva {type(e).__name__} invece di un errore chiaro")
    finally:
        if chiave_salvata is not None:
            os.environ["LLAMA_CLOUD_API_KEY"] = chiave_salvata


def check_pulisci() -> None:
    print("\n— Lab 2 · pulisci_corpus.py (offline: solo loader nativi)")
    try:
        import pulisci_corpus
    except Exception as e:
        esito(False, f"pulisci_corpus non importabile: {type(e).__name__}: {e}")
        return

    rotte = pulisci_corpus.ROUTING
    esito(CANDIDATI_LLAMAPARSE <= set(rotte),
          "ROUTING decide la rotta per tutti e 5 i file candidati (TODO 5)")
    valide = {"nativo", "fast", "cost_effective", "agentic", "agentic_plus"}
    esito(all(v in valide for v in rotte.values()),
          "ogni rotta è 'nativo' o un tier LlamaParse valido")
    esito(any(v != "nativo" for v in rotte.values()),
          "almeno un file passa da LlamaParse (le scansioni non si aggiustano gratis…)")

    chiave_salvata = os.environ.pop("LLAMA_CLOUD_API_KEY", None)   # forza l'offline
    try:
        righe = pulisci_corpus.pulisci()
        pulisci_corpus.scrivi_report(righe)
    except NotImplementedError as e:
        esito(False, f"pulisci_corpus non ancora implementato ({e})")
        return
    except Exception as e:
        esito(False, f"pulisci() solleva {type(e).__name__}: {e}")
        return
    finally:
        if chiave_salvata is not None:
            os.environ["LLAMA_CLOUD_API_KEY"] = chiave_salvata

    out = TARGET / "corpus_pulito"
    txt = list(out.glob("*.txt")) if out.exists() else []
    esito(len(txt) >= 8, f"corpus_pulito/ contiene i file puliti ({len(txt)}/8 attesi)")

    report = TARGET / "report.md"
    esito(report.exists() and "guida_smartworking" in report.read_text(encoding="utf-8"),
          "report.md esiste e contiene le metriche per file")

    faq = out / "faq_prodotto.txt"
    if faq.exists():
        pulito = faq.read_text(encoding="utf-8")
        import triage
        grezzo = "\n".join(d.text for d in triage.carica_robusto(str(DATASET / "faq_prodotto.html")))
        esito(len(pulito) < len(grezzo) and "cookie" not in pulito,
              "l'HTML è ripulito: più corto del grezzo e senza cookie banner")
        esito("garanzia" in pulito and "bambù" in pulito,
              "…ma il CONTENUTO è sopravvissuto (garanzia, materiali)")
    else:
        esito(False, "manca corpus_pulito/faq_prodotto.txt")


def check_live() -> None:
    print("\n— LIVE · parse veri via LlamaParse (~6 crediti)")
    if not os.getenv("LLAMA_CLOUD_API_KEY", "").strip():
        esito(False, "serve LLAMA_CLOUD_API_KEY nel .env per il check --live")
        return
    from llamaparse import load_llamaparse
    try:
        md = load_llamaparse(str(DATASET / "listino_prezzi.pdf"),
                             tier="cost_effective")[0].text
    except NotImplementedError as e:
        esito(False, f"load_llamaparse non ancora implementato ({e})")
        return
    esito("LD-200" in md and ("<td>" in md or "|" in md),
          "cost_effective: la tabella del listino torna RICOSTRUITA (celle strutturate)")


if __name__ == "__main__":
    print(f"verifico: {TARGET.name}/")
    check_triage()
    check_llamaparse()
    check_pulisci()
    if "--live" in sys.argv:
        check_live()
    print("\n" + ("Tutto a posto ✔" if FALLIMENTI == 0
                  else f"{FALLIMENTI} requisito/i ancora da sistemare."))
    sys.exit(0 if FALLIMENTI == 0 else 1)
