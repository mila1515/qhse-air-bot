import os
import logging
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.models import MesureWAQI, AccidentARIA, ArticleCodeTravail
from src.config import get_settings

# Configuration du logger spécifique pour ce module
logger = logging.getLogger(__name__)
settings = get_settings()

def ensure_data_dir():
    """
    Vérifie que le dossier de destination src/rag/data/api_data existe.
    Retourne le chemin absolu du dossier.
    """
    # On remonte de 3 niveaux depuis ce fichier : loader -> rag -> src -> root
    # Puis on redescend : src -> rag -> data -> api_data
    # Plus simple : chemin relatif par rapport au fichier actuel
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src/rag/loader
    rag_dir = os.path.dirname(current_dir) # src/rag
    data_dir = os.path.join(rag_dir, "data", "api_data")
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info(f"📁 Dossier créé : {data_dir}")
    
    return data_dir

def format_waqi(mesure: MesureWAQI) -> str:
    """Transforme une ligne WAQI en bloc texte structuré."""
    # Construction de la liste des polluants disponibles
    polluants = []
    if mesure.pm25 is not None: polluants.append(f"PM2.5={mesure.pm25}")
    if mesure.pm10 is not None: polluants.append(f"PM10={mesure.pm10}")
    if mesure.no2 is not None: polluants.append(f"NO2={mesure.no2}")
    if mesure.o3 is not None: polluants.append(f"O3={mesure.o3}")
    
    polluants_str = ", ".join(polluants) if polluants else "Non spécifié"

    return f"""---
SOURCE: WAQI
VILLE: {mesure.ville}
STATION: {mesure.station}
DATE: {mesure.date_collecte}
AQI: {mesure.aqi}
NIVEAU_RISQUE: {mesure.niveau_risque}
CONSEIL: {mesure.conseil_qhse}
POLLUANTS: {polluants_str}
---
"""

def format_aria(accident: AccidentARIA) -> str:
    """Transforme une ligne ARIA en bloc texte structuré."""
    return f"""---
SOURCE: ARIA
ID: {accident.id}
COMMUNE: {accident.commune} ({accident.departement})
TYPE: {accident.type_accident}
CAUSE: {accident.causes or 'Non spécifiée'}
CONSEQUENCES: {accident.contenu or 'Non spécifiées'}
DATE: {accident.date_event}
---
"""

def format_code_travail(article: ArticleCodeTravail) -> str:
    """Transforme un article du Code du Travail en bloc texte structuré."""
    return f"""---
SOURCE: CODE DU TRAVAIL
ARTICLE: {article.article_ref}
TITRE: {article.titre}
CONTENU: {article.contenu}
URL: {article.url}
---
"""

def export_db_to_txt():
    """
    Fonction principale d'export.
    Récupère les données de toutes les tables pertinentes et génère db_dump.txt.
    """
    logger.info("💾 Début de l'export des données SQL vers texte...")
    
    data_dir = ensure_data_dir()
    output_file = os.path.join(data_dir, "db_dump.txt")
    
    db: Session = SessionLocal()
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            # 1. Export WAQI (Qualité de l'air)
            # Récupère TOUTES les mesures, toutes villes confondues
            waqi_data = db.query(MesureWAQI).all()
            if waqi_data:
                logger.info(f"📊 Export WAQI : {len(waqi_data)} entrées trouvées.")
                for item in waqi_data:
                    f.write(format_waqi(item))
            else:
                logger.warning("⚠️ Aucune donnée WAQI trouvée en base.")

            # 2. Export ARIA (Accidents industriels)
            aria_data = db.query(AccidentARIA).all()
            if aria_data:
                logger.info(f"🏭 Export ARIA : {len(aria_data)} entrées trouvées.")
                for item in aria_data:
                    f.write(format_aria(item))
            else:
                logger.warning("⚠️ Aucune donnée ARIA trouvée en base.")

            # 3. Export Code du Travail
            articles = db.query(ArticleCodeTravail).all()
            if articles:
                logger.info(f"⚖️ Export Code du Travail : {len(articles)} entrées trouvées.")
                for item in articles:
                    f.write(format_code_travail(item))
            else:
                logger.warning("⚠️ Aucune donnée Code du Travail trouvée en base.")

        logger.info(f"✅ Export terminé avec succès : {output_file}")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'export DB : {e}")
        # On ne relève pas l'erreur pour ne pas bloquer tout le pipeline, 
        # mais le fichier risque d'être incomplet.
    finally:
        db.close()

if __name__ == "__main__":
    # Permet de tester le script isolément
    logging.basicConfig(level=logging.INFO)
    export_db_to_txt()
