import requests
from src.frontend.utils.session import API_URL, get_api_headers

def send_chat_message(conversation_id, question):
    """Envoie un message au bot dans une conversation spécifique."""
    try:
        payload = {"question": question}
        response = requests.post(
            f"{API_URL}/conversations/{conversation_id}/chat", 
            headers=get_api_headers(), 
            json=payload,
            timeout=120  # Timeout de 120 secondes pour les réponses longues (RAG)
        )
        return response
    except requests.exceptions.RequestException as e:
        raise e
