# RAPPORT DE COMPÉTENCES E5 : SURVEILLANCE ET RÉSOLUTION D'INCIDENTS
**Projet :** QHSE Air Bot  
**Candidat :** Djamel  
**Date :** 28 Janvier 2026

---

## 1. Contexte de la Preuve
Ce rapport valide les compétences du bloc **"Surveiller l'application et résoudre les incidents"** (C20, C21). Il démontre la mise en place d'une architecture de monitoring robuste et la gestion proactive d'un incident critique lié aux dépendances externes (APIs IA).

---

## 2. Surveillance de l'Application (C20)

### 2.1 Architecture de Monitoring
Pour surveiller **QHSE Air Bot**, j'ai déployé une stack standard de l'industrie (Prometheus/Grafana) conteneurisée via Docker.

*   **Prometheus** : Base de données de séries temporelles qui "pull" (récupère) les métriques toutes les 15 secondes.
*   **Grafana** : Interface de visualisation connectée à Prometheus pour afficher les tableaux de bord.
*   **Pushgateway** : Composant intermédiaire permettant à nos scripts batch (ETL, Scrapers) de pousser leurs métriques à la fin de leur exécution (car Prometheus ne peut pas "scraper" un script qui s'arrête).

**Preuve d'Infrastructure :**
> Voir le fichier [docker-compose.yml](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\docker-compose.yml) (lignes 74-100) définissant les services `prometheus`, `grafana` et `pushgateway`.

### 2.2 Stratégie de Logs (Journalisation)
J'ai remplacé les `print()` standards par la librairie **Loguru**.
*   **Avantage :** Logs structurés, niveaux de sévérité (INFO, WARNING, ERROR), et rotation automatique des fichiers.
*   **Sécurité :** Les logs sont configurés pour ne **jamais** afficher les clés d'API ou les données personnelles (RGPD), se limitant aux métadonnées techniques et aux erreurs.

**Preuve de Code :**
> Voir [src/monitoring/logger.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\monitoring\logger.py) pour la configuration centralisée.

### 2.3 Métriques Clés Surveillées
J'ai défini des métriques "Métier" spécifiques pour valider le bon fonctionnement de l'IA et des données :

1.  **Fraîcheur des Données (ETL) :**
    *   `etl_last_run_success_timestamp` : Permet de savoir si la base de connaissances est à jour.
    *   `etl_processed_rows_total` : Volume de documents traités (alerting si volume = 0).
2.  **Santé du RAG :**
    *   `rag_query_latency` : Temps de réponse (crucial pour l'UX).
    *   `rag_fallback_activation_count` : Nombre de fois où le système a dû basculer sur le modèle de secours (Google).

**Preuve de Code :**
> Voir [src/monitoring/metrics.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\monitoring\metrics.py).

---

## 3. Gestion et Résolution d'Incident (C21)

### 3.1 Scénario de l'Incident : "Panne Majeure Azure OpenAI"
**Description :** Le mardi 28/01 à 14h00, l'API Azure OpenAI ne répond plus (Erreur 503 Service Unavailable) ou les latences dépassent 30 secondes (Timeout).
**Impact :** Le Chatbot ne peut plus générer de réponses, bloquant les utilisateurs sur le terrain.

### 3.2 Détection
L'incident est détecté par deux canaux :
1.  **Monitoring :** Pic d'erreurs `5xx` sur le dashboard Grafana.
2.  **Logs Applicatifs :** Apparition de warnings `openai.error.ServiceUnavailableError` dans les logs du backend.

### 3.3 Résolution Automatique (Self-Healing)
Pour garantir la continuité de service (Business Continuity Plan), j'ai implémenté un mécanisme de **Fallback (Bascule Automatique)** au niveau du code.

**Algorithme de Résolution :**
1.  Le système tente d'interroger le modèle principal (Azure GPT-4).
2.  En cas d'exception (Timeout, API Error), le code capture l'erreur (`try/except`).
3.  Le système bascule instantanément vers le fournisseur de secours (**Google Gemini Pro**).
4.  L'utilisateur reçoit sa réponse sans interruption, avec une latence légèrement accrue mais acceptable.

**Preuve Technique (Code du Fallback) :**
Extrait de [src/rag/pipeline/rag_chain.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\rag\pipeline\rag_chain.py#L185-L193) :

```python
try:
    # Tentative 1 : Chaîne Principale (Azure)
    response = self.combine_docs_chain.invoke({"input": question, "context": docs})
except Exception as e_main:
    # Si erreur, bascule sur le Fallback
    if self.fallback_docs_chain:
        logger.warning(f"⚠️ Échec du LLM Principal ({e_main}). Bascule sur Google Gemini...")
        response = self.fallback_docs_chain.invoke({"input": question, "context": docs})
```

### 3.4 Solution de Repli Ultime (Mode Dégradé)
Si **Azure ET Google** sont en panne (scénario catastrophe) ou s'il y a une coupure internet totale :
*   **Embeddings :** Le système bascule sur un modèle local (`all-MiniLM-L6-v2`) qui ne nécessite pas d'internet.
*   **Preuve :** Voir [src/rag/embeddings/embedding_provider.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\rag\embeddings\embedding_provider.py) (logique `try Azure -> except OpenAI -> except Local`).

### 3.5 Post-Mortem et Amélioration Continue
Une fois l'incident clos :
1.  **Analyse :** Vérifier pourquoi Azure a planté (quota dépassé ? panne régionale ?).
2.  **Action :** Si c'est un problème de quota, augmenter les limites via le portail Azure.
3.  **Optimisation :** Ajuster le `request_timeout` dans la configuration pour basculer plus vite vers Google (ex: passer de 30s à 10s).

---

## 4. Conclusion
L'architecture de QHSE Air Bot intègre la **résilience par design**. Le monitoring permet de *voir* le problème, et le code est conçu pour *réagir* automatiquement, transformant une panne critique en simple avertissement dans les logs.
