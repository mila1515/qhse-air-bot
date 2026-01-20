from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator

from src.db.session import SessionLocal, engine
from src.db.models import Base, ArticleCodeTravail, GuideINRS, AccidentARIA, MesureWAQI
from src.api import models as schemas

# Création des tables (si pas encore fait)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QHSE Air Bot API",
    description="API REST pour consulter les données QHSE (Qualité Air, Réglementation, Accidents)",
    version="1.0.0"
)

# Instrumentation Prometheus (Métriques API)
print("DEBUG: Exposing metrics...")
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics", include_in_schema=True)
print("DEBUG: Metrics exposed.")

# Dépendance pour la session BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints de Base ---

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API QHSE Air Bot. Consultez /docs pour la documentation."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- Endpoints Métier (C5: API REST) ---

@app.get("/articles/", response_model=List[schemas.ArticleRead])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste des articles de loi (Code du Travail)"""
    articles = db.query(ArticleCodeTravail).offset(skip).limit(limit).all()
    return articles

@app.get("/guides/", response_model=List[schemas.GuideRead])
def read_guides(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère les guides INRS"""
    guides = db.query(GuideINRS).offset(skip).limit(limit).all()
    return guides

@app.get("/accidents/", response_model=List[schemas.AccidentRead])
def read_accidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère les accidents industriels (ARIA)"""
    accidents = db.query(AccidentARIA).offset(skip).limit(limit).all()
    return accidents

@app.get("/waqi/", response_model=List[schemas.WaqiRead])
def read_waqi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère les mesures de qualité de l'air"""
    measures = db.query(MesureWAQI).offset(skip).limit(limit).all()
    return measures

# --- Endpoint SQL Complexe (C2: Extraction SQL avancée) ---

@app.get("/stats/risks", response_model=List[schemas.RiskStats])
def get_risk_stats(db: Session = Depends(get_db)):
    """
    Agrégation SQL complexe : Compte le nombre de mesures par niveau de risque.
    Equivalent SQL : SELECT niveau_risque, COUNT(*) FROM mesures_waqi GROUP BY niveau_risque;
    """
    results = db.query(
        MesureWAQI.niveau_risque, 
        func.count(MesureWAQI.id).label("count")
    ).group_by(MesureWAQI.niveau_risque).all()
    
    return [{"niveau_risque": r[0], "count": r[1]} for r in results]
