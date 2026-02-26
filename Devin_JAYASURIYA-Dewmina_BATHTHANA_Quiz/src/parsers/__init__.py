# Parseurs de documents pour le Générateur de Quiz
"""Module de parsing de documents pour extraire le contenu."""

# Import conditionnel pour éviter les erreurs avec python-docx sur Windows
try:
    from .base_parser import BaseParser
except ImportError:
    pass

__all__ = ["BaseParser"]
