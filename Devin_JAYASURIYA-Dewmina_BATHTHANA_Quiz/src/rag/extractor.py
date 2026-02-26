"""Module RAG pour l'extraction d'information des documents."""

import json
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..llm.client import LLMClient


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Découpe un texte en chunks avec chevauchement.

    Args:
        text: Texte à découper
        chunk_size: Taille max d'un chunk (en caractères)
        overlap: Chevauchement entre chunks

    Returns:
        Liste des chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(text):
            break

        start += chunk_size - overlap

    return chunks


def chunk_by_sentences(text: str, sentences_per_chunk: int = 5) -> List[str]:
    """
    Découpe un texte en chunks par phrases.

    Args:
        text: Texte à découper
        sentences_per_chunk: Nombre de phrases par chunk

    Returns:
        Liste des chunks
    """
    import re
    # Split sur . ! ?
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = []

    for sentence in sentences:
        current_chunk.append(sentence)
        if len(current_chunk) >= sentences_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return [c for c in chunks if c.strip()]


class RAGExtractor:
    """Extracteur d'information utilisant la RAG."""

    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        """
        Initialise l'extracteur RAG.

        Args:
            model: Modèle LLM à utiliser
            api_key: Clé API OpenAI
        """
        self.client = LLMClient(api_key=api_key, model=model)
        self.model = model
        self.embeddings_cache: Dict[str, List[float]] = {}

    def extract_key_concepts(self, text: str, num_concepts: int = 10) -> List[Dict[str, Any]]:
        """
        Extrait les concepts clés d'un texte.

        Args:
            text: Texte à analyser
            num_concepts: Nombre de concepts à extraire

        Returns:
            Liste des concepts avec descriptions
        """
        # Découper le texte
        chunks = chunk_text(text, chunk_size=3000)
        combined_text = "\n---\n".join(chunks[:3])  # Limiter à 3 chunks

        prompt = f"""Analysez le texte suivant et extrayez les {num_concepts} concepts clés les plus importants.
        Pour chaque concept, fournissez:
        1. Le nom du concept
        2. Une courte définition (1-2 phrases)
        3. Son importance (haute, moyenne, basse)

        Retournez le résultat en JSON avec ce format:
        {{
            "concepts": [
                {{
                    "name": "Nom du concept",
                    "definition": "Définition",
                    "importance": "haute/moyenne/basse"
                }}
            ]
        }}

        TEXTE À ANALYSER:
        {combined_text}
        """

        response = self.client.generate(
            prompt=prompt,
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        try:
            result = json.loads(response)
            return result.get("concepts", [])
        except json.JSONDecodeError:
            return self._default_concepts(text, num_concepts)

    def _default_concepts(self, text: str, num_concepts: int) -> List[Dict[str, Any]]:
        """Fallback pour extraire des concepts si JSON échoue."""
        # Extraire les mots en capital comme concepts
        import re
        concepts_found = set()
        pattern = r'\b[A-Z][A-Z_]+\b'
        for match in re.finditer(pattern, text):
            concepts_found.add(match.group())
            if len(concepts_found) >= num_concepts:
                break

        return [
            {
                "name": concept,
                "definition": f"Terme important dans le document",
                "importance": "haute"
            }
            for concept in list(concepts_found)[:num_concepts]
        ]

    def extract_detailed_information(
        self,
        text: str,
        concepts: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extrait des informations détaillées sur les concepts.

        Args:
            text: Texte à analyser
            concepts: Liste des concepts à détailler

        Returns:
            Dictionnaire avec informations détaillées
        """
        if concepts is None:
            concept_list = self.extract_key_concepts(text)
            concepts = [c["name"] for c in concept_list]

        chunks = chunk_text(text, chunk_size=3000)
        combined_text = "\n---\n".join(chunks[:3])

        details = {}

        for concept in concepts[:5]:  # Limiter à 5 concepts pour l'API
            prompt = f"""À partir du texte suivant, extrayez toutes les informations importantes concernant "{concept}".

            Fournissez:
            1. Définition claire
            2. Caractéristiques principales
            3. Exemples
            4. Contexte d'utilisation

            Retournez le résultat en JSON:
            {{
                "definition": "...",
                "characteristics": ["...", "...", "..."],
                "examples": ["...", "..."],
                "context": "..."
            }}

            TEXTE:
            {combined_text}
            """

            response = self.client.generate(
                prompt=prompt,
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            try:
                details[concept] = json.loads(response)
            except json.JSONDecodeError:
                details[concept] = {
                    "definition": "Information disponible dans le document",
                    "characteristics": [],
                    "examples": [],
                    "context": "N/A"
                }

        return details

    def generate_questions_from_chunks(
        self,
        chunks: List[str],
        num_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Génère des questions à partir de chunks de texte.

        Args:
            chunks: Liste des chunks de texte
            num_questions: Nombre de questions à générer par chunk

        Returns:
            Liste des questions générées
        """
        all_questions = []

        for chunk in chunks[:5]:  # Limiter à 5 chunks
            prompt = f"""À partir du texte suivant, générez exactement {num_questions} questions d'examen.
            
            Pour chaque question:
            1. Posez une question claire et spécifique
            2. Fournissez la réponse correcte
            3. Si c'est un QCM, créez 3 fausses réponses plausibles
            
            Retournez en JSON:
            {{
                "questions": [
                    {{
                        "text": "Question?",
                        "type": "qcm" ou "ouvert",
                        "correct_answer": "Réponse",
                        "options": ["Option1", "Option2", "Option3"],
                        "explanation": "Explication"
                    }}
                ]
            }}
            
            TEXTE:
            {chunk[:2000]}
            """

            response = self.client.generate(
                prompt=prompt,
                temperature=0.5,
                response_format={"type": "json_object"}
            )

            try:
                result = json.loads(response)
                all_questions.extend(result.get("questions", []))
            except json.JSONDecodeError:
                pass

        return all_questions[:num_questions]
