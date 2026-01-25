from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relation avec les conversations
    conversations = relationship("Conversation", back_populates="user")
    notes = relationship("Note", back_populates="user")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="notes")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="Nouvelle conversation")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    sender = Column(String)  # 'user' ou 'assistant'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    conversation = relationship("Conversation", back_populates="messages")


class ArticleCodeTravail(Base):
    __tablename__ = "articles_code_travail"

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
