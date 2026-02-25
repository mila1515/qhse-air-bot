import requests
import streamlit as st
from src.frontend.utils.session import API_URL, get_api_headers

def login_user(email, password):
    """Authentifie l'utilisateur et récupère le token JWT."""
    try:
        # Standard OAuth2 : Utiliser 'data' (form-urlencoded) et 'username' pour l'email
        response = requests.post(
            f"{API_URL}/auth/login", 
            data={"username": email, "password": password}
        )
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion API (Login): {e}")
        return None

def register_user(email, password, username=None):
    """Crée un nouveau compte utilisateur."""
    try:
        payload = {"email": email, "password": password}
        # Note: L'API actuelle ne semble pas encore stocker le username, mais on le passe au cas où
        # Si l'API évolue pour accepter le username, il faudra l'ajouter ici.
        # Pour l'instant, on garde la signature compatible avec l'appel frontend.
        response = requests.post(f"{API_URL}/auth/register", json=payload)
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion API (Register): {e}")
        return None

def get_current_user():
    """Récupère les informations de l'utilisateur connecté."""
    try:
        response = requests.get(f"{API_URL}/auth/me", headers=get_api_headers())
        return response
    except requests.exceptions.RequestException as e:
        print(f"DEBUG AUTH: Erreur get_current_user: {e}")
        return None
