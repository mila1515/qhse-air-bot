import pandas as pd
from pathlib import Path
from src.monitoring.logger import logger
from src.monitoring.metrics import record_processed_rows
import re

class DataTransformer:
    """Nettoyage et Transformation des données brutes"""
    
    def __init__(self):
        self.raw_dir = Path("data/raw")
        self.processed_dir = Path("data/processed")
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
    def transform_code_travail(self) -> pd.DataFrame:
        """Nettoie les articles du Code du Travail"""
        input_file = self.raw_dir / "code_travail.csv"
        if not input_file.exists():
            logger.warning("⚠️ Transform Code du Travail impossible: Fichier brut manquant")
            return pd.DataFrame()
            
        logger.info("🛠️ Transformation Code du Travail...")
        df = pd.read_csv(input_file)
        
        # Nettoyage
        df['titre'] = df['titre'].astype(str).str.strip()
        df['contenu'] = df['contenu'].astype(str).str.strip()
        
        # Ajout métadonnées
        df['type'] = "REGLEMENTATION"
        df['processed_at'] = pd.Timestamp.now()
        
        output_file = self.processed_dir / "code_travail_cleaned.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Code du Travail nettoyé: {len(df)} articles -> {output_file}")
        record_processed_rows('cdtn', 'transform', len(df))
        return df

    def transform_inrs(self) -> pd.DataFrame:
        """Nettoie les guides INRS"""
        input_file = self.raw_dir / "inrs.csv"
        if not input_file.exists():
            logger.warning("⚠️ Transform INRS impossible: Fichier brut manquant")
            return pd.DataFrame()
            
        logger.info("🛠️ Transformation INRS...")
        df = pd.read_csv(input_file)
        
        # Nettoyage
        df['titre'] = df['titre'].astype(str).str.strip()
        
        # Ajout métadonnées
        df['type'] = "GUIDE_PRACTIQUE"
        df['processed_at'] = pd.Timestamp.now()
        
        output_file = self.processed_dir / "inrs_cleaned.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"✅ INRS nettoyé: {len(df)} guides -> {output_file}")
        record_processed_rows('inrs', 'transform', len(df))
        return df

    def transform_aria(self) -> pd.DataFrame:
        """Nettoie les données accidents ARIA"""
        input_file = self.raw_dir / "aria_accidents.csv"
        if not input_file.exists():
            logger.warning("⚠️ Transform ARIA impossible: Fichier brut manquant")
            return pd.DataFrame()
            
        logger.info("🛠️ Transformation ARIA...")
        try:
            # Relecture avec les mêmes paramètres que le collect pour être sûr
            df = pd.read_csv(input_file)
            
            # Sélection et renommage des colonnes pertinentes (si elles existent)
            # Les colonnes ARIA peuvent varier, on essaie de normaliser
            # Exemple de colonnes standard ARIA: "Date de l'événement", "Commune", "Résumé"
            
            # Normalisation des noms de colonnes (minuscule, sans accent, sans espace)
            df.columns = [c.lower().replace(' ', '_').replace("'", "") for c in df.columns]
            
            # Gestion des dates (colonne souvent nommée 'date_de_levenement' ou 'date')
            date_col = next((c for c in df.columns if 'date' in c), None)
            if date_col:
                df['date_event'] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
            
            # Nettoyage texte
            text_cols = [c for c in df.columns if df[c].dtype == 'object']
            for col in text_cols:
                df[col] = df[col].astype(str).str.strip()

            # Ajout métadonnées
            df['type'] = "ACCIDENT_RETEX"
            df['processed_at'] = pd.Timestamp.now()
            
            output_file = self.processed_dir / "aria_cleaned.csv"
            df.to_csv(output_file, index=False)
            logger.info(f"✅ ARIA nettoyé: {len(df)} accidents -> {output_file}")
            record_processed_rows('aria', 'transform', len(df))
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur transformation ARIA: {e}")
            return pd.DataFrame()

    def transform_waqi(self) -> pd.DataFrame:
        """Nettoie et enrichit les données WAQI"""
        input_file = self.raw_dir / "waqi.csv"
        if not input_file.exists():
            logger.warning("⚠️ Transform WAQI impossible: Fichier brut manquant")
            return pd.DataFrame()
            
        logger.info("🛠️ Transformation WAQI...")
        df = pd.read_csv(input_file)
        
        # Conversion types
        numeric_cols = ['aqi', 'pm25', 'pm10', 'no2', 'o3', 'so2']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Ajout niveau de risque (Logique simple basée sur AQI)
        # 0-50: Bon, 51-100: Modéré, 101-150: Mauvais pour sensibles, 150+: Mauvais
        def get_risk_level(aqi):
            if pd.isna(aqi): return "INCONNU"
            if aqi <= 50: return "BON"
            if aqi <= 100: return "MODÉRÉ"
            if aqi <= 150: return "MAUVAIS_POUR_SENSIBLES"
            return "MAUVAIS"

        if 'aqi' in df.columns:
            df['niveau_risque'] = df['aqi'].apply(get_risk_level)
            
        # Recommandations automatiques
        def get_recommendation(risk):
            if risk == "BON": return "Qualité de l'air idéale pour les activités extérieures."
            if risk == "MODÉRÉ": return "Qualité acceptable. Aérez les locaux."
            if risk == "MAUVAIS_POUR_SENSIBLES": return "Réduisez l'exposition extérieure pour les personnes fragiles."
            if risk == "MAUVAIS": return "⚠️ Évitez les efforts intenses à l'extérieur. Port de masque recommandé si exposition prolongée."
            return "Pas de données."

        if 'niveau_risque' in df.columns:
            df['conseil_qhse'] = df['niveau_risque'].apply(get_recommendation)

        df['type'] = "QUALITE_AIR_TR"
        df['processed_at'] = pd.Timestamp.now()
        
        output_file = self.processed_dir / "waqi_cleaned.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"✅ WAQI nettoyé: {len(df)} relevés -> {output_file}")
        record_processed_rows('waqi', 'transform', len(df))
        return df

if __name__ == "__main__":
    transformer = DataTransformer()
    transformer.transform_code_travail()
    transformer.transform_inrs()
    transformer.transform_aria()
    transformer.transform_waqi()
