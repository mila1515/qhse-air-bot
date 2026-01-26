from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Union
from datetime import datetime, date

# --- Schémas pour la documentation API (Swagger/OpenAPI) ---

class MessageBase(BaseModel):
    content: str
    sender: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ConversationBase(BaseModel):
    title: str
    status: Optional[str] = "active"

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None

class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# 0. Auth & Users
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# 1. Schémas de base (communs lecture/écriture)

class ArticleBase(BaseModel):
    article_ref: str
    titre: str
    contenu: str
    url: Optional[str] = None
    source: str

class GuideBase(BaseModel):
    titre: str
    url: str
    source: str

class AccidentBase(BaseModel):
    date_event: Optional[Union[date, str]] = None
    commune: Optional[str] = None
    type_accident: Optional[str] = None
    matieres: Optional[str] = None
    contenu: Optional[str] = None
    causes: Optional[str] = None

class WaqiBase(BaseModel):
    ville: str
    station: str
    aqi: int
    niveau_risque: str
    conseil_qhse: str
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    no2: Optional[float] = None
    o3: Optional[float] = None

# 2. Schémas de Lecture (incluent l'ID et les métadonnées)

class ArticleRead(ArticleBase):
    id: int
    processed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class GuideRead(GuideBase):
    id: int
    processed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class AccidentRead(AccidentBase):
    id: int
    processed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class WaqiRead(WaqiBase):
    id: int
    processed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# 3. Schémas pour les Statistiques (Complex SQL)
class RiskStats(BaseModel):
    niveau_risque: str
    count: int

# 4. Schémas pour le RAG (Chatbot)
class ChatQuery(BaseModel):
    question: str

class ChatResponse(BaseModel):
    question: str
    answer: str
    timestamp: datetime = datetime.now()
