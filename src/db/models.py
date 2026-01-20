from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Date
from sqlalchemy.sql import func
from src.db.session import Base

class ArticleLegifrance(Base):
    __tablename__ = "articles_legifrance"

    id = Column(Integer, primary_key=True, index=True)
    article_ref = Column(String, unique=True, index=True)
    titre = Column(String)
    contenu = Column(Text)
    url = Column(String)
    source = Column(String)
    date_collecte = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))

class GuideINRS(Base):
    __tablename__ = "guides_inrs"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    url = Column(String, unique=True)
    source = Column(String)
    date_collecte = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))

class AccidentARIA(Base):
    __tablename__ = "accidents_aria"

    id = Column(Integer, primary_key=True, index=True)
    date_event = Column(Date, nullable=True)
    commune = Column(String, nullable=True)
    departement = Column(String, nullable=True)
    type_accident = Column(String, nullable=True)
    matieres = Column(Text, nullable=True)
    contenu = Column(Text)
    causes = Column(Text, nullable=True)
    url = Column(String, nullable=True)
    processed_at = Column(DateTime(timezone=True))

class MesureWAQI(Base):
    __tablename__ = "mesures_waqi"

    id = Column(Integer, primary_key=True, index=True)
    date_collecte = Column(DateTime(timezone=True), server_default=func.now())
    ville = Column(String, index=True)
    station = Column(String)
    aqi = Column(Integer)
    niveau_risque = Column(String)
    conseil_qhse = Column(Text)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    no2 = Column(Float, nullable=True)
    o3 = Column(Float, nullable=True)
    processed_at = Column(DateTime(timezone=True))
