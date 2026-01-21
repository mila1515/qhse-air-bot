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
Le projet intègre **Evidently AI** pour détecter la dérive des données (Drift) et valider leur qualité avant insertion en base ou périodiquement.

*   **Rapports HTML** : Générés dans `src/data_monitoring/reports/`.
*   **Scripts** :
    *   `src/data_monitoring/drift/` : Détection de dérive (comparaison référence vs actuel).
    *   `src/data_monitoring/quality/` : Analyse de la qualité (valeurs manquantes, stats).

**Génération des rapports :**
```bash
# Exemple pour WAQI
python src/data_monitoring/drift/waqi_drift.py
python src/data_monitoring/quality/waqi_quality.py
```

## 🧪 Exécuter les Tests
Pour valider le bon fonctionnement du code :

```bash
# Installation des dépendances locales (si pas de Docker)
pip install -r requirements.txt

# Lancement des tests
pytest
```

*Projet développé avec Python, FastAPI, PostgreSQL et Docker.*
