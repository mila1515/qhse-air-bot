import time
import schedule
import sys
import os

# Ajout du chemin racine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.etl.pipeline import run_pipeline
from src.monitoring.logger import logger

def job():
    logger.info("⏰ [SCHEDULER] Déclenchement automatique du pipeline journalier...")
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"❌ [SCHEDULER] Erreur lors de l'exécution du pipeline : {e}")

# Planification à 22:00
schedule.every().day.at("22:00").do(job)

logger.info("⏳ Scheduler démarré. Le pipeline tournera chaque jour à 22:00.")

# Boucle infinie pour maintenir le script en vie
while True:
    schedule.run_pending()
    time.sleep(60)
