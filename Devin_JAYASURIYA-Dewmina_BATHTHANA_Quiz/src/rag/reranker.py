"""Reranker pour filtrer les résultats de recherche RAG."""

from typing import List, Dict, Any, Optional
from .vectorstore import VectorStore


class SimpleReranker:
    """Reranker simple basé sur le score de similarité."""

    def __init__(self, min_score: float = 0.6, max_results: int = 5):
        """
        Initialise le reranker.

        Args:
            min_score: Score minimum de similarité (0-1)
            max_results: Nombre max de résultats à conserver
        """
        self.min_score = min_score
        self.max_results = max_results

    def rerank(
        self,
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Filtre et reranke les résultats.

        Args:
            results: Liste de résultats de recherche

        Returns:
            Liste de résultats filtrés
        """
        # Filtrer par score
        filtered = [r for r in results if r.get("score", 0) >= self.min_score]

        # Trier par score décroissant
        filtered.sort(key=lambda x: x.get("score", 0), reverse=True)

        # Limiter le nombre de résultats
        return filtered[:self.max_results]

    def rerank_with_citations(
        self,
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Reranke et ajoute des citations.

        Args:
            results: Liste de résultats de recherche

        Returns:
            Dictionnaire avec résultats et métadonnées
        """
        filtered = self.rerank(results)

        # Déterminer le niveau de confiance
        if len(filtered) == 0:
            confidence = "basse"
        elif all(r.get("score", 0) >= 0.8 for r in filtered):
            confidence = "haute"
        else:
            confidence = "moyenne"

        return {
            "results": filtered,
            "citations": [
                {
                    "id": i + 1,
                    "source": r.get("source", "inconnu"),
                    "score": r.get("score", 0)
                }
                for i, r in enumerate(filtered)
            ],
            "confidence": confidence,
            "count": len(filtered)
        }


class LLMReranker:
    """Reranker utilisant un LLM pour évaluer la pertinence."""

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: Optional[str] = None
    ):
        """
        Initialise le LLM reranker.

        Args:
            model: Modèle LLM à utiliser
            api_key: Clé API OpenAI
        """
        from ..llm.client import LLMClient
        self.client = LLMClient(api_key=api_key, model=model)

    def rerank(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Reranke les résultats avec LLM.

        Args:
            query: Query originale
            results: Liste de résultats

        Returns:
            Liste de résultats rerankés
        """
        if not results:
            return []

        # Construire le prompt
        results_text = "\n\n".join([
            f"Resultat {i+1}:\nSource: {r.get('source', 'N/A')}\nContenu: {r.get('text', '')[:500]}"
            for i, r in enumerate(results)
        ])

        prompt = f"""Réévalue la pertinence des résultats suivants pour la requête: "{query}"

        Classe-les de plus pertinent à moins pertinent.
        Fournis un score de pertinence (0-100) pour chaque résultat.

        Retourne en JSON:
        {{
            "reranked": [
                {{
                    "original_index": 0,
                    "score": 95,
                    "relevance_reason": "Pourquoi pertinent"
                }}
            ]
        }}

        RESULTATS:
        {results_text}
        """

        try:
            response = self.client.generate(
                prompt=prompt,
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            import json
            result = json.loads(response)
            reranked = result.get("reranked", [])

            # Remettre les documents dans l'ordre
            ordered = []
            for r in reranked:
                idx = r.get("original_index", 0)
                if idx < len(results):
                    doc = results[idx].copy()
                    doc["rerank_score"] = r.get("score", 0) / 100
                    doc["relevance_reason"] = r.get("relevance_reason", "")
                    ordered.append(doc)

            return ordered

        except Exception:
            # Fallback: retourner les résultats originaux
            return results


def create_reranker(type: str = "simple", **kwargs) -> SimpleReranker | LLMReranker:
    """
    Factory pour créer un reranker.

    Args:
        type: Type de reranker ("simple" ou "llm")
        **kwargs: Paramètres du reranker

    Returns:
        Instance de reranker
    """
    if type == "simple":
        return SimpleReranker(**kwargs)
    elif type == "llm":
        return LLMReranker(**kwargs)
    else:
        raise ValueError(f"Type de reranker inconnu: {type}")
