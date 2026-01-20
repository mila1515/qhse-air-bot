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
    
    # External URLs (Public)
    CDTN_BASE_URL: str = "https://code.travail.gouv.fr/code-du-travail"
    INRS_BASE_URL: str = "https://www.inrs.fr"
    
    # API Keys & Tokens
    # LEGIFRANCE_API_KEY: str # Obsolète - Remplacé par Scraping CDTN
    # LEGIFRANCE_CLIENT_ID: str # Obsolète
    # LEGIFRANCE_CLIENT_SECRET: str # Obsolète
    WAQI_API_TOKEN: str

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    @property
    def DATABASE_URL(self) -> str:
        # Priorité à la variable d'environnement complète si elle existe
        import os
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            return env_url
            
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    
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
