"""Pipeline d'extraction de données depuis des PDF via Structured Outputs."""

from pathlib import Path

import pdfplumber

from .llm_client import detect_document_type, extract_invoice_with_llm, extract_order_with_llm
from .models import ExtractedDocument, Invoice, Order


def _extract_text_from_pdf(path: Path) -> str:
    """Lit et concatène le texte de toutes les pages d'un PDF."""
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def extract_document(path: Path) -> ExtractedDocument:
    """Point d'entrée : détecte le type puis extrait via Structured Output.

    1. Lit le texte brut du PDF
    2. Détecte le type (order / invoice) via LLM
    3. Extrait les champs avec le schéma Pydantic correspondant
    4. Retourne un objet Order ou Invoice validé automatiquement
    """
    text = _extract_text_from_pdf(path)
    doc_type = detect_document_type(text)

    if doc_type == "invoice":
        invoice = extract_invoice_with_llm(text, Invoice)
        invoice.source_file = str(path)
        return invoice

    order = extract_order_with_llm(text, Order)
    order.source_file = str(path)
    return order

