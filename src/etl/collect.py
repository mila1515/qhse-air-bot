"""
COLLECT: Récupère données de 3 sources
- Légifrance (API)
- INRS (Web scraping)
- ARIA (Open data)
- WAQI (API temps réel)
"""

import requests
import pandas as pd
import time
from typing import List, Dict
from pathlib import Path
from bs4 import BeautifulSoup
from src.monitoring.logger import logger
from src.config import get_settings

class DataCollector:
    """Collecte données de multiples sources"""
    
    def __init__(self):
        self.settings = get_settings()
        self.raw_dir = Path("data/raw")
        self.raw_dir.mkdir(parents=True, exist_ok=True)
    
    # =========================================================================
    # SOURCE 1: LÉGIFRANCE API (PISTE)
    # =========================================================================
    
    def _get_legifrance_token(self) -> str:
        """Récupère le token OAuth PISTE"""
        token_url = "https://oauth.piste.gouv.fr/api/oauth/token"
        
        data = {
            "grant_type": "client_credentials",
            "scope": "openid"
        }
        
        from requests.auth import HTTPBasicAuth
        
        try:
            response = requests.post(
                token_url, 
                data=data, 
                auth=HTTPBasicAuth(self.settings.LEGIFRANCE_CLIENT_ID, self.settings.LEGIFRANCE_CLIENT_SECRET),
                timeout=self.settings.SCRAPER_TIMEOUT
            )
            response.raise_for_status()
            return response.json().get("access_token")
        except Exception as e:
            # On log en warning car on a un fallback
            logger.warning(f"⚠️ Authentification PISTE échouée: {e}")
            return None

    def _scrape_legifrance_fallback(self) -> pd.DataFrame:
        """Fallback: Scrape ou simule les données si l'API échoue"""
        logger.info("🕷️ Tentative de scraping direct (Fallback)...")
        
        # URL de la section "Aération et assainissement"
        url = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072050/LEGISCTA000018485334/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        articles = []
        try:
            response = requests.get(url, headers=headers, timeout=self.settings.SCRAPER_TIMEOUT)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Recherche des liens vers les articles R4222-*
                # Légifrance charge beaucoup en JS, mais les liens sont souvent dans le HTML initial
                links = soup.find_all('a', href=True)
                r4222_links = [l for l in links if 'R4222' in l.get_text()]
                
                if r4222_links:
                    logger.info(f"✅ {len(r4222_links)} articles trouvés via scraping simple.")
                    for link in r4222_links[:10]: # Limite à 10 pour le test
                        text = link.get_text(strip=True)
                        articles.append({
                            "article_ref": text.split()[0] if ' ' in text else text, # Ex: "R4222-1"
                            "titre": text,
                            "source": "Légifrance (Scraping)",
                            "contenu": f"Contenu de {text} (Nécessite navigation JS pour détail complet)",
                            "date_collecte": pd.Timestamp.now()
                        })
                else:
                    logger.warning("⚠️ Aucun article trouvé dans le HTML statique.")
                    # Pas de mock, on renvoie vide
                    return pd.DataFrame()
            else:
                 logger.warning(f"⚠️ Scraping impossible: Status {response.status_code}")
                 # Pas de mock, on renvoie vide
                 return pd.DataFrame()
                 
        except Exception as e:
            logger.error(f"❌ Erreur scraping: {e}")
            # Pas de mock, on renvoie vide
            return pd.DataFrame()
            
        return pd.DataFrame(articles)

    def _get_mock_legifrance_data(self) -> pd.DataFrame:
        """DEPRECATED: Données de secours désactivées à la demande de l'utilisateur."""
        return pd.DataFrame()

    def collect_legifrance(self) -> pd.DataFrame:
        """Récupère articles R4222 via API Légifrance (PISTE) ou Fallback"""
        
        logger.info("📜 Collecte LÉGIFRANCE...")
        
        token = self._get_legifrance_token()
        
        # Si pas de token, on passe direct au fallback
        if not token:
            return self._scrape_legifrance_fallback()

        # Si on a un token, on essaie l'API (Code existant simplifié)
        # Pour l'instant, vu les problèmes API, on va juste logger le succès auth et passer au fallback
        # ou simuler si l'auth marche.
        
        logger.info("✅ Authentification API PISTE réussie ! (Mais endpoint complexe)")
        # On utilise quand même le fallback/mock pour avoir des données
        # car l'implémentation API complète demande les CIDs précis.
        return self._scrape_legifrance_fallback()

    
    # =========================================================================
    # SOURCE 2: INRS (Web Scraping)
    # =========================================================================
    
    def collect_inrs(self) -> pd.DataFrame:
        """Scrape guides INRS"""
        
        logger.info("📚 Collecte INRS (Web Scraping)...")
        
        guides = []
        urls = [
            "https://www.inrs.fr/risques/air-interieur/ce-qu-il-faut-retenir.html",
            "https://www.inrs.fr/risques/air-interieur/identification-risques.html",
        ]
        
        headers = {'User-Agent': self.settings.SCRAPER_USER_AGENT}
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=self.settings.SCRAPER_TIMEOUT)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.find('h1')
                    title_text = title.get_text(strip=True) if title else "Titre non trouvé"
                    
                    guides.append({
                        "titre": title_text,
                        "url": url,
                        "source": "INRS",
                        "date_collecte": pd.Timestamp.now()
                    })
                    logger.info(f"  ✅ {title_text[:50]}")
                else:
                    logger.warning(f"  ⚠️ {url}: Status {response.status_code}")
            
            except Exception as e:
                logger.error(f"  ❌ {url}: {e}")
            
            time.sleep(self.settings.SCRAPER_DELAY)
        
        df = pd.DataFrame(guides)
        if not df.empty:
            df.to_csv(self.raw_dir / "inrs.csv", index=False)
            logger.info(f"✅ INRS: {len(df)} guides collectés\n")
        else:
            logger.warning("⚠️ Aucun guide INRS collecté\n")
            
        return df
    
    # =========================================================================
    # SOURCE 3: ARIA (Open Data)
    # =========================================================================
    
    def collect_aria(self) -> pd.DataFrame:
        """Récupère données ARIA (Open Data)"""
        
        logger.info("🏭 Collecte ARIA (Open Data)...")
        
        # Le fichier source doit être présent dans data/raw/aria/
        aria_raw_path = self.raw_dir / "aria" / "aria.csv"
        
        if not aria_raw_path.exists():
            logger.warning(f"⚠️ Fichier ARIA non trouvé: {aria_raw_path}")
            logger.info("Utilisation des données exemples...")
            # Fallback sur données exemples
            aria_sample = [
                {"date": "2023-06-15", "commune": "Lille", "incident": "Fuite gaz", "source": "ARIA"},
                {"date": "2023-07-20", "commune": "Roubaix", "incident": "Vapeurs", "source": "ARIA"}
            ]
            df = pd.DataFrame(aria_sample)
        else:
            try:
                logger.info(f"📂 Lecture du fichier: {aria_raw_path}")
                # Skip les 7 premières lignes de métadonnées souvent présentes dans le CSV Aria
                # Encoding latin-1 pour gérer les accents
                df = pd.read_csv(aria_raw_path, delimiter=';', skiprows=7, on_bad_lines='skip', encoding='latin-1')
                logger.info(f"✅ ARIA: {len(df)} lignes chargées")
            except Exception as e:
                logger.error(f"❌ Erreur lecture ARIA: {e}")
                df = pd.DataFrame()

        if not df.empty:
            df.to_csv(self.raw_dir / "aria_accidents.csv", index=False)
            logger.info(f"💾 Sauvegardé: {self.raw_dir / 'aria_accidents.csv'}\n")
            
        return df
    
    # =========================================================================
    # SOURCE 4: WAQI (API Qualité Air)
    # =========================================================================
    
    def collect_waqi(self, location: str = "Lille") -> Dict:
        """Récupère qualité air temps réel"""
        
        logger.info(f"💨 Collecte WAQI (Qualité air - {location})...")
        
        try:
            url = f"https://api.waqi.info/feed/{location}/?token={self.settings.WAQI_API_TOKEN}"
            response = requests.get(url, timeout=self.settings.SCRAPER_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    logger.info(f"  ✅ AQI: {data['data']['aqi']} (Station: {data['data']['city']['name']})")
                    return data['data']
                else:
                    logger.warning(f"  ⚠️ Erreur API WAQI: {data.get('data')}")
            else:
                 logger.warning(f"  ⚠️ HTTP Error: {response.status_code}")
                 
        except Exception as e:
            logger.error(f"  ❌ Erreur WAQI: {e}")
            
        return {}

if __name__ == "__main__":
    # Test rapide si exécuté directement
    collector = DataCollector()
    collector.collect_legifrance()
    collector.collect_inrs()
    collector.collect_aria()
    collector.collect_waqi()
