import requests
from src.frontend.utils.session import API_URL, get_api_headers

def get_conversations():
    """Récupère la liste des conversations de l'utilisateur."""
    try:
        response = requests.get(f"{API_URL}/conversations/", headers=get_api_headers())
        return response
    except requests.exceptions.RequestException as e:
        return None

def get_conversation(conversation_id):
    """Récupère les détails d'une conversation."""
    try:
        response = requests.get(f"{API_URL}/conversations/{conversation_id}", headers=get_api_headers())
        return response
    except requests.exceptions.RequestException as e:
        return None

def create_conversation(title="Nouvelle conversation"):
    """Crée une nouvelle conversation."""
    try:
        response = requests.post(f"{API_URL}/conversations/", headers=get_api_headers(), json={"title": title})
        return response
    except requests.exceptions.RequestException as e:
        return None

def get_conversation_history(conversation_id):
    """Récupère l'historique des messages d'une conversation."""
    try:
        response = requests.get(f"{API_URL}/conversations/{conversation_id}/history", headers=get_api_headers())
        return response
    except requests.exceptions.RequestException as e:
        return None

def delete_conversation(conversation_id):
    """Supprime une conversation."""
    try:
        response = requests.delete(f"{API_URL}/conversations/{conversation_id}", headers=get_api_headers())
        return response
    except requests.exceptions.RequestException as e:
        return None

def update_conversation(conversation_id, title=None, status=None):
    """Met à jour une conversation (titre ou statut)."""
    try:
        payload = {}
        if title:
            payload["title"] = title
        if status:
            payload["status"] = status
            
        response = requests.patch(
            f"{API_URL}/conversations/{conversation_id}", 
            headers=get_api_headers(), 
            json=payload
        )
        return response
    except requests.exceptions.RequestException as e:
        return None
