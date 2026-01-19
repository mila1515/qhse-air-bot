
import sys
from pathlib import Path
# Add project root to python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import get_settings
import os

settings = get_settings()
print(f"Loaded LEGIFRANCE_API_KEY: {settings.LEGIFRANCE_API_KEY}")
print(f"First 4 chars: {settings.LEGIFRANCE_API_KEY[:4]}")
print(f"Is default? {settings.LEGIFRANCE_API_KEY == 'your_key_here'}")

# Check if .env exists
print(f".env exists: {os.path.exists('.env')}")
