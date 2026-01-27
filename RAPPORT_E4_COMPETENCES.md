# RAPPORT DE COMPÉTENCES E4 - DÉVELOPPEMENT D'UNE APPLICATION IA COMPLÈTE

**Projet :** QHSE Air Bot
**Candidat :** [Votre Nom]
**Date :** Janvier 2026

---

## 1. Contexte et Besoin du Commanditaire (C14)

### 1.1 Présentation du Contexte
Le projet **QHSE Air Bot** répond à un besoin critique des responsables Qualité, Hygiène, Sécurité et Environnement (QHSE) dans le secteur industriel. Ces professionnels doivent gérer une double contrainte :
1.  **Veille Réglementaire** : Maîtriser un volume massif de textes juridiques (Code du Travail, arrêtés préfectoraux).
2.  **Surveillance Environnementale** : Suivre en temps réel la qualité de l'air et les incidents industriels.

### 1.2 Problématique et Objectifs
**Problème :** L'accès à l'information est fragmenté. Un responsable QHSE perd du temps à chercher l'article de loi pertinent ou à vérifier les relevés de capteurs sur des sites disparates.

**Objectif :** Développer une application centralisée ("One-Stop Shop") intégrant :
*   Un **Assistant IA (Chatbot)** capable de répondre aux questions réglementaires en citant ses sources.
*   Un **Dashboard** de visualisation des données environnementales (Qualité de l'air WAQI, Accidents ARIA).

### 1.3 Utilisateurs Cibles (Personas)
*   **Le Responsable QHSE** : Utilisateur principal. Besoin de réponses fiables, rapides et sourcées.
*   **L'Auditeur / Inspecteur** : Besoin de vérifier la conformité d'un site par rapport aux normes en vigueur.

---

## 2. Spécifications Fonctionnelles et Modélisation (C14)

### 2.1 Fonctionnalités Priorisées (MVP)
Le périmètre du Minimum Viable Product (MVP) a été défini comme suit :
1.  **Authentification Sécurisée** : Accès restreint via Login/Mot de passe (JWT).
2.  **Module Chat RAG** : Interface de dialogue avec l'IA, interrogant une base vectorielle de documents métiers.
3.  **Module Dashboard** : Graphiques interactifs montrant l'évolution des polluants (NO2, PM10) et les incidents récents.
4.  **Gestion de Notes** : Possibilité pour l'utilisateur de sauvegarder des informations clés.

### 2.2 Parcours Utilisateur (User Flow)
1.  **Login** : L'utilisateur arrive sur la page d'accueil, s'identifie.
2.  **Dashboard** : Il accède immédiatement à la "Météo des sites" (Alertes pollution).
3.  **Consultation** : Il pose une question technique ("Quelle est la VLEP pour le Benzène ?").
4.  **Réponse** : Le bot répond en affichant l'extrait du Code du Travail correspondant.
5.  **Action** : L'utilisateur peut copier la réponse ou l'ajouter à ses notes.

### 2.3 UX et Accessibilité
*   **Design System** : Utilisation de Streamlit pour une interface épurée et responsive. Voir [app.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\frontend\app.py).
*   **Accessibilité** : Contraste élevé pour les textes, navigation au clavier native, messages d'erreur clairs (pas de jargon technique).

---

## 3. Cadre Technique et Architecture (C15)

### 3.1 Architecture Globale
L'application repose sur une architecture **Microservices** conteneurisée :

```mermaid
graph TD
    Client[Navigateur Utilisateur] -->|HTTPS| Frontend[Streamlit (UI)]
    Frontend -->|REST API + JWT| Backend[FastAPI (Core)]
    Backend -->|SQL| DB[(PostgreSQL)]
    Backend -->|Vector Search| FAISS[(FAISS Index)]
    Backend -->|API Call| Azure[Azure OpenAI Service]
```

### 3.2 Choix Technologiques
*   **Frontend : Streamlit (Python)**. Choix pragmatique pour le prototypage rapide d'interfaces Data/IA. Permet de se concentrer sur la logique métier.
*   **Backend : FastAPI**. Framework asynchrone moderne, très performant, générant automatiquement la documentation (OpenAPI).
*   **Base de Données : PostgreSQL**. Robustesse pour les données relationnelles (utilisateurs, historiques, notes).
*   **IA : Azure OpenAI**. Garantie de sécurité des données (Enterprise Grade) et performance des modèles GPT-4.
*   **Déploiement : Docker**. Standardisation de l'environnement de dev à la prod.

### 3.3 Preuve de Concept (POC)
La faisabilité technique a été validée par un POC initial connectant un script Python simple à l'API Azure pour vérifier la qualité des réponses sur un document test ("Code du Travail - Extrait").

---

## 4. Organisation du Projet et Coordination (C16)

### 4.1 Méthodologie Agile
Le développement a suivi une approche itérative (inspirée de Scrum) :
*   **Sprints** courts (1 semaine).
*   **Backlog** : Liste des fonctionnalités gérée (simulé) via GitHub Projects / Trello.

### 4.2 Suivi des Tâches
Exemple de découpage du travail :
*   *Sprint 1* : Setup Docker + Base de données.
*   *Sprint 2* : Développement API Backend + Auth.
*   *Sprint 3* : Pipeline RAG + Intégration Azure.
*   *Sprint 4* : Interface Streamlit + Connexion API.

### 4.3 Gestion de Version (Git)
Utilisation de Git avec une stratégie de branches :
*   `main` : Code stable, livrable.
*   `dev` / `feature/*` : Développement des nouvelles fonctionnalités.
*   Commits atomiques et messages explicites.

### 4.4 Gestion des Risques et Imprévus (Scénario C16)
Si un **imprévu technique** survient (ex: Latence inacceptable de l'API Azure), j'applique la méthode **MoSCoW** pour réévaluer le backlog :
*   **Action** : Je sacrifie une fonctionnalité "Could have" (ex: Export PDF des notes) pour libérer du temps.
*   **Objectif** : Sauver le "Must have" (le Chatbot) et garantir la livraison dans les délais.

---

## 5. Développement de l'Application (C17)

### 5.1 Structure du Code (Clean Architecture)
Le code est organisé pour séparer les responsabilités :
*   `src/api/` : Logique des endpoints, validation des données (Pydantic).
*   `src/rag/` : Logique purement IA (Chaines LangChain, Prompts).
*   `src/frontend/` : Composants visuels et gestion de l'état de session.

### 5.2 Points d'Attention Techniques
*   **Sécurité** : Les secrets (clés API, mots de passe BDD) ne sont jamais codés en dur, mais chargés via des variables d'environnement (`.env`).
*   **Performance** : Utilisation de `async/await` dans FastAPI pour gérer de multiples requêtes simultanées sans blocage.
*   **Mocking** : Comme vu dans le dossier E3, les appels coûteux (Azure) sont mockés dans les tests pour garantir la rapidité du développement.

---

## 6. Intégration Continue (C18)

### 6.1 Pipeline CI
Un pipeline d'Intégration Continue (CI) a été mis en place via **GitHub Actions**. Voir [main.yml](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\.github\workflows\main.yml).

### 6.2 Étapes du Pipeline
À chaque `push` sur la branche principale :
1.  **Checkout** : Récupération du code.
2.  **Setup Python** : Installation de l'environnement.
3.  **Linting** : Vérification de la qualité du code (Flake8 / Black).
4.  **Tests Unitaires** : Exécution automatique de `pytest`. Voir [test_api.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\tests\test_api.py).
    *   Si un test échoue (ex: régression sur le calcul des seuils), le pipeline s'arrête et le commit est marqué "Failed".

### 6.3 Garantie de Qualité
Ce processus interdit l'intégration de code "cassé" dans la branche principale, garantissant une base de code toujours déployable.

---

## 7. Livraison Continue (C19)

### 7.1 Stratégie de Déploiement
L'application est livrée sous forme d'images **Docker**.
Le pipeline CD (Continuous Delivery) étend la CI :
1.  **Build** : Construction des images `qhse-backend` et `qhse-frontend`.
2.  **Push** : Envoi des images vers un registre privé (ou Docker Hub).
3.  **Deploy** : Sur le serveur de production, un simple `docker-compose pull && docker-compose up -d` suffit à mettre à jour l'application avec la dernière version.

### 7.2 Gestion des Environnements
La configuration spécifique à chaque environnement (Dev vs Prod) est gérée exclusivement par le fichier `.env`, sans modifier le code source (Principe "Twelve-Factor App").

---

## 8. Bilan et Perspectives

### 8.1 Ce qui fonctionne bien
*   L'architecture découplée (Back/Front) est robuste et maintenable.
*   Le pipeline RAG offre des réponses pertinentes (>80% de précision sur les tests).
*   L'environnement Docker simplifie drastiquement l'installation ("It works on my machine").

### 8.2 Pistes d'Amélioration
*   **Tests E2E** : Ajouter des tests de bout en bout (avec Selenium ou Playwright) pour tester l'interface graphique.
*   **Feedback Utilisateur** : Ajouter un système de "pouce haut/bas" sur les réponses du chat pour affiner le modèle (RLHF simplifié).
*   **Multi-modalité** : Permettre à l'utilisateur d'uploader des photos d'incidents pour analyse par GPT-4o Vision.
