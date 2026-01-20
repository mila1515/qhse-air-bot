"""
COLLECT: Récupère données de 3 sources
- Code du Travail (Scraping CDTN)
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
    # SOURCE 1: CODE DU TRAVAIL NUMÉRIQUE (API CDTN)
    # Remplaçant de l'API précédente
    # =========================================================================
    
    def collect_code_travail(self) -> pd.DataFrame:
        """Récupère articles R4222 via Scraping Code du Travail Numérique (HTML)"""
        
        logger.info("📜 Collecte Articles (via Scraping code.travail.gouv.fr)...")
        
        base_url = self.settings.CDTN_BASE_URL
        
        articles_cibles = [
            # Aération / Assainissement
            "R4222-1", "R4222-2", "R4222-3", "R4222-4", "R4222-5",
            "R4222-6", "R4222-10", "R4222-11", "R4222-12", "R4222-13",
            "R4222-14", "R4222-15", "R4222-16", "R4222-17", "R4222-18",
            "R4222-19", "R4222-20", "R4222-21", "R4222-22", "R4222-23",
            "R4222-24", "R4222-25", "R4222-26",
            
            # Ambiance physique (Lumière/Aération/Bruit lié aux locaux)
            "R4212-1", "R4212-2", "R4212-3", "R4212-4", "R4212-5", "R4212-6", "R4212-7",

            # Risques Chimiques & VLEP (Seuils)
            "R4412-149", "R4412-150", "R4412-152", "R4412-154",
            
            # Poussières
            "R4412-156", "R4412-157", "R4412-158", "R4412-159", "R4412-160",
            
            # Amiante
            "R4412-97"
        ]
        
        data_collected = []
        headers = {'User-Agent': self.settings.SCRAPER_USER_AGENT}
        
        for art_ref in articles_cibles:
            url = f"{base_url}/{art_ref.lower()}"
            
            try:
                response = requests.get(url, headers=headers, timeout=self.settings.SCRAPER_TIMEOUT)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extraction du titre
                    titre_tag = soup.find('h1')
                    titre = titre_tag.get_text(strip=True) if titre_tag else f"Article {art_ref}"
                    
                    # Extraction du contenu (souvent dans une div spécifique sur CDTN)
                    # CDTN structure change parfois, on cherche large
                    content_div = soup.find('div', class_=lambda x: x and 'html' in x) or soup.find('main')
                    
                    if content_div:
                        contenu = content_div.get_text(strip=True)[:1000] # On limite la taille
                        
                        data_collected.append({
                            "article_ref": art_ref,
                            "titre": titre,
                            "contenu": contenu,
                            "url": url,
                            "source": "CDTN (Scraping Web)",
                            "date_collecte": pd.Timestamp.now()
                        })
                        logger.info(f"  ✅ {art_ref} trouvé")
                    else:
                        logger.warning(f"  ⚠️ Contenu non trouvé pour {art_ref}")
                else:
                    logger.warning(f"  ⚠️ Erreur {response.status_code} pour {url}")
                    
            except Exception as e:
                logger.error(f"  ❌ Erreur {art_ref}: {e}")
                
            time.sleep(0.5)

        df = pd.DataFrame(data_collected)
        
        if not df.empty:
            df.to_csv(self.raw_dir / "code_travail.csv", index=False)
            logger.info(f"✅ Code du Travail: {len(df)} articles collectés via CDTN Web\n")
        else:
            logger.warning("⚠️ Aucun article collecté via CDTN Web.\n")
        
        return df

    # Méthodes obsolètes (supprimées)
    # def _get_code_travail_token(self): pass
    # def _scrape_code_travail_fallback(self): pass
    # def _get_mock_code_travail_data(self): pass

    
    # =========================================================================
    # SOURCE 2: INRS (Web Scraping)
    # =========================================================================
    
    def collect_inrs(self) -> pd.DataFrame:
        """Récupère guides INRS via Web Scraping"""
        
        logger.info("📚 Collecte Guides INRS (via Scraping)...")
        
        guides = []
        base_url = self.settings.INRS_BASE_URL
        
        # URLs de départ pour la recherche de guides
        urls = [
            f"{base_url}/risques/aeration-assainissement-locaux-travail/ce-qu-il-faut-retenir.html",
            f"{base_url}/risques/chimiques/ce-qu-il-faut-retenir.html",
            f"{base_url}/risques/bruit/ce-qu-il-faut-retenir.html",
            f"{base_url}/risques/biologiques/ce-qu-il-faut-retenir.html"
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
    
    def collect_waqi(self, cities: List[str] = None) -> pd.DataFrame:
        """
        Récupère qualité air temps réel pour une liste de villes.
        API: https://aqicn.org/api/
        """
        if cities is None:
            cities = ["Paris", "Marseille", "Lyon", "Lille", "Toulouse", "Nice", "Nantes", "Strasbourg", "Bordeaux", "Rennes"]

        logger.info(f"💨 Collecte WAQI (Qualité air) pour {len(cities)} villes...")
        
        data_collected = []
        
        for city in cities:
            try:
                # Utilisation du endpoint search pour trouver la station la plus pertinente ou feed direct
                # Feed direct est plus simple: feed/:city/?token=:token
                url = f"https://api.waqi.info/feed/{city}/?token={self.settings.WAQI_API_TOKEN}"
                response = requests.get(url, timeout=self.settings.SCRAPER_TIMEOUT)
                
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json.get("status") == "ok":
                        data = res_json['data']
                        
                        # Extraction des polluants spécifiques (iaqi)
                        iaqi = data.get('iaqi', {})
                        
                        entry = {
                            "date_collecte": pd.Timestamp.now(),
                            "ville_recherchee": city,
                            "station_nom": data.get('city', {}).get('name'),
                            "aqi": data.get('aqi'), # Indice global
                            "pm25": iaqi.get('pm25', {}).get('v'),
                            "pm10": iaqi.get('pm10', {}).get('v'),
                            "no2": iaqi.get('no2', {}).get('v'),
                            "o3": iaqi.get('o3', {}).get('v'),
                            "so2": iaqi.get('so2', {}).get('v'),
                            "url_source": data.get('city', {}).get('url'),
                            "lat": data.get('city', {}).get('geo', [None, None])[0],
                            "lon": data.get('city', {}).get('geo', [None, None])[1]
                        }
                        data_collected.append(entry)
                        logger.info(f"  ✅ {city}: AQI={entry['aqi']}")
                    else:
                        logger.warning(f"  ⚠️ {city}: Erreur API ({res_json.get('data')})")
                else:
                     logger.warning(f"  ⚠️ {city}: HTTP Error {response.status_code}")
                
                time.sleep(0.5) # Respect rate limits
                     
            except Exception as e:
                logger.error(f"  ❌ Erreur WAQI {city}: {e}")
            
        df = pd.DataFrame(data_collected)
        
        if not df.empty:
            df.to_csv(self.raw_dir / "waqi.csv", index=False)
            logger.info(f"✅ WAQI: Données collectées pour {len(df)} villes -> {self.raw_dir / 'waqi.csv'}\n")
        else:
            logger.warning("⚠️ Aucune donnée WAQI collectée.\n")
            
        return df

if __name__ == "__main__":
    # Test rapide si exécuté directement
    collector = DataCollector()
    collector.collect_legifrance()
    collector.collect_inrs()
    collector.collect_aria()
    collector.collect_waqi()
