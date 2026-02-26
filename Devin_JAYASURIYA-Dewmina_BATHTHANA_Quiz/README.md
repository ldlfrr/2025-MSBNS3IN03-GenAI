# Générateur de Quiz - Devin JAYASURIYA & Dewmina BATHTHANA

**Projet MSBNS3IN03 - Intelligence Artificielle Générative (2025-2026)**

## 📋 Description

Outil complet d'automatisation de création de quiz utilisant l'IA générative (RAG + IRT):

- ✅ Parser multiples formats (PDF, DOCX, PPTX, TXT, Markdown)
- ✅ Extraction RAG de concepts clés
- ✅ Génération de questions calibrées par difficulté
- ✅ Création de distracteurs plausibles
- ✅ Corrections détaillées avec explications
- ✅ Export multi-formats (JSON, Markdown, Anki, Quizlet)

---

## Architecture Technique

```
Devin_JAYASURIYA-Dewmina_BATHTHANA_Quiz/
├── src/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée CLI
│   ├── config.py            # Configuration
│   ├── parsers/             # Parseurs de documents
│   │   ├── __init__.py
│   │   ├── base_parser.py
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   ├── pptx_parser.py
│   │   └── text_parser.py
│   ├── generators/          # Générateurs de quiz
│   │   ├── __init__.py
│   │   ├── base_generator.py
│   │   └── quiz_generator.py
│   └── llm/                 # Integration LLM
│       ├── __init__.py
│       └── client.py
├── tests/                   # Tests unitaires
├── docs/                    # Documentation
├── .env.example             # Template variables d'environnement
├── requirements.txt
└── README.md
```

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- Git
- Une clé API OpenAI (ou Anthropic)

### Étapes

1. Cloner le dépôt:
```bash
git clone <votre-fork-url>
cd Devin_JAYASURIYA-Dewmina_BATHTHANA_Quiz
```

2. Créer un environnement virtuel:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances:
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement:
```bash
cp .env.example .env
# Editez .env avec vos clés API
```

---

## Utilisation

### Ligne de commande

#### Générer un quiz à partir d'un document

```bash
python -m src.main generate document.pdf
```

Options disponibles:
- `-o, --output`: Dossier de sortie (par défaut: ./output)
- `-f, --format`: Format de sortie (json, markdown, anki, quizlet)
- `-n, --num-questions`: Nombre de questions à générer
- `-t, --question-type`: Type de questions (qcm, ouvert, mixed)
- `-d, --difficulty`: Difficulté cible (1-5)

#### Exemples d'utilisation

Générer un quiz QCM avec 10 questions:
```bash
python -m src.main generate cours.pdf -n 10 -t qcm
```

Générer un quiz mixte et l'exporter en Markdown:
```bash
python -m src.main generate cours.pdf -t mixed -f markdown
```

Générer un quiz pour Anki:
```bash
python -m src.main generate cours.pdf -f anki
```

#### Afficher la configuration
```bash
python -m src.main config
```

---

## Notebooks de Référence

Ce projet s'appuie sur les notebooks suivants du cours:

| Notebook | Description |
|----------|-------------|
| [GenAI/Texte/5_RAG_Modern.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/5_RAG_Modern.ipynb) | Extraction d'information |
| [GenAI/Texte/3_Structured_Outputs.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Structuration des quiz |
| [Probas/Infer/Infer-5-Skills-IRT.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Probas/Infer/Infer-5-Skills-IRT.ipynb) | Item Response Theory pour calibration de difficulté |

---

## References Externes

- [Quizlet AI](https://quizlet.com/) - Exemple de plateforme
- [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom%27s_taxonomy) - Niveaux cognitifs
- [Computerized Adaptive Testing](https://en.wikipedia.org/wiki/Computerized_adaptive_testing) - Tests adaptatifs

---

## Développement

### Lancer les tests
```bash
pytest tests/
```

### Avec couverture
```bash
pytest --cov=src tests/
```

### Formatage du code
```bash
black src/
ruff check src/
```

---

## Calendrier du Projet

| Etape | Date | Statut |
|-------|------|--------|
| Initialisation | 24 février 2026 | Terminé |
| Parsing de documents | A venir | |
| Génération de quiz | A venir | |
| Tests et validation | A venir | |
| Documentation | A venir | |
| Soumission PR | 25 février 2026 | |
| Soutenance | 27 février 2026 | |

---

## Auteurs

- Devin JAYASURIYA
- Dewmina BATHTHANA

---

## License

Ce projet est soumis aux memes conditions que le depot parent.
