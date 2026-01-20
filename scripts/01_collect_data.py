"""
Script d'exécution de la collecte des données (ETL - Step 1: Collect)
Utilise le module src.etl.collect
"""

import sys
import os
from pathlib import Path

# Ajout du dossier racine au path pour les imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.etl.collect import DataCollector
from src.monitoring.logger import logger

def main():
    logger.info("🚀 Démarrage du script de collecte...")
    
    try:
        collector = DataCollector()
        
        # 1. Légifrance
        collector.collect_legifrance()
        
        # 2. INRS
        collector.collect_inrs()
        
        # 3. ARIA
        collector.collect_aria()
        
        # 4. WAQI (Qualité Air)
        collector.collect_waqi()
        
        logger.info("🎉 Collecte terminée avec succès !")
        
    except Exception as e:
        logger.error(f"❌ Erreur critique lors de la collecte : {e}")
        raise e

if __name__ == "__main__":
    main()
