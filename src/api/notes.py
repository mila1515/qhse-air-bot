from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.db.models import Note, User
from src.api import models as schemas
from src.api.auth import oauth2_scheme
from src.api.security import jwt, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/notes", tags=["Notes"])

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/", response_model=List[schemas.NoteRead])
def read_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Récupère toutes les notes de l'utilisateur connecté"""
    return db.query(Note).filter(Note.user_id == current_user.id).order_by(Note.updated_at.desc()).all()

@router.post("/", response_model=schemas.NoteRead)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Crée une nouvelle note"""
    new_note = Note(title=note.title, content=note.content, user_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Supprime une note"""
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
