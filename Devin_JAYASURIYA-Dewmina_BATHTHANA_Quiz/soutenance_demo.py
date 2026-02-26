"""
SCRIPT DE SOUTENANCE - Générateur de Quiz avec PDFs réels

Démontre le système sur les 3 PDFs fournis:
1. Revolutions technologiques
2. Algorithmes
3. Photosynthèse
"""

import sys
import pandas
import io
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

from src.generators.quiz_generator import QuizGenerator
from PyPDF2 import PdfReader
from typing import List, Dict, Any


class SimplePdfParser:
    """Parser simple pour PDF sans dépendances externes problématiques."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def parse(self) -> List[Dict[str, Any]]:
        """Parse le PDF et retourne une liste de pages."""
        reader = PdfReader(self.file_path)
        pages_content = []

        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            pages_content.append({
                "page": page_num,
                "title": f"Page {page_num}",
                "content": text,
                "text": text
            })

        return pages_content


def test_pdf(pdf_path, num_questions=5, difficulty=3):
    """Teste la génération de quiz sur un PDF."""

    pdf_file = Path(pdf_path)
    print(f"\n{'='*70}")
    print(f"Processing: {pdf_file.name}")
    print('='*70)

    # Étape 1: Parser le PDF
    print(f"\nStep 1: Parsing PDF...")
    try:
        parser = SimplePdfParser(pdf_file)
        sections = parser.parse()
        print(f"  -> Found {len(sections)} pages/sections")

        if not sections:
            print(f"  -> WARNING: No content detected!")
            return None

    except Exception as e:
        print(f"  -> ERROR parsing: {e}")
        return None

    # Afficher un aperçu du contenu
    first_section = sections[0] if sections else {}
    content_preview = first_section.get('content', '')[:100]
    print(f"  -> Preview: \"{content_preview}...\"")

    # Étape 2: Générer le quiz
    print(f"\nStep 2: Generating quiz...")
    try:
        generator = QuizGenerator()
        # Passer les sections (dicts avec 'content') au générateur
        quiz = generator.generate_quiz_from_sections(
            sections,
            num_questions=num_questions,
            difficulty=difficulty
        )

        if not quiz or not quiz.get('questions'):
            print(f"  -> ERROR: No questions generated")
            return None

        print(f"  -> Generated {len(quiz.get('questions', []))} questions")

    except Exception as e:
        print(f"  -> ERROR generation: {e}")
        return None

    # Étape 3: Afficher les statistiques
    print(f"\nStep 3: Quiz statistics")
    questions = quiz.get('questions', [])

    # Compter par type
    types = {}
    for q in questions:
        qtype = q.get('type', 'unknown')
        types[qtype] = types.get(qtype, 0) + 1

    for qtype, count in types.items():
        print(f"  - {qtype.upper()}: {count} question(s)")

    # Difficultés
    if questions:
        difficulties = [q.get('difficulty', 3) for q in questions]
        avg_diff = sum(difficulties) / len(difficulties)
        print(f"  - Average difficulty: {avg_diff:.1f}/5")
        print(f"  - Range: {min(difficulties)}-{max(difficulties)}/5")

    # Étape 4: Export
    print(f"\nStep 4: Export to multiple formats")
    try:
        # JSON
        output_json = generator.export_quiz(quiz, format='json', output_path=Path('./output'))
        print(f"  - JSON: OK {output_json}")

        # Markdown
        output_md = generator.export_quiz(quiz, format='markdown', output_path=Path('./output'))
        print(f"  - Markdown: OK {output_md}")

    except Exception as e:
        print(f"  -> ERROR export: {e}")

    # Étape 5: Exemple de question
    print(f"\nStep 5: Sample question")
    if questions:
        q = questions[0]
        print(f"  Type: {q.get('type').upper()}")
        print(f"  Difficulty: {q.get('difficulty')}/5")
        print(f"  Q: {q.get('question')[:70]}...")
        print(f"  A: {q.get('correct_answer')[:70]}...")

    return quiz


def main():
    """Fonction principale - Soutenance."""

    print("\n")
    print("=" * 70)
    print("SOUTENANCE - GENERATEUR DE QUIZ IA")
    print("Devin JAYASURIYA & Dewmina BATHTHANA")
    print("25 fevrier 2026")
    print("=" * 70 + "\n")

    # Dossier des PDFs (basé sur le répertoire du script)
    script_dir = Path(__file__).parent
    docs_folder = script_dir / "docs"

    if not docs_folder.exists():
        print("ERROR: Dossier 'docs/' non trouve!")
        return

    # Chercher les PDFs
    pdf_files = list(docs_folder.glob("*.pdf"))

    if not pdf_files:
        print("ERROR: Aucun PDF trouve dans 'docs/'!")
        return

    print(f"Found {len(pdf_files)} PDF files:\n")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")

    # Tester chaque PDF
    print(f"\n{'='*70}")
    print("STARTING TESTS")
    print('='*70)

    # Générer 3-4 questions par document
    for i, pdf_file in enumerate(pdf_files, 1):
        num_q = 4 if i == 1 else 3  # 4 questions pour le premier, 3 pour les autres
        print(f"\n[{i}/{len(pdf_files)}] Generating {num_q} questions...")
        quiz = test_pdf(pdf_file, num_questions=num_q, difficulty=None)

    # Résumé final
    print(f"\n\n{'='*70}")
    print("FINAL SUMMARY")
    print('='*70 + "\n")

    # Résumé des résultats
    for pdf_name in [p.name for p in pdf_files]:
        output_json = Path(f"output/quiz_{pdf_name.replace('.pdf', '')}.json")
        output_md = Path(f"output/quiz_{pdf_name.replace('.pdf', '')}.md")
        if output_json.exists() or output_md.exists():
            print(f"  OK {pdf_name}")
        else:
            print(f"  ERROR {pdf_name}")

    print(f"\n{'='*70}")
    print("READY FOR SOUTENANCE!")
    print('='*70 + "\n")

    print("PRESENTATION SEQUENCE:\n")
    print("1. Oral presentation (3 min)")
    print("2. Run: python soutenance_demo.py (5-7 min)")
    print("3. Show output/quiz*.json (2 min)")
    print("4. Code walkthrough VS Code (2-3 min)")
    print("5. Q&A (2-3 min)")
    print()

    print("\nGenerated files:")
    for pdf_name in [p.name for p in pdf_files]:
        print(f"   - output/quiz_{pdf_name.replace('.pdf', '')}.json")
        print(f"   - output/quiz_{pdf_name.replace('.pdf', '')}.md")


if __name__ == "__main__":
    main()