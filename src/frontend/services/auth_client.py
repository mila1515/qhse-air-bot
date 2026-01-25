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

def register_user(email, password):
    """Crée un nouveau compte utilisateur."""
    try:
        response = requests.post(f"{API_URL}/auth/register", json={"email": email, "password": password})
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
        return None
