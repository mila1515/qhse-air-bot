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
    
    # 0. Si on vient de se déconnecter (indicateur dans l'URL), on FORCE le nettoyage et on ne restaure rien.
    if st.query_params.get("logged_out") == "true":
        # On s'assure que le token session est bien None
        st.session_state.token = None
        st.session_state.user = None
        
        # On tente à nouveau de supprimer le cookie si jamais il a survécu
        try:
             cookie_manager.delete("access_token")
        except:
             pass
             
        # On ne va PAS plus loin (pas de restauration)
        # Mais on initialise quand même les variables de base pour éviter les KeyError ailleurs
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "current_view" not in st.session_state:
            st.session_state.current_view = "Login"
            
        return

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
                if user_resp is not None and user_resp.status_code == 200:
                    st.session_state.user = user_resp.json()
                    # Si on vient de restaurer la session, on peut notifier ou juste continuer
                elif user_resp is not None and user_resp.status_code in [401, 403, 422]:
                    # Token explicitement invalide ou expiré (ou malformé 422)
                    st.session_state.token = None
                    cookie_manager.delete("access_token")
                    # Force rerun pour nettoyer l'interface
                    st.rerun()
                else:
                    # Erreur technique (API down, Timeout, 500...)     
                    # On ne supprime PAS le cookie pour permettre la reconnexion auto au retour du service
                    st.session_state.token = None
                    error_msg = f"Code: {user_resp.status_code}" if user_resp is not None else "Pas de réponse"
                    print(f"DEBUG SESSION: Erreur récupération user. {error_msg}")
                    st.warning(f"⚠️ Serveur indisponible temporairement ({error_msg}). Veuillez rafraîchir la page dans quelques instants.")
            except Exception as e:
                # Erreur inattendue dans le bloc try
                print(f"DEBUG SESSION: Exception inattendue: {e}")
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
    # 1. Supprimer le cookie AVANT de nettoyer session_state pour s'assurer que l'instance est là
    if "cookie_manager" in st.session_state:
        cookie_manager = st.session_state.cookie_manager
        try:
            # On tente de supprimer le cookie 'access_token'
            cookie_manager.delete("access_token")
        except Exception as e:
            print(f"DEBUG LOGOUT: Erreur suppression cookie: {e}")
    
    # 2. Nettoyer session_state
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.current_conversation_id = None
    st.session_state.messages = []
    st.session_state.current_view = "Login"
    
    # 3. Mettre à jour l'URL pour éviter la persistance de la vue précédente
    try:
        st.query_params.clear()
        st.query_params["view"] = "Login"
        # Ajout d'un indicateur explicite pour que le prochain run sache qu'on vient de sortir
        st.query_params["logged_out"] = "true"
    except Exception:
        pass
    
    # 4. Rerun pour appliquer les changements
    st.rerun()
