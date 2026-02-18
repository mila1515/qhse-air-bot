import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from src.db.session import SessionLocal, engine, Base
from src.db.models import ArticleCodeTravail, GuideINRS, AccidentARIA, MesureWAQI
from src.monitoring.logger import logger
from src.monitoring.metrics import record_processed_rows, record_etl_success, update_aqi_gauge

class DataLoader:
    """Charge les données transformées en base de données"""
    
    def __init__(self):
        self.processed_dir = Path("data/processed")
        # Création des tables si elles n'existent pas
        Base.metadata.create_all(bind=engine)
        self.db: Session = SessionLocal()

    def load_code_travail(self):
        """Charge les articles Code du Travail"""
        input_file = self.processed_dir / "code_travail_cleaned.csv"
        if not input_file.exists(): return

        logger.info("💾 Chargement Code du Travail en BDD...")
        df = pd.read_csv(input_file)
        
        count = 0
        for _, row in df.iterrows():
            # Upsert (Insert ou Update si existe déjà)
            existing = self.db.query(ArticleCodeTravail).filter_by(article_ref=row['article_ref']).first()
            
            data = {
                "article_ref": row['article_ref'],
                "titre": row['titre'],
                "contenu": row['contenu'],
                "url": row['url'],
                "source": row['source'],
                "processed_at": pd.to_datetime(row['processed_at'])
            }
            
            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                article = ArticleCodeTravail(**data)
                self.db.add(article)
                count += 1
        
        self.db.commit()
        logger.info(f"✅ Code du Travail: {count} nouveaux articles insérés (Total traité: {len(df)})")
        record_processed_rows('cdtn', 'load', count)

    def load_inrs(self):
        """Charge les guides INRS"""
        input_file = self.processed_dir / "inrs_cleaned.csv"
        if not input_file.exists(): return

        logger.info("💾 Chargement INRS en BDD...")
        df = pd.read_csv(input_file)
        
        count = 0
        for _, row in df.iterrows():
            existing = self.db.query(GuideINRS).filter_by(url=row['url']).first()
            
            data = {
                "titre": row['titre'],
                "url": row['url'],
                "source": row['source'],
                "processed_at": pd.to_datetime(row['processed_at'])
            }
            
            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                guide = GuideINRS(**data)
                self.db.add(guide)
                count += 1
                
        self.db.commit()
        logger.info(f"✅ INRS: {count} nouveaux guides insérés")
        record_processed_rows('inrs', 'load', count)

    def load_aria(self):
        """Charge les accidents ARIA"""
        input_file = self.processed_dir / "aria_cleaned.csv"
        if not input_file.exists(): return

        logger.info("💾 Chargement ARIA en BDD (Cela peut prendre un peu de temps)...")
        df = pd.read_csv(input_file)
        
        # Pour ARIA, on ne charge que les nouveaux pour éviter les doublons massifs
        # (Simplification: On vide et recharge ou on vérifie juste les derniers ?)
        # Ici stratégie simple: on insère tout en batch, idéalement il faudrait une clé unique (numéro_aria)
        # Mais le CSV Aria est parfois sale. On va supposer que 'url' ou une combinaison est unique
        # Pour l'instant, on insert massivement les 100 derniers pour l'exemple pour ne pas saturer
        
        # On prend les 1000 plus récents pour la démo
        df_recent = df.head(1000) 
        
        objects = []
        for _, row in df_recent.iterrows():
            # Gestion des dates
            date_evt = pd.to_datetime(row['date_event'], errors='coerce')
            if pd.isna(date_evt):
                date_evt = None
            
            objects.append(AccidentARIA(
                date_event=date_evt,
                commune=str(row.get('commune', ''))[:255],
                departement=str(row.get('departement', row.get('départment', '')))[:50],
                type_accident=str(row.get('type_accident', row.get('type_daccident', '')))[:255],
                matieres=str(row.get('matieres', row.get('matières', ''))),
                contenu=str(row.get('contenu', '')),
                causes=str(row.get('causes_profondes', '')),
                url=str(row.get('url', '')),
                processed_at=pd.to_datetime(row['processed_at'])
            ))
            
        # Bulk insert est plus rapide
        # Attention: pour la prod, gérer les doublons
        self.db.bulk_save_objects(objects)
        self.db.commit()
        logger.info(f"✅ ARIA: {len(objects)} accidents insérés (Batch)")
        record_processed_rows('aria', 'load', len(objects))

    def load_waqi(self):
        """Charge les données WAQI"""
        input_file = self.processed_dir / "waqi_cleaned.csv"
        if not input_file.exists(): return

        logger.info("💾 Chargement WAQI en BDD...")
        df = pd.read_csv(input_file)
        
        objects = []
        for _, row in df.iterrows():
            objects.append(MesureWAQI(
                ville=row['ville_recherchee'],
                station=row['station_nom'],
                aqi=row['aqi'],
                niveau_risque=row['niveau_risque'],
                conseil_qhse=row['conseil_qhse'],
                pm25=row['pm25'] if pd.notna(row['pm25']) else None,
                pm10=row['pm10'] if pd.notna(row['pm10']) else None,
                no2=row['no2'] if pd.notna(row['no2']) else None,
                o3=row['o3'] if pd.notna(row['o3']) else None,
                processed_at=pd.to_datetime(row['processed_at'])
            ))
            
            # Mise à jour métrique AQI temps réel
            update_aqi_gauge(row['ville_recherchee'], row['aqi'])
            
        self.db.add_all(objects)
        self.db.commit()
        logger.info(f"✅ WAQI: {len(objects)} relevés insérés")
        record_processed_rows('waqi', 'load', len(objects))

    def close(self):
        self.db.close()

if __name__ == "__main__":
    loader = DataLoader()
    try:
        loader.load_code_travail() # Correction nom méthode
        loader.load_inrs()
        loader.load_waqi()
        loader.load_aria()
        record_etl_success() # Métrique succès global
    finally:
        loader.close()
