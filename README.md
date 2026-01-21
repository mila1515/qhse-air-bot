# QHSE Air Bot 🌍

**Assistant intelligent pour l'analyse et le monitoring des données QHSE (Qualité, Hygiène, Sécurité, Environnement).**

Ce projet centralise des données réglementaires et environnementales pour faciliter la prise de décision et la surveillance des risques.

---

## 🚀 Fonctionnalités Principales

*   **📡 Collecte Multi-Sources (ETL)** :
    *   **Réglementation** : Articles du Code du Travail (Scraping).
    *   **Prévention** : Guides et brochures de l'INRS.
    *   **Retours d'Expérience** : Historique des accidents industriels (Base ARIA).
    *   **Temps Réel** : Qualité de l'air et polluants (API WAQI).
*   **🔌 API REST Performante** : Construite avec **FastAPI**, documentée automatiquement via Swagger UI.
*   **📊 Observabilité Complète** : Stack de monitoring intégrée (Prometheus, Grafana, Pushgateway) pour surveiller la santé de l'app et les données.

## 🛠️ Démarrage Rapide (Docker)

Le projet est entièrement conteneurisé pour un déploiement facile.

### 1. Lancer l'application
```bash
docker-compose up -d --build
```
*Cela démarre l'API, la Base de données, et toute la stack de monitoring.*

### 2. Accéder aux Interfaces
| Service | URL | Description |
| :--- | :--- | :--- |
| **Documentation API** | [http://localhost:8000/docs](http://localhost:8000/docs) | Tester les endpoints en direct |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | Visualiser les tableaux de bord |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Explorer les métriques brutes |
| **Evidently UI** | [http://localhost:8101](http://localhost:8101) | Dashboard Qualité des Données |

## 🕵️‍♂️ Monitoring Qualité des Données (Evidently)

Le projet intègre **Evidently AI** pour assurer la fiabilité des données ingérées. Ce module est distinct du monitoring système (Prometheus/Grafana) et se concentre sur la *valeur* et la *qualité* de la donnée métier.

### 📂 Structure du Module
Le code se trouve dans `src/data_monitoring/` :
*   `drift/` : Scripts de détection de dérive (Data Drift). Compare les nouvelles données (current) à un jeu de référence (reference) pour détecter les changements de distribution.
*   `quality/` : Scripts de contrôle qualité (Data Quality). Vérifie les statistiques descriptives, les valeurs manquantes et la cohérence des données.

### 🔄 Automatisation (Pipeline Complet)
Le projet utilise un **Scheduler automatique** intégré dans Docker.
- Il tourne en tâche de fond dans le conteneur `qhse_scheduler`.
- Il lance le pipeline complet (Collecte ➔ Load ➔ Monitoring) **tous les jours à 22:00**.

Vous n'avez rien à faire, tout est automatique.

Pour lancer le pipeline manuellement (hors horaire prévu) :
```bash
# Lancer le pipeline complet manuellement
python src/etl/pipeline.py
```

### 🚦 Exécution Manuelle des Rapports (Optionnel)
Les scripts peuvent aussi être lancés individuellement si nécessaire.

**Exécuter les analyses (Drift & Quality) :**
```bash
# Analyse de dérive (Drift)
python src/data_monitoring/drift/waqi_drift.py
python src/data_monitoring/drift/aria_drift.py

# Analyse de qualité (Quality)
python src/data_monitoring/quality/waqi_quality.py
python src/data_monitoring/quality/aria_quality.py
```

### 📊 Visualisation
Le projet utilise le **service Evidently** (mode serveur) pour centraliser les rapports.
*   **Interface Web** : Accessible sur [http://localhost:8101](http://localhost:8101).
*   **Fonctionnement** : Les scripts Python envoient les métriques via l'API du service Docker, sans générer de fichiers HTML locaux.
*   **Intégration** : Le dashboard Evidently permet de suivre l'évolution de la qualité dans le temps (historisation des snapshots).

## 🧪 Exécuter les Tests
Pour valider le bon fonctionnement du code :

```bash
# Installation des dépendances locales (si pas de Docker)
pip install -r requirements.txt

# Lancement des tests
pytest
```

*Projet développé avec Python, FastAPI, PostgreSQL et Docker.*
