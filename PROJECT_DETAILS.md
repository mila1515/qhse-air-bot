# Détails du Projet : QHSE Air Bot

## 📝 Vue d'ensemble
QHSE Air Bot est un assistant intelligent dédié à la Qualité, Hygiène, Sécurité et Environnement (QHSE). Il agrège des données provenant de multiples sources (réglementation, qualité de l'air, accidents industriels) pour fournir des informations consolidées via une API REST.

## 🏗️ Architecture Technique

### Structure du Code (`src/`)
- **`src/etl/`** : Pipeline d'Extraction, Transformation et Chargement.
  - `collect.py` : Récupère les données (API WAQI, Scraping INRS/CDTN, Open Data ARIA).
  - `transform.py` : Nettoie et normalise les données (Pandas).
  - `load.py` : Charge les données en base de données (PostgreSQL/SQLAlchemy).
- **`src/api/`** : API REST construite avec FastAPI.
  - `main.py` : Point d'entrée, configuration de l'application et instrumentation Prometheus.
  - `endpoints.py` & `models.py` : Définition des routes et schémas de données.
- **`src/monitoring/`** : Observabilité et Métriques.
  - `metrics.py` : Définition des métriques Prometheus (Gauges, Counters) et logique Pushgateway.
  - `logger.py` : Configuration centralisée des logs (Loguru).
- **`src/db/`** : Gestion de la base de données (modèles SQLAlchemy, session).

### Infrastructure (Docker)
Le projet utilise Docker Compose pour orchestrer les services :
1.  **API** (`qhse_api`) : Serveur FastAPI (Port 8000).
2.  **Base de Données** (`qhse_postgres`) : PostgreSQL 15 (Port 5432).
3.  **Monitoring Stack** (via `docker-compose-monitoring.yml`) :
    -   **Prometheus** (`qhse_prometheus`) : Collecte les métriques (Port 9090).
    -   **Grafana** (`qhse_grafana`) : Visualisation des tableaux de bord (Port 3000).
    -   **Pushgateway** (`qhse_pushgateway`) : Réception des métriques des jobs batch ETL (Port 9091).

## 🚀 Fonctionnalités Implémentées

### 1. Pipeline ETL (Automatisé)
-   **Sources de Données** :
    -   **WAQI** : Qualité de l'air temps réel pour 50 grandes villes françaises.
    -   **Code du Travail** : Articles de loi via scraping (CDTN).
    -   **INRS** : Guides de prévention (Web Scraping).
    -   **ARIA** : Base d'accidents industriels.
-   **Monitoring ETL** :
    -   Envoi automatique de métriques à la fin de chaque étape (Collect/Transform/Load).
    -   Métriques : Succès/Échec, Nombre de lignes traitées, Valeurs AQI temps réel.

### 2. API REST
-   Endpoints pour consulter les données (Articles, Guides, Accidents, Mesures WAQI).
-   Endpoint `/metrics` exposé pour le scraping Prometheus.
-   Documentation automatique via Swagger UI (`/docs`).

### 3. Monitoring & Observabilité
-   **Prometheus** : Scrape l'API toutes les 5s et la Pushgateway.
-   **Grafana** : Tableaux de bord pour visualiser la santé de l'API et les performances de l'ETL.
-   **Métriques Clés** :
    -   `etl_last_run_success_timestamp` : Dernier succès du pipeline.
    -   `etl_processed_rows_total` : Volume de données traité par source.
    -   `air_quality_index_value` : Jauge de qualité de l'air par ville.
    -   `http_requests_total` : Trafic API.

## 🛠️ Guide d'Utilisation Rapide

### Lancer l'environnement complet
```bash
# 1. Démarrer l'API et la BDD
docker-compose up -d

# 2. Démarrer le Monitoring
docker-compose -f docker-compose-monitoring.yml up -d
```

### Exécuter le Pipeline ETL (Mise à jour des données)
Les scripts envoient automatiquement les métriques au monitoring.
```bash
# Étape 1 : Collecte
python scripts/01_collect_data.py

# Étape 2 : Transformation
python scripts/02_transform_data.py

# Étape 3 : Chargement
python scripts/03_load_data.py
```

### Accès aux Interfaces
-   **API (Swagger)** : http://localhost:8000/docs
-   **Grafana** : http://localhost:3000 (Login: `admin` / `admin`)
-   **Prometheus** : http://localhost:9090

---

## 🏗️ Infrastructure & Outils : Comprendre la BDD

Une distinction importante pour comprendre l'environnement de données :

### 1. `qhse_postgres` (Le Coffre-Fort)
*   **C'est la base de données elle-même (Moteur).**
*   C'est là où sont **physiquement stockées** vos données (les villes, la qualité de l'air, les articles de loi, etc.).
*   C'est un service invisible qui travaille en arrière-plan. Il ne possède pas d'interface graphique native, il ne comprend que le langage SQL.
*   *Analogie : C'est le disque dur ou le classeur sécurisé où sont rangés tous les dossiers.*

### 2. Accès aux données (Le Client)
*   Vous pouvez utiliser l'outil de votre choix pour visualiser les données (pgAdmin, DBeaver, etc.).
*   **Configuration de connexion** :
    *   **Hôte** : `localhost`
    *   **Port** : `5436`
    *   **Utilisateur** : `chatbot`
    *   **Mot de passe** : `chatbot_secure_password_123`
    *   **Base de données** : `chatbot_qhse`

---

# Documentation détaillée du Monitoring

Ce document détaille l'architecture de surveillance mise en place pour le projet QHSE Air Bot. Il explique le "Quoi", le "Pourquoi" et le "Comment" du monitoring.

## 1. Vue d'ensemble (Architecture)

Le système de monitoring repose sur trois composants principaux (la stack "PLG" simplifiée) :

1.  **Prometheus (Le Cerveau)** : C'est la base de données de séries chronologiques. Il "aspire" (scrape) les métriques à intervalles réguliers (toutes les 5 secondes ici).
2.  **Grafana (Le Visage)** : C'est l'interface de visualisation. Il se connecte à Prometheus pour afficher des graphiques et des tableaux de bord compréhensibles.
3.  **Pushgateway (La Boîte aux lettres)** : Un composant intermédiaire crucial pour nos scripts ETL.

## 2. Fonctionnement détaillé & Relation avec la Data

### A. Le défi des scripts "Batch" (ETL)
Contrairement à une API qui tourne 24/7, nos scripts ETL (`collect`, `transform`, `load`) ne durent que quelques secondes.
*   **Problème** : Si Prometheus essaie de les interroger quand ils ne tournent pas, il ne trouve rien. S'il les interroge pendant qu'ils tournent, ils peuvent se terminer avant la réponse.
*   **Solution (Pushgateway)** :
    1.  Les scripts **calculent** leurs métriques pendant l'exécution (ex: nombre de villes collectées).
    2.  À la fin de l'exécution (bloc `finally`), ils **poussent** (push) ces métriques vers la **Pushgateway**.
    3.  La Pushgateway **stocke** ces valeurs en mémoire.
    4.  Prometheus vient **lire** la Pushgateway tranquillement, même si le script est fini depuis longtemps.

### B. Le cas de l'API (Service Continu)
L'API FastAPI est un service web classique.
*   **Mécanisme** : Nous utilisons `prometheus-fastapi-instrumentator`.
*   **Fonctionnement** : L'API expose une route spéciale `/metrics`.
*   **Scraping** : Prometheus interroge directement cette route (`http://api:8000/metrics`) pour connaître l'état de santé, le temps de réponse et le nombre de requêtes.

## 3. Les Métriques Clés (KPIs)

Nous surveillons trois types d'informations définies dans `src/monitoring/metrics.py` :

| Métrique | Type | Description | Utilité |
| :--- | :--- | :--- | :--- |
| `etl_last_run_success_timestamp` | **Gauge** | Heure du dernier succès (Unix) | Permet de savoir si l'ETL a planté ou ne tourne plus (alerte si > 24h). |
| `etl_processed_rows_total` | **Counter** | Nombre de lignes traitées | Vérifier qu'on récupère bien de la donnée (ex: si chute brutale, l'API source a peut-être changé). |
| `etl_error_count_total` | **Counter** | Nombre d'erreurs | Détecter les problèmes de parsing ou de connexion API. |
| `air_quality_index_value` | **Gauge** | Valeur AQI par ville | Suivi métier de la qualité de l'air en temps réel. |

## 4. Implémentation Technique

### Structure des fichiers
*   **`src/monitoring/metrics.py`** : Le cœur du système. Il définit les objets `Gauge` et `Counter` et contient la fonction `push_metrics()` qui envoie tout à la Pushgateway.
*   **`scripts/*.py`** : Chaque script importe `push_metrics` et l'appelle à la fin de son exécution pour "valider" les chiffres.
*   **`docker-compose-monitoring.yml`** : Orchestre le lancement des conteneurs (Prometheus, Grafana, Pushgateway) en réseau.
*   **`prometheus.yml`** : Le fichier de configuration qui dit à Prometheus *où* chercher les infos (`targets: ['pushgateway:9091', 'api:8000']`).

## 5. Pourquoi avoir fait ça ?

1.  **Observabilité** : On ne subit plus les pannes ("Tiens, la base est vide ?"). On les voit arriver.
2.  **Débogage** : Si `etl_error_count` explose sur la source "WAQI", on sait tout de suite qu'il faut regarder le script `collect.py` ou la clé API WAQI.
3.  **Confiance** : On peut prouver que les données sont fraîches grâce au timestamp de dernière exécution.
