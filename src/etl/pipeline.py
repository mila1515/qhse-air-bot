import time
import sys
import os

# Ajout du chemin racine au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.etl.collect import DataCollector
from src.etl.transform import DataTransformer
from src.etl.load import DataLoader
from src.monitoring.logger import logger
from src.monitoring.metrics import push_metrics, record_etl_success
from src.data_monitoring.drift.waqi_drift import run_waqi_drift
from src.data_monitoring.drift.aria_drift import run_aria_drift
from src.data_monitoring.quality.waqi_quality import run_waqi_quality
from src.data_monitoring.quality.aria_quality import run_aria_quality

def run_pipeline():
    """
    Exécute le pipeline ETL complet :
    1. Collecte (Sources -> Raw)
    2. Transformation (Raw -> Processed)
    3. Chargement (Processed -> Base de données)
    4. Monitoring (Analyse Qualité & Dérive -> Evidently)
    """
    logger.info("🚀 Démarrage du Pipeline ETL + Monitoring QHSE Air Bot")
    start_time = time.time()

    # --- Étape 1 : Collecte ---
    try:
        logger.info("📡 [ETL] Démarrage de la COLLECTE...")
        collector = DataCollector()
        collector.collect_code_travail()
        collector.collect_inrs()
        collector.collect_aria()
        collector.collect_waqi()
        logger.info("✅ [ETL] COLLECTE terminée.")
    except Exception as e:
        logger.error(f"❌ [ETL] Échec COLLECTE : {e}")
        return

    # --- Étape 2 : Transformation ---
    try:
        logger.info("🛠️ [ETL] Démarrage de la TRANSFORMATION...")
        transformer = DataTransformer()
        transformer.transform_code_travail()
        transformer.transform_inrs()
        transformer.transform_aria()
        transformer.transform_waqi()
        logger.info("✅ [ETL] TRANSFORMATION terminée.")
    except Exception as e:
        logger.error(f"❌ [ETL] Échec TRANSFORMATION : {e}")
        return

    # --- Étape 3 : Chargement ---
    try:
        logger.info("💾 [ETL] Démarrage du CHARGEMENT (Load)...")
        loader = DataLoader()
        loader.load_code_travail()
        loader.load_inrs()
        loader.load_waqi()
        loader.load_aria()
        loader.close()
        record_etl_success()
        logger.info("✅ [ETL] CHARGEMENT terminé.")
    except Exception as e:
        logger.error(f"❌ [ETL] Échec CHARGEMENT : {e}")
        return

    # --- Étape 4 : Monitoring (Evidently) ---
    try:
        logger.info("🕵️‍♂️ [MONITORING] Démarrage des analyses Evidently...")
        
        # Qualité (Quality)
        logger.info("   - Analyse Qualité WAQI...")
        run_waqi_quality()
        logger.info("   - Analyse Qualité ARIA...")
        run_aria_quality()

        # Dérive (Drift)
        logger.info("   - Analyse Dérive WAQI...")
        run_waqi_drift()
        logger.info("   - Analyse Dérive ARIA...")
        run_aria_drift()
        
        logger.info("✅ [MONITORING] Analyses terminées et envoyées au dashboard.")
    except Exception as e:
        logger.error(f"❌ [MONITORING] Échec des analyses : {e}")

    duration = time.time() - start_time
    logger.info(f"🎉 Pipeline complet terminé avec succès en {duration:.2f} secondes.")
    
    # Envoi des métriques à Prometheus via Pushgateway
    push_metrics()

if __name__ == "__main__":
    run_pipeline()
