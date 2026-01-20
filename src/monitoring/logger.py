import sys
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

# Handler Fichier (Rotation journalière, niveau DEBUG)
logger.add(
    LOG_DIR / "app.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    compression="zip"
)

# Exporter le logger configuré
__all__ = ["logger"]
