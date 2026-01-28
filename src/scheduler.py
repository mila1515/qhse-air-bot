import time
import schedule
import sys
import os

# Ajout du chemin racine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.etl.pipeline import run_pipeline
from src.rag.pipeline.rag_chain import rag_pipeline
from src.monitoring.logger import logger

def etl_job():
    logger.info("⏰ [SCHEDULER] Déclenchement automatique du pipeline ETL (Collect & Load)...")
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"❌ [SCHEDULER] Erreur lors de l'exécution du pipeline ETL : {e}")

def ingestion_job():
    logger.info("⏰ [SCHEDULER] Déclenchement automatique de l'ingestion RAG (Vectorisation)...")
    try:
        rag_pipeline.ingest_data()
    except Exception as e:
        logger.error(f"❌ [SCHEDULER] Erreur lors de l'exécution de l'ingestion RAG : {e}")

# Planification ETL à 21:00
schedule.every().day.at("21:00").do(etl_job)

# Planification Ingestion RAG à 22:00
schedule.every().day.at("22:00").do(ingestion_job)

logger.info("⏳ Scheduler démarré.")
logger.info("   - Pipeline ETL : tous les jours à 21:00")
logger.info("   - Ingestion RAG : tous les jours à 22:00")

# Boucle infinie pour maintenir le script en vie
while True:
    schedule.run_pending()
    time.sleep(60)
