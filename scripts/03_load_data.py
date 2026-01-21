"""
Script d'exécution du chargement des données (ETL - Step 3: Load)
Utilise le module src.etl.load
"""

import sys
from pathlib import Path

# Ajout du dossier racine au path pour les imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Force l'encodage UTF-8 pour la console Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from src.etl.load import DataLoader
from src.monitoring.logger import logger
from src.monitoring.metrics import push_metrics, record_etl_success

def main():
    logger.info("🚀 Démarrage du script de chargement (Load)...")
    
    try:
        loader = DataLoader()
        
        # Exécution des chargements
        loader.load_code_travail()
        loader.load_inrs()
        loader.load_waqi()
        loader.load_aria()
        
        record_etl_success()
        loader.close()
        logger.info("🎉 Chargement terminé avec succès !")
        
    except Exception as e:
        logger.error(f"❌ Erreur critique lors du chargement : {e}")
        raise e
    finally:
        push_metrics()

if __name__ == "__main__":
    main()
