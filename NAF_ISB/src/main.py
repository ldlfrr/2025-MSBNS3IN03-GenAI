"""Point d'entrée – extraction de documents PDF en JSON."""

import json
import sys
from pathlib import Path

try:
    from .extractors import extract_document
except ImportError:
    from extractors import extract_document

INPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "input"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "output"


def process_one(pdf_path: Path, output_path: Path) -> None:
    """Traite un PDF : détection du type, extraction, écriture JSON."""
    print(f"\n--- Traitement : {pdf_path.name} ---")

    document = extract_document(pdf_path)
    print(f"  Type détecté : {document.document_type}")

    result = document.model_dump(mode="json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"  OK → {output_path}")


def main() -> None:
    """Traite tous les PDF de data/input/ ou un chemin passé en argument."""
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if target.is_dir():
            pdf_files = sorted(target.glob("*.pdf"))
        elif target.is_file() and target.suffix.lower() == ".pdf":
            pdf_files = [target]
        else:
            print(f"Erreur : '{target}' n'est ni un fichier PDF ni un dossier.")
            sys.exit(1)
    else:
        pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        print("Aucun fichier PDF trouvé.")
        sys.exit(0)

    print(f"=== NAF_ISB – {len(pdf_files)} fichier(s) à traiter ===")

    ok, ko = 0, 0
    for pdf in pdf_files:
        out = OUTPUT_DIR / (pdf.stem + ".json")
        try:
            process_one(pdf, out)
            ok += 1
        except Exception as exc:
            print(f"  ERREUR sur {pdf.name} : {exc}")
            ko += 1

    print(f"\n=== Résumé : {ok} réussi(s), {ko} erreur(s) ===")


if __name__ == "__main__":
    main()


