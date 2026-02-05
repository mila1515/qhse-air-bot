import streamlit as st
import os
import extra_streamlit_components as stx
from datetime import datetime, timedelta

# Configuration de l'API
# En local : http://localhost:8000
# Dans Docker : http://qhse_api:8000 (nom du service/conteneur)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# @st.cache_resource supprimé pour éviter CachedWidgetWarning
def get_cookie_manager():
    # Utilisation d'une clé fixe pour éviter la duplication du widget
    return stx.CookieManager(key="auth_cookie_manager")

def init_session_state():
    """Initialise les variables de session Streamlit et restaure la session via cookies."""
    # Instancier le gestionnaire de cookies (doit être fait à chaque run pour le rendu du composant)
    # On le stocke dans session_state pour réutilisation dans save_token/logout
    st.session_state.cookie_manager = get_cookie_manager()
    cookie_manager = st.session_state.cookie_manager
    
    # 1. Initialiser les variables de base si elles n'existent pas
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # 2. Tentative de restauration depuis le cookie si pas connecté
    if not st.session_state.token:
        # Récupération du cookie (peut nécessiter un rerun automatique géré par le composant)
        token_cookie = cookie_manager.get("access_token")
        if token_cookie:
            st.session_state.token = token_cookie
            
            # Valider le token et récupérer l'utilisateur
            # Import local pour éviter import circulaire
            from src.frontend.services import auth_client
            try:
                user_resp = auth_client.get_current_user()
                if user_resp and user_resp.status_code == 200:
                    st.session_state.user = user_resp.json()
                    # Si on vient de restaurer la session, on peut notifier ou juste continuer
                else:
                    # Token invalide ou expiré
                    st.session_state.token = None
                    cookie_manager.delete("access_token")
            except Exception:
                st.session_state.token = None

def save_token(token):
    """Sauvegarde le token en session et dans les cookies."""
    st.session_state.token = token
    # Utiliser l'instance stockée dans session_state pour éviter de recréer le widget
    cookie_manager = st.session_state.cookie_manager
    
    # Expire dans 7 jours
    expires_at = datetime.now() + timedelta(days=7)
    cookie_manager.set("access_token", token, expires_at=expires_at)

def get_api_headers():
    """Retourne les headers HTTP avec le token JWT si disponible."""
    headers = {"Content-Type": "application/json"}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers

def logout():
    """Déconnecte l'utilisateur et nettoie la session."""
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.current_conversation_id = None
    st.session_state.messages = []
    st.session_state.current_view = "Login"
    
    # Supprimer le cookie
    # Utiliser l'instance stockée dans session_state
    if "cookie_manager" in st.session_state:
        cookie_manager = st.session_state.cookie_manager
        try:
            # Vérifier si le cookie existe avant de supprimer pour éviter KeyError
            if cookie_manager.get("access_token"):
                cookie_manager.delete("access_token")
        except Exception:
            # En cas d'erreur (ex: KeyError interne au composant), on ignore
            pass
    
    # Mettre à jour l'URL pour éviter la persistance de la vue précédente
    try:
        st.query_params["view"] = "Login"
    except Exception:
        pass
    
    # Rerun pour appliquer les changements
    st.rerun()
