from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from src.db.session import get_db
from src.db.models import ArticleCodeTravail, GuideINRS, AccidentARIA, MesureWAQI
from src.api import models as schemas

router = APIRouter()

# --- Endpoints Métier (C5: API REST) ---

@router.get("/articles/", response_model=List[schemas.ArticleRead])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste des articles de loi (Code du Travail)"""
    articles = db.query(ArticleCodeTravail).offset(skip).limit(limit).all()
    return articles

@router.get("/guides/", response_model=List[schemas.GuideRead])
def read_guides(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère les guides INRS"""
    guides = db.query(GuideINRS).offset(skip).limit(limit).all()
    return guides

@router.get("/accidents/", response_model=List[schemas.AccidentRead])
def read_accidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère les accidents industriels (ARIA)"""
    accidents = db.query(AccidentARIA).offset(skip).limit(limit).all()
    return accidents

@router.get("/waqi/", response_model=List[schemas.WaqiRead])
def read_waqi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère les mesures de qualité de l'air"""
    measures = db.query(MesureWAQI).offset(skip).limit(limit).all()
    return measures

# --- Endpoint SQL Complexe (C2: Extraction SQL avancée) ---

@router.get("/stats/risks", response_model=List[schemas.RiskStats])
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
