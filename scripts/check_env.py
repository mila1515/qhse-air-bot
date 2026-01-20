
import sys
from pathlib import Path
# Add project root to python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import get_settings
import os

settings = get_settings()
print(f"Loaded APP_NAME: {settings.APP_NAME}")
print(f"Loaded CDTN_BASE_URL: {settings.CDTN_BASE_URL}")

# Check if .env exists
print(f".env exists: {os.path.exists('.env')}")
