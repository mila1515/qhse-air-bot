# Détails du Projet : QHSE Air Bot

Ce document fournit une vue d'ensemble technique et fonctionnelle complète du projet **QHSE Air Bot**.

## 1. Description Générale
**QHSE Air Bot** est une plateforme intégrée d'analyse et de monitoring de données QHSE (Qualité, Hygiène, Sécurité, Environnement). Elle automatise la collecte de données réglementaires et environnementales, les centralise dans une base de données, et les expose via une API REST tout en assurant une surveillance technique et métier complète.

---

## 2. Architecture Technique

### Stack Technologique
- **Langage** : Python 3.12+
- **Framework API** : FastAPI
- **Base de Données** : PostgreSQL 15
- **ORM** : SQLAlchemy
- **Validation de Données** : Pydantic V2
- **Data Processing** : Pandas, BeautifulSoup4 (Scraping)
- **Conteneurisation** : Docker & Docker Compose
- **Tests** : Pytest
- **Monitoring** : Prometheus, Grafana, Pushgateway

### Infrastructure Docker
Le projet est orchestré via `docker-compose.yml` et comprend 5 services interconnectés sur le réseau `qhse_net` :
1.  **`api`** : Application FastAPI (Port 8000).
2.  **`postgres`** : Base de données relationnelle (Port 5432).
3.  **`prometheus`** : Collecteur de métriques (Port 9090).
4.  **`grafana`** : Visualisation des tableaux de bord (Port 3000).
5.  **`pushgateway`** : Passerelle pour les métriques des jobs batch ETL (Port 9091).

---

## 3. Composants du Projet

### A. Pipeline ETL (`src/etl/`)
Le module ETL (Extract, Transform, Load) est responsable de l'alimentation des données.

*   **Collecte (`collect.py`)** : Récupération multi-sources.
    *   **Code du Travail** : Scraping du site `code.travail.gouv.fr` pour les articles R4222 (Aération/Assainissement).
    *   **INRS** : Scraping des guides de prévention et sécurité.
    *   **ARIA** : Importation Open Data des accidents industriels.
    *   **WAQI** : Connexion API temps réel pour la qualité de l'air (PM2.5, PM10, NO2, O3).
*   **Transformation (`transform.py`)** : Nettoyage, normalisation et structuration via Pandas.
*   **Chargement (`load.py`)** : Insertion/Mise à jour en base PostgreSQL via SQLAlchemy.

### B. API REST (`src/api/`)
L'interface d'accès aux données pour les clients (Front-end, Chatbot, Analystes).

*   **Endpoints Principaux** :
    *   `GET /articles/` : Consultation des articles de loi.
    *   `GET /guides/` : Accès aux guides INRS.
    *   `GET /accidents/` : Historique des accidents industriels.
    *   `GET /waqi/` : Mesures de qualité de l'air.
    *   `GET /stats/risks` : Statistiques agrégées (SQL complexe) sur les risques.
*   **Endpoints Système** :
    *   `GET /health` : État de santé de l'API et connexion DB.
    *   `GET /metrics` : Exposition des métriques pour Prometheus.
*   **Documentation** : Swagger UI disponible sur `/docs`.

### C. Monitoring & Observability (`src/monitoring/`)
Système complet de surveillance de la santé de l'application.

*   **Métriques Techniques** : Requêtes par seconde, latence, erreurs HTTP, utilisation CPU/RAM (via `prometheus-fastapi-instrumentator`).
*   **Métriques Métier** : Nombre de lignes traitées par l'ETL, succès/échec des jobs de collecte (via Pushgateway).
*   **Visualisation** : Dashboards Grafana pré-configurés pour le suivi temps réel.

### D. Tests (`tests/`)
Suite de tests automatisés avec `pytest` pour garantir la stabilité.

*   **`test_api.py`** : Tests d'intégration des endpoints HTTP.
*   **`test_db.py`** : Validation de la connexion et des transactions BDD.
*   **`test_etl.py`** : Tests unitaires avec Mocks pour simuler les sources de données (sans appels réseau réels).
*   **`test_monitoring.py`** : Vérification de l'exposition correcte des métriques Prometheus.

---

## 4. Structure du Code
```
qhse-air-bot/
├── src/
│   ├── api/          # Application FastAPI (Routes, Modèles Pydantic)
│   ├── db/           # Configuration DB, Modèles SQLAlchemy, Sessions
│   ├── etl/          # Logique d'extraction et traitement des données
│   ├── monitoring/   # Configuration Logs et Métriques
│   └── config.py     # Gestion des variables d'environnement
├── tests/            # Tests unitaires et d'intégration
├── scripts/          # Scripts utilitaires (Lancement ETL, Check env)
├── docker-compose.yml # Orchestration des conteneurs
├── prometheus.yml    # Configuration Prometheus
├── requirements.txt  # Dépendances Python
└── README.md         # Documentation rapide
```

---

## 5. Guide d'Utilisation

### Lancement complet (Docker)
Pour démarrer toute la stack (App + DB + Monitoring) :
```bash
docker-compose up -d --build
```
*   API : http://localhost:8000
*   Docs API : http://localhost:8000/docs
*   Prometheus : http://localhost:9090
*   Grafana : http://localhost:3000
*   Pushgateway : http://localhost:9091

### Développement Local
1.  Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
2.  Lancer les tests :
    ```bash
    pytest
    ```
3.  Lancer l'API :
    ```bash
    python -m src.api.main
    # ou
    uvicorn src.api.main:app --reload
    ```
