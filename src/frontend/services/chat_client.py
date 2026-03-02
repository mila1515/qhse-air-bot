import httpx
from src.config import get_settings
from src.monitoring.logger import logger

settings = get_settings()

class ChatClient:
    def __init__(self):
        self.api_url = f"http://localhost:8000/api/v1/rag/chat"
        # Timeout étendu pour les réponses RAG (120s)
        self.timeout = 120.0

    def send_chat_message(self, message: str, token: str) -> dict:
        """Envoie un message au backend RAG."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    self.api_url,
                    json={"question": message},
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    return {
                        "answer": "🔒 Votre session a expiré. Veuillez vous reconnecter.",
                        "sources": []
                    }
                else:
                    logger.error(f"Erreur API ({response.status_code}): {response.text}")
                    return {
                        "answer": f"⚠️ Erreur serveur ({response.status_code}). Veuillez réessayer.",
                        "sources": []
                    }

        except httpx.ReadTimeout:
            logger.error("❌ Timeout lors de la requête API.")
            return {
                "answer": "⚠️ Le serveur met trop de temps à répondre (Timeout > 120s).\n\n"
                          "Cela peut arriver si :\n"
                          "- La question est très complexe\n"
                          "- Le serveur est surchargé\n"
                          "- Le modèle IA est en cours d'initialisation\n\n"
                          "👉 Veuillez réessayer dans quelques instants ou reformuler votre question.",
                "sources": []
            }
        except (httpx.ConnectError, httpx.RequestError) as e:
            logger.error(f"❌ Impossible de se connecter à l'API : {e}")
            return {
                "answer": "🔌 Impossible de joindre le serveur API.\n\n"
                          "Vérifiez que l'API est bien lancée (`uvicorn src.api.main:app`).",
                "sources": []
            }
