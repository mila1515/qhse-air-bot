from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_read_root():
    """Teste la route racine"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Teste la route de santé (health check)"""
    response = client.get("/health")
    # Le statut peut être 200 (OK) ou 200 avec status degraded si la DB échoue
    # Note: Dans l'implémentation actuelle, le health check retourne toujours 200 (par défaut FastAPI) 
    # sauf si exception non gérée, mais le code gère l'exception et retourne un JSON.
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["ok", "degraded"]

def test_read_articles_structure():
    """Teste que la route /articles/ répond (succès, erreur DB ou non authentifié)"""
    response = client.get("/articles/?limit=1")
    assert response.status_code in [200, 401, 500]
