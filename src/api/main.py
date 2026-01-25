from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text

from src.db.session import engine, SessionLocal
from src.db.models import Base
from src.api import endpoints, auth, conversations, notes
from src.monitoring.api_metrics import DB_CONNECTION_STATUS

# Création des tables (si pas encore fait)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QHSE Air Bot API",
    description="API REST pour consulter les données QHSE (Qualité Air, Réglementation, Accidents)",
    version="1.0.0"
)

# Instrumentation Prometheus (Métriques API)
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics", include_in_schema=True)

# Inclusion des routes
app.include_router(auth.router)
app.include_router(conversations.router)
app.include_router(notes.router)
app.include_router(endpoints.router)

# --- Endpoints de Base ---

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API QHSE Air Bot. Consultez /docs pour la documentation."}

@app.get("/health")
def health_check():
    """Vérifie l'état de l'API et de la connexion BDD"""
    try:
        # Test de connexion DB simple (SELECT 1)
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        # Mise à jour de la métrique : 1 = OK
        DB_CONNECTION_STATUS.set(1)
        return {"status": "ok", "db": "connected"}
        
    except Exception as e:
        # Mise à jour de la métrique : 0 = KO
        DB_CONNECTION_STATUS.set(0)
        return {"status": "degraded", "db": "disconnected", "error": str(e)}
