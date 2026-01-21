from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_metrics_endpoint():
    """
    Vérifie que l'endpoint /metrics est accessible et renvoie des données Prometheus.
    """
    response = client.get("/metrics")
    assert response.status_code == 200
    
    # Vérification que le contenu ressemble à du format Prometheus
    assert "http_requests_total" in response.text or "starlette_requests_total" in response.text
    assert "# HELP" in response.text
    assert "# TYPE" in response.text
