# Recommandations pour la Soutenance

Ce document anticipe les questions techniques pointues que le jury pourrait poser lors de la présentation, avec des éléments de réponse basés sur le code réel du projet.

---

## 1. Monitoring et Observabilité (C20)

**Question Jury :** *"Pourquoi avoir choisi Prometheus plutôt qu'une simple journalisation (logs) ? Quel avantage cela apporte-t-il pour la détection en temps réel ?"*

**Éléments de Réponse :**
*   **Logs vs Métriques :** Les logs (gérés par [logger.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\monitoring\logger.py)) racontent une "histoire" détaillée (pour le débogage), tandis que Prometheus gère des **séries temporelles** chiffrées (pour la supervision).
*   **Détection Temps Réel :** Prometheus permet de définir des **alertes mathématiques** (ex: "Si le taux d'erreur > 5% pendant 1 minute"). Faire cela avec des logs nécessiterait de parser des gigaoctets de texte en temps réel, ce qui est lent et coûteux.
*   **Code :** Dans [metrics.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\monitoring\metrics.py), nous utilisons des `Counter` et `Histogram` qui sont instantanément agrégables, contrairement aux lignes de texte dans `app.log`.

---

## 2. Résolution d'Incident et Fallback (C21)

**Question Jury :** *"Votre solution de repli (Fallback) vers Google Gemini utilise-t-elle la même base vectorielle (FAISS) ? Comment garantissez-vous que la réponse reste cohérente d'un modèle à l'autre ?"*

**Éléments de Réponse :**
*   **Architecture Unifiée :** Oui, la base de connaissance est identique. Comme le montre [rag_chain.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\rag\pipeline\rag_chain.py), le "Retrieval" (récupération des documents) est effectué **avant** l'appel au LLM.
*   **Flux de Données :**
    1.  Le `retriever` trouve les documents pertinents (ex: "Article R4222-10").
    2.  Ces documents sont stockés dans la variable `docs`.
    3.  Si Azure échoue, nous passons **exactement les mêmes `docs`** à Google Gemini via `fallback_docs_chain.invoke({"context": docs})`.
*   **Garantie de Cohérence :** L'IA (Azure ou Google) ne sert qu'à *synthétiser* l'information fournie. Puisque la source (le contexte FAISS) ne change pas, la réponse factuelle reste la même, seul le style de rédaction peut varier légèrement.

---

## 3. Sécurité et RGPD

**Question Jury :** *"Comment vous assurez-vous que les logs du monitoring ne contiennent pas de données personnelles sensibles (RGPD) ?"*

**Éléments de Réponse :**
*   **Minimisation des Données :** Nous privilégions les logs techniques (Statut 200/500, temps de réponse) aux logs conversationnels.
*   **Politique de Rétention :** Dans [logger.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\monitoring\logger.py), nous avons configuré une rotation automatique et une rétention stricte :
    ```python
    logger.add(..., retention="7 days")
    ```
    Cela garantit le "Droit à l'oubli" par défaut ; aucun log n'est conservé indéfiniment.
*   **Anonymisation (Piste d'amélioration) :** Actuellement, les questions sont logguées pour le debugging. Pour une mise en production stricte, nous ajouterions un filtre "PII Scrubber" (comme Microsoft Presidio) avant l'écriture dans les logs pour masquer automatiquement les noms ou numéros de téléphone détectés.

---

## 4. Intégration Continue (CI/CD) et Base de Données

**Question Jury :** *"Comment gérez-vous la base de données lors des tests automatisés dans GitHub Actions, sachant que vous utilisez une base locale en développement ?"*

**Éléments de Réponse :**
*   **Phrase clé :** "Pour l'intégration continue, j'utilise un conteneur de service PostgreSQL éphémère. Cela garantit l'isolation des tests et évite les effets de bord liés aux données locales."
*   **Preuve Technique :** Dans le fichier [main.yml](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\.github\workflows\main.yml), la section `services: postgres` lance une base de données vierge dédiée uniquement à la durée du test.
*   **Mécanisme :** Le fichier [config.py](file:///c:\Users\djami\Desktop\devIA\project\qhse-air-bot\src\config.py) détecte automatiquement les variables d'environnement injectées par GitHub Actions (`DATABASE_URL`) et se connecte à ce conteneur éphémère au lieu de chercher la base locale.
