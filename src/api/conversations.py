from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.db.models import Conversation, Message, User
from src.api import models as schemas
from src.api.auth import get_current_user
from sqlalchemy.sql import func
from src.rag.pipeline.rag_chain import rag_pipeline

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.get("/", response_model=List[schemas.ConversationRead])
def get_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Récupère toutes les conversations de l'utilisateur connecté"""
    return db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.updated_at.desc()).all()

@router.get("/{conversation_id}", response_model=schemas.ConversationRead)
def get_conversation(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Récupère les détails d'une conversation"""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@router.post("/", response_model=schemas.ConversationRead)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Crée une nouvelle conversation"""
    new_conv = Conversation(title=conversation.title, user_id=current_user.id)
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)
    return new_conv

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Supprime une conversation"""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conv)
    db.commit()
    return {"message": "Conversation deleted"}

@router.patch("/{conversation_id}", response_model=schemas.ConversationRead)
def update_conversation(
    conversation_id: int, 
    conversation_update: schemas.ConversationUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Met à jour une conversation (titre ou statut)"""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation_update.title is not None:
        setattr(conv, 'title', conversation_update.title)
    if conversation_update.status is not None:
        setattr(conv, 'status', conversation_update.status)
    
    conv.updated_at = func.now()
    db.commit()
    db.refresh(conv)
    return conv

@router.get("/{conversation_id}/history", response_model=List[schemas.MessageRead])
def get_conversation_history(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Récupère l'historique des messages d'une conversation"""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()

@router.post("/{conversation_id}/messages", response_model=schemas.MessageRead)
def add_message(conversation_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Ajoute un message à une conversation (interne, pour l'historique)"""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    new_msg = Message(content=message.content, sender=message.sender, conversation_id=conversation_id)
    db.add(new_msg)
    # Met à jour la date de modif de la conversation
    conv.updated_at = func.now()
    
    db.commit()
    db.refresh(new_msg)
    return new_msg

@router.post("/{conversation_id}/chat", response_model=schemas.MessageRead)
def chat_conversation(
    conversation_id: int, 
    query: schemas.ChatQuery, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Envoie un message dans une conversation, obtient la réponse RAG, et sauvegarde le tout.
    """
    # 1. Vérifier la conversation
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # 2. Sauvegarder le message de l'utilisateur
    user_msg = Message(content=query.question, sender="user", conversation_id=conversation_id)
    db.add(user_msg)
    
    # 3. Appeler le pipeline RAG
    try:
        # Note: rag_pipeline.query might take time.
        rag_response = rag_pipeline.query(query.question)
    except Exception as e:
        # En cas d'erreur RAG, on peut soit échouer, soit répondre une erreur
        rag_response = f"Désolé, je n'ai pas pu traiter votre demande. Erreur: {str(e)}"
    
    # 4. Sauvegarder la réponse de l'assistant
    bot_msg = Message(content=rag_response, sender="assistant", conversation_id=conversation_id)
    db.add(bot_msg)
    
    # 5. Mise à jour du titre si "Nouvelle conversation"
    if conv.title == "Nouvelle conversation" or conv.title == "Nouvelle discussion":
        # Générer un titre court (max 50 chars) à partir de la question
        # Option simple : tronquer
        new_title = (query.question[:47] + "...") if len(query.question) > 47 else query.question
        conv.title = new_title

    # 6. Mettre à jour la date de la conversation
    conv.updated_at = func.now()
    
    db.commit()
    db.refresh(bot_msg)
    
    return bot_msg
