# QHSE Air Bot 🌍

**Assistant intelligent pour l'analyse et le monitoring des données QHSE (Qualité, Hygiène, Sécurité, Environnement).**

Ce projet centralise des données réglementaires et environnementales pour faciliter la prise de décision et la surveillance des risques. Il combine une architecture ETL robuste, un assistant IA résilient et un monitoring complet.

---

## 🚀 Fonctionnalités Principales

*   **📡 Collecte Multi-Sources (ETL)** :
    *   **Réglementation** : Articles du Code du Travail (Scraping).
    *   **Prévention** : Guides et brochures de l'INRS.
    *   **Retours d'Expérience** : Historique des accidents industriels (Base ARIA).
    *   **Temps Réel** : Qualité de l'air et polluants (API WAQI).
*   **🔌 API REST Performante** : Construite avec **FastAPI**, documentée automatiquement via Swagger UI.
*   **📊 Observabilité & Monitoring** :
    *   **Métriques** : Stack Prometheus/Grafana pour surveiller la santé système et métier (ETL, RAG).
    *   **Logs** : Journalisation structurée et sécurisée avec Loguru.
*   **🧠 Assistant IA Résilient (RAG)** :
*   **Multi-Provider** : OpenAI Standard (Principal) avec fallback DeepSeek éventuel.
    *   **Mode Déconnecté** : Embeddings locaux si nécessaire.

## 🛠️ Démarrage Rapide (Docker)

Le projet est entièrement conteneurisé pour un déploiement facile et reproductible.

### 1. Lancer l'application
```bash
docker-compose up -d --build
```
*Cela démarre l'API, la Base de données, le Frontend et toute la stack de monitoring.*

### 2. Accéder aux Interfaces
| Service | URL | Description |
| :--- | :--- | :--- |
| **Frontend App** | [http://localhost:8501](http://localhost:8501) | Interface Utilisateur (Streamlit) |
| **Documentation API** | [http://localhost:8100/docs](http://localhost:8100/docs) | Tester les endpoints en direct |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | Visualiser les tableaux de bord (Monitoring) |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Explorer les métriques brutes |
| **Evidently UI** | [http://localhost:8101](http://localhost:8101) | Dashboard Qualité des Données (Data Drift) |

---

## 🤖 Architecture RAG (Retrieval-Augmented Generation)

Le module d'IA générative répond aux questions en se basant sur la documentation collectée. Il est conçu pour la **haute disponibilité**.

### Stratégie de Fallback (Résilience)
1.  **Tentative Principale** : Interrogation du modèle **OpenAI Standard** (si une clé `OPENAI_API_KEY` est configurée).
2.  **Fallback** : Interrogation du modèle **DeepSeek** si la clé `DEEPSEEK_API_KEY` est configurée.
3.  **Embeddings** : Utilisation d'**OpenAI Embeddings** (`text-embedding-3-small`) si possible, puis d'un modèle local (`all-MiniLM-L6-v2`) si les APIs d'embedding sont indisponibles.

### Utilisation (CLI)
Le module RAG peut être testé directement en ligne de commande :

1.  **Ingestion des données** (À lancer après l'ETL) :
    Exporte les données SQL et crée l'index vectoriel (FAISS).
    ```bash
    python src/rag/main.py --ingest
    ```

2.  **Poser une question** :
    ```bash
    python src/rag/main.py --query "Quelles sont les procédures en cas d'incendie ?"
    ```

---

## �️‍♂️ Qualité des Données (Evidently AI)

Le projet surveille la *valeur* de la donnée via **Evidently AI** :
*   **Data Drift** : Détection des dérives statistiques (ex: changement brutal de la qualité de l'air).
*   **Automatisation** : Un scheduler lance les tests de qualité chaque nuit à 22h00.

---

## 🔒 Sécurité

*   **Gestion des Secrets** : Aucune clé d'API n'est stockée dans le code. Tout passe par un fichier `.env` non versionné.
*   **Logs Anonymisés** : Les logs applicatifs sont filtrés pour ne jamais exposer de données sensibles (RGPD, Clés).

---

## 🧪 Tests

Le projet inclut une suite de tests unitaires et d'intégration (avec Mocks pour les APIs externes).

```bash
# Lancer les tests
pytest
```

*Projet développé avec Python 3.12, FastAPI, PostgreSQL et Docker.*
