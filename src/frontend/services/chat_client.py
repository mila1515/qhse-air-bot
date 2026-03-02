import httpx
from src.frontend.utils.session import API_URL, get_api_headers
from src.monitoring.logger import logger

# Timeout étendu pour les réponses RAG (120s)
TIMEOUT = 120.0

def send_chat_message(conversation_id: int, message: str) -> httpx.Response:
    """
    Envoie un message au backend pour une conversation donnée.
    Retourne l'objet Response brut (httpx) pour que l'appelant gère le status_code et le json().
    """
    url = f"{API_URL}/conversations/{conversation_id}/chat"
    headers = get_api_headers()
    
    # On utilise un client context manager pour s'assurer que la connexion est fermée
    # Mais comme on veut retourner la réponse, on ne peut pas utiliser 'with' ici facilement 
    # si on veut streamer ou lire après.
    # Cependant, httpx.post est un raccourci qui utilise un client temporaire.
    # Pour le timeout custom, on doit passer timeout=...
    
    try:
        response = httpx.post(
            url,
            json={"question": message},
            headers=headers,
            timeout=TIMEOUT
        )
        return response
    except httpx.RequestError as e:
        # On laisse remonter l'exception pour que la vue la gère (ex: affichage erreur réseau)
        # Ou on log ici avant de relancer
        logger.error(f"Erreur lors de l'envoi du message chat: {e}")
        raise e
