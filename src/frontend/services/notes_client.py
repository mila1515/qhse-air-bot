import requests
from src.frontend.utils.session import API_URL, get_api_headers

def get_notes():
    """Récupère la liste des notes."""
    try:
        response = requests.get(f"{API_URL}/notes/", headers=get_api_headers())
        return response
    except requests.exceptions.RequestException as e:
        return None

def create_note(title, content):
    """Crée une nouvelle note."""
    try:
        payload = {"title": title, "content": content}
        response = requests.post(f"{API_URL}/notes/", headers=get_api_headers(), json=payload)
        return response
    except requests.exceptions.RequestException as e:
        return None

# update_note n'est pas implémenté dans l'API pour l'instant
def update_note(note_id, content):
    """Met à jour une note existante."""
    # TODO: Implementer PUT /notes/{id} dans l'API si besoin
    return None

def delete_note(note_id):
    """Supprime une note."""
    try:
        response = requests.delete(f"{API_URL}/notes/{note_id}", headers=get_api_headers())
        return response
    except requests.exceptions.RequestException as e:
        return None
