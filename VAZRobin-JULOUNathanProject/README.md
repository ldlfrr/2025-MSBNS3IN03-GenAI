
# 🤖 AI Code Reviewer - Assistant de Revue de Code Intelligent

Ce projet a été réalisé par **Robin et Nathan** dans le cadre de nos études (E3). Il s'agit d'une application web complète conçue pour automatiser et enrichir le processus de **Code Review** (revue de code) sur GitHub grâce à l'Intelligence Artificielle.

**Description :** Analyser automatiquement le Diff d'une Pull Request GitHub pour suggérer des améliorations et détecter des bugs potentiels via un modèle d'IA générative avancé.

### 🎯 Objectifs du projet :

* **Parser** les diffs et Pull Requests depuis GitHub.
* **Détecter** les patterns problématiques et les failles de sécurité.
* **Suggérer** des améliorations avec des explications adaptées au développeur.
* **Vérifier** le respect des conventions de code et d'architecture.


## 📁 Architecture du Projet (Modèle-Vue-Contrôleur)

```text
projet-revieweur-ia/
├── app.py                # Point d'entrée, Serveur web Flask & Routes API (dont /api/chat)
├── requirements.txt      # Liste des dépendances Python
├── .env                  # Variables d'environnement secrètes (Clé API) - NON INCLUS
├── src/                  # Logique métier ("Cerveau" de l'application)
│   ├── config.py         # Chargement sécurisé de la configuration
│   ├── git_parser.py     # Communication avec l'API REST officielle de GitHub
│   └── ai_reviewer.py    # Logique IA, Prompts dynamiques, et gestion de la mémoire du Chat
└── templates/            # Vues (Interface Utilisateur / Frontend)
    ├── index.html        # Page principale : Extraction, Analyse et Chat interactif avec l'IA
    ├── login.html        # Page de connexion sécurisée
    ├── register.html     # Page d'inscription avec hachage de mot de passe
    └── historique.html   # Tableau de bord listant les anciennes analyses sauvegardées
```


---

## ⚙️ Plongée dans le Code : Méthodologies Utilisées

Ce projet repose sur une architecture MVC (Modèle-Vue-Contrôleur) robuste en Python/Flask. Voici le détail technique de notre implémentation :

### 1. Extraction des Données (`git_parser.py`)

Nous n'utilisons pas de librairie tierce complexe pour GitHub. Nous interrogeons directement l'**API REST officielle de GitHub** via le module `requests`.

* **Méthode clé :** Nous passons un header spécifique `"Accept": "application/vnd.github.v3.diff"` dans la requête HTTP. Cela permet de forcer l'API GitHub à nous renvoyer directement le code source sous format `diff` (les lignes ajoutées et supprimées) au lieu d'un fichier JSON lourd et complexe à parser.

### 2. Prompt Engineering & OpenRouter (`ai_reviewer.py`)

Le "cerveau" de l'application utilise la bibliothèque officielle `openai`, mais nous avons **détourné le `base_url`** vers `https://openrouter.ai/api/v1` afin d'exploiter le modèle `anthropic/claude-3.5-sonnet`, actuellement le plus performant pour la compréhension de code.

* **Prompt Dynamique (Pédagogie Adaptative) :** Le comportement de l'IA change drastiquement selon l'entrée utilisateur.
  * *Profil Junior :* L'IA reçoit des instructions (`system prompt`) strictes pour agir comme un mentor : elle doit être prolixe, expliquer le *pourquoi* des concepts fondamentaux, et utiliser des analogies.
  * *Profil Senior :* L'IA est bridée pour être purement technique, directe, et se concentrer uniquement sur l'algorithmique avancée et la sécurité.
* **Formatage :** L'IA est contrainte de renvoyer sa réponse en Markdown structuré (utilisation des `###`).

### 3. Backend, ORM et Sécurité (`app.py` & `config.py`)

* **Base de Données relationnelle :** Gérée via `Flask-SQLAlchemy`. Nous avons modélisé deux tables (`User` et `Review`) reliées par une clé étrangère (One-to-Many), permettant à chaque utilisateur de retrouver son historique d'analyses.
* **Sécurité Cryptographique :** Les mots de passe ne sont jamais stockés en clair. Nous utilisons `werkzeug.security` (`generate_password_hash` et `check_password_hash`) pour hacher les mots de passe avant l'insertion en BDD.
* **Gestion des Sessions :** Sécurisation des routes via `session['user_id']`. L'API (`/api/analyze`) bloque automatiquement les requêtes HTTP `POST` non autorisées (renvoi d'une erreur 401) si l'utilisateur n'est pas connecté.

### 4. Frontend Asynchrone (`index.html`)

L'interface utilisateur a été développée en Vanilla JS, HTML5 et CSS3.

* **Communication fluide :** Utilisation de l'API `fetch()` pour envoyer les requêtes d'analyse au serveur de manière asynchrone (AJAX). L'utilisateur n'a pas besoin de recharger la page, un "spinner" CSS gère l'attente.
* **Rendu du Rapport :** Utilisation de la bibliothèque `marked.js` côté client pour parser le texte Markdown renvoyé par l'IA et l'injecter proprement dans le DOM HTML (avec un formatage spécifique pour les blocs de code).

---

## 🛠️ Stack Technique

* **Backend :** Python 3, Flask, Flask-SQLAlchemy (ORM).
* **Frontend :** HTML5, CSS3, JavaScript (Fetch API, DOM manipulation).
* **Base de données :** MySQL (via PyMySQL).
* **Intelligence Artificielle :** OpenRouter API (Modèle Anthropic Claude 3.5 Sonnet).
* **Sécurité :** Werkzeug (Hachage), Dotenv (Variables d'environnement).

---

## 🚀 Guide d'Installation

### 1. Prérequis

* Python 3.8+ installé.
* Un serveur MySQL local actif (XAMPP, WAMP, etc.).
* Avoir créé une base de données vide nommée `code_reviewer_db`.

### 2. Cloner le projet et installer les dépendances

```bash
git clone <url-de-votre-repo>
cd projet-revieweur-ia

# Création et activation de l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate

# Installation des paquets
pip install -r requirements.txt
```
