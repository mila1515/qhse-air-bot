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

## 🕵️‍♂️ Monitoring Qualité des Données (Evidently)

Le projet intègre **Evidently AI** pour assurer la fiabilité des données ingérées. Ce module est distinct du monitoring système (Prometheus/Grafana) et se concentre sur la *valeur* et la *qualité* de la donnée métier.

### 📂 Structure du Module
Le code se trouve dans `src/data_monitoring/` :
*   `drift/` : Scripts de détection de dérive (Data Drift). Compare les nouvelles données (current) à un jeu de référence (reference) pour détecter les changements de distribution.
*   `quality/` : Scripts de contrôle qualité (Data Quality). Vérifie les statistiques descriptives, les valeurs manquantes et la cohérence des données.
*   `reports/` : Dossier de sortie contenant les rapports HTML générés automatiquement (ignorés par Git).

### 🚦 Exécution des Rapports
Les scripts peuvent être lancés manuellement ou intégrés au pipeline ETL (fin de l'étape Load).

**Générer les rapports de dérive (Drift) :**
```bash
python src/data_monitoring/drift/waqi_drift.py  # Pour les données Qualité de l'Air
python src/data_monitoring/drift/aria_drift.py  # Pour les données ARIA (Accidents)
```

**Générer les rapports de qualité (Quality) :**
```bash
python src/data_monitoring/quality/waqi_quality.py
python src/data_monitoring/quality/aria_quality.py
```

### 📊 Visualisation
Les résultats sont générés sous forme de fichiers HTML interactifs dans `src/data_monitoring/reports/`.
*   Ces rapports peuvent être ouverts directement dans un navigateur.
*   Ils sont également conçus pour être intégrés dans **Grafana** via un plugin de visualisation HTML (ex: Ajax panel ou Text panel avec iframe), permettant aux équipes métier de consulter l'état des données directement depuis les dashboards de supervision.

## 🧪 Exécuter les Tests
Pour valider le bon fonctionnement du code :

```bash
# Installation des dépendances locales (si pas de Docker)
pip install -r requirements.txt

# Lancement des tests
pytest
```

*Projet développé avec Python, FastAPI, PostgreSQL et Docker.*
