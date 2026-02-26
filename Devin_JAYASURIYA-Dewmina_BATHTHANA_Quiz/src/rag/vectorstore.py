"""Vector store pour la recherche vectorielle en RAG."""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from sklearn.neighbors import NearestNeighbors

from ..llm.client import LLMClient


class VectorStore:
    """Store de vecteurs pour la recherche vectorielle (k-NN)."""

    def __init__(
        self,
        documents: List[Dict[str, Any]] = None,
        embedding_col: str = "embedding",
        model: str = "text-embedding-3-large",
        api_key: Optional[str] = None
    ):
        """
        Initialise le vector store.

        Args:
            documents: Liste de documents avec contenu et embeddings
            embedding_col: Nom de la colonne contenant les embeddings
            model: Modèle d'embedding à utiliser
            api_key: Clé API OpenAI
        """
        self.embedding_col = embedding_col
        self.model = model
        self.api_key = api_key
        self.client = LLMClient(api_key=api_key, model=model) if api_key else None

        # Stockage des documents
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray = np.array([])

        # Index k-NN
        self.nn_model = None

        if documents:
            self.add_documents(documents)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Ajoute des documents au vector store.

        Args:
            documents: Liste de documents avec champ 'text' et optionnellement 'embedding'
        """
        for doc in documents:
            # Créer un embedding si non fourni
            if self.embedding_col not in doc or doc[self.embedding_col] is None:
                if self.client:
                    doc[self.embedding_col] = self._create_embedding(doc.get("text", ""))
                else:
                    # Embedding par défaut (aléatoire pour les tests)
                    doc[self.embedding_col] = np.random.rand(3072).tolist()

            self.documents.append(doc)

        # Mettre à jour la matrice d'embeddings
        if self.documents:
            embeddings_list = [doc[self.embedding_col] for doc in self.documents]
            self.embeddings = np.array(embeddings_list, dtype=np.float32)

            # Entraîner le modèle k-NN
            self.nn_model = NearestNeighbors(n_neighbors=3, metric="cosine")
            self.nn_model.fit(self.embeddings)

    def _create_embedding(self, text: str) -> List[float]:
        """
        Crée un embedding pour un texte.

        Args:
            text: Texte à embedding

        Returns:
            Vector d'embedding
        """
        if self.client:
            try:
                response = self.client.client.embeddings.create(
                    model=self.model,
                    input=text
                )
                return response.data[0].embedding
            except Exception:
                return np.random.rand(3072).tolist()
        return np.random.rand(3072).tolist()

    def search(
        self,
        query: str,
        k: int = 3,
        min_score: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Recherche les documents les plus similaires à une query.

        Args:
            query: Query à rechercher
            k: Nombre de résultats à retourner
            min_score: Score minimum de similarité (0-1)

        Returns:
            Liste des documents pertinents avec scores
        """
        # Créer l'embedding de la query
        query_embedding = self._create_embedding(query)
        query_array = np.array([query_embedding], dtype=np.float32)

        # Recherche k-NN
        if self.nn_model is None:
            return []

        distances, indices = self.nn_model.kneighbors(query_array, n_neighbors=k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            # Convertir distance en score (1 - distance cosine)
            score = 1 - dist

            if score >= min_score and idx < len(self.documents):
                result = self.documents[idx].copy()
                result["score"] = score
                result["distance"] = dist
                results.append(result)

        # Trier par score décroissant
        results.sort(key=lambda x: x["score"], reverse=True)

        return results

    def batch_search(
        self,
        queries: List[str],
        k: int = 3,
        min_score: float = 0.5
    ) -> List[List[Dict[str, Any]]]:
        """
        Recherche multiple en batch.

        Args:
            queries: Liste de queries
            k: Nombre de résultats par query
            min_score: Score minimum

        Returns:
            Liste de listes de résultats
        """
        return [self.search(q, k, min_score) for q in queries]

    def clear(self) -> None:
        """Efface tous les documents."""
        self.documents = []
        self.embeddings = np.array([])
        self.nn_model = None

    def save(self, path: str) -> None:
        """
        Sauvegarde le vector store.

        Args:
            path: Chemin de sauvegarde
        """
        import json
        data = {
            "documents": self.documents,
            "embeddings": self.embeddings.tolist() if len(self.embeddings) > 0 else [],
            "embedding_col": self.embedding_col,
            "model": self.model
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

    def load(self, path: str) -> None:
        """
        Charge un vector store sauvegardé.

        Args:
            path: Chemin de chargement
        """
        import json
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.documents = data.get("documents", [])
        self.embedding_col = data.get("embedding_col", "embedding")
        self.model = data.get("model", "text-embedding-3-large")

        embeddings_list = data.get("embeddings", [])
        if embeddings_list:
            self.embeddings = np.array(embeddings_list, dtype=np.float32)
            self.nn_model = NearestNeighbors(n_neighbors=3, metric="cosine")
            self.nn_model.fit(self.embeddings)
