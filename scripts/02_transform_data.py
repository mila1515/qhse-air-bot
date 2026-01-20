"""
Script d'exécution de la transformation des données (ETL - Step 2: Transform)
Utilise le module src.etl.transform
"""

import sys
import os
from pathlib import Path

# Ajout du dossier racine au path pour les imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.etl.transform import DataTransformer
from src.monitoring.logger import logger

def main():
    logger.info("🚀 Démarrage du script de transformation...")
    
    try:
        transformer = DataTransformer()
        
        # Exécution des transformations
        transformer.transform_code_travail()
        transformer.transform_inrs()
        transformer.transform_aria()
        transformer.transform_waqi()
        
        logger.info("🎉 Transformation terminée avec succès !")
        
    except Exception as e:
        logger.error(f"❌ Erreur critique lors de la transformation : {e}")
        raise e

if __name__ == "__main__":
    main()
