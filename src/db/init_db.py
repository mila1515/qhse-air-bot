from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.models import User
from src.api.security import get_password_hash
from src.monitoring.logger import logger

def init_db():
    """
    Initialise la base de données avec des données par défaut si nécessaire.
    Crée un utilisateur admin par défaut si aucun n'existe.
    """
    db: Session = SessionLocal()
    try:
        # Vérifier si l'admin existe déjà
        admin_email = "admin@gmail.com"
        user = db.query(User).filter(User.email == admin_email).first()
        
        if not user:
            logger.info(f"👤 Création de l'utilisateur admin par défaut : {admin_email}")
            hashed_password = get_password_hash("admin")
            admin_user = User(
                email=admin_email,
                hashed_password=hashed_password
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.info("✅ Utilisateur admin créé avec succès.")
        else:
            logger.info(f"✅ L'utilisateur admin {admin_email} existe déjà.")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation de la DB : {e}")
    finally:
        db.close()
