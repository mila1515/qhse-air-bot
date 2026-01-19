from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "QHSE Chatbot API"
    DEBUG: bool = True
    
    # Scraper Config
    SCRAPER_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    SCRAPER_TIMEOUT: int = 10
    SCRAPER_DELAY: int = 2
    
    # API Keys & Tokens
    LEGIFRANCE_API_KEY: str = "your_key_here"  # Token OAuth (access_token)
    LEGIFRANCE_CLIENT_ID: str = ""
    LEGIFRANCE_CLIENT_SECRET: str = ""
    WAQI_API_TOKEN: str = "demo"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings():
    return Settings()
