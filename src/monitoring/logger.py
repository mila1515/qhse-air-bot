import sys
import os
from loguru import logger
from pathlib import Path

# Configurer les chemins
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configuration du logger
logger.remove()  # Supprimer le handler par défaut

# Handler Console (Couleur, niveau INFO)
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Récupérer le nom du service depuis les variables d'environnement (défini dans docker-compose)
service_name = os.getenv("SERVICE_NAME", "app")

# Handler Fichier (Rotation journalière, niveau DEBUG)
# Chaque service aura son propre fichier de log (api.log, scheduler.log, frontend.log)
logger.add(
    LOG_DIR / f"{service_name}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    compression="zip"
)

# Exporter le logger configuré
__all__ = ["logger"]
