import sys
import os

# Ajout du chemin racine au path
sys.path.append(os.getcwd())

from src.rag.pipeline.rag_chain import rag_pipeline
from src.monitoring.logger import logger

if __name__ == "__main__":
    logger.info("🚀 Lancement manuel de l'ingestion RAG...")
    try:
        rag_pipeline.ingest_data()
        logger.info("✅ Ingestion terminée avec succès.")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'ingestion : {e}")
