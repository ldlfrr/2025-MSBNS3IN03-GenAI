## Projet NAF_ISB – Extracteur de Données Structurées

Ce projet est un **extracteur de données structurées** (sujet H5 du cours MSBNS3IN03 IA Générative).
Il vise à transformer des documents non structurés (par ex. factures, formulaires) en **données JSON** prêtes à être exploitées en data science.

### Objectifs

- **Reconnaître** différents types de documents (ex. facture, formulaire simple).
- **Extraire** les champs pertinents (ex. date, montant TTC, fournisseur, lignes de facture).
- **Valider et normaliser** les données extraites (formats de dates, numéros, montants).
- **Exporter** les résultats dans un format **JSON structuré** (et éventuellement CSV).

### Installation

1. Se placer à la racine du dépôt cloné :

```bash
cd "c:\Users\Nacim\Projet IA Generative\Projet_AgentMCP_NAF_ISB"
```

2. Créer et activer un environnement virtuel (ex. Python 3.11) :

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Installer les dépendances du projet :

```bash
pip install --upgrade pip
pip install -r NAF_ISB/requirements.txt
```

### Utilisation rapide

Une fois l’environnement installé, vous pourrez lancer une première extraction (prototype) avec :

```bash
cd NAF_ISB
python -m src.main --input "data/input/mon_fichier.pdf" --output "data/output/resultat.json"
```

> Cette commande sera ajustée au fur et à mesure que l’API d’extraction sera définie (schéma JSON final, types de documents supportés, etc.).

### Structure du projet

```text
NAF_ISB/
|-- README.md
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- src/
|   |-- __init__.py
|   |-- main.py
|-- data/
|   |-- input/
|   |-- output/
|-- tests/
|-- docs/
|-- slides/
```

Les sous-dossiers `tests`, `docs` et `slides` seront remplis au fur et à mesure du développement.

