from sqlalchemy import text
from src.db.session import SessionLocal

def test_db_connection():
    """
    Vérifie que la connexion à la base de données fonctionne.
    Nécessite que le conteneur Postgres soit lancé.
    """
    try:
        db = SessionLocal()
        # Exécuter une requête simple "SELECT 1" pour valider la connexion
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
        db.close()
    except Exception as e:
        # On fail le test avec un message clair si la DB n'est pas accessible
        import pytest
        pytest.fail(f"Échec connexion DB. Assurez-vous que Docker est lancé (docker-compose up -d postgres). Erreur: {e}")
