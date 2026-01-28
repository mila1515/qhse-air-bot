import streamlit as st
import sys
import os

# Ajout du dossier racine au sys.path pour résoudre les imports 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.frontend.utils.session import init_session_state, logout
from src.frontend.views import login, chat, conversations, notes, home, about, profile
from src.frontend.views.components import render_navbar

# Configuration de la page
st.set_page_config(
    page_title="QHSE Air Bot",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialisation de la session
init_session_state()

def apply_global_styles():
    st.markdown("""
    <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #37474f;
        }

        /* --- Global Background --- */
        .stApp {
            background-color: #eff5f6; /* Bleu-Gris très pâle (Choix utilisateur) */
        }
        
        /* --- Header & Sidebar Hide --- */
        /* Masquer complètement la Sidebar native et son bouton */
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }
        
        /* Masquer le Header Streamlit standard (décorations) */
        header[data-testid="stHeader"] {
            background: transparent !important;
            pointer-events: none;
        }
        header[data-testid="stHeader"] > div {
            display: none;
        }

        /* Padding global pour éviter que le contenu soit caché sous la Navbar fixe (70px) */
        .block-container {
            padding-top: 6rem !important; /* 70px navbar + padding */
            padding-bottom: 2rem !important;
            max-width: 1200px;
        }

        /* --- Buttons --- */
        /* Primary (Vert #48bb78) */
        div.stButton > button[kind="primary"] {
            background-color: #48bb78 !important; 
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #38a169 !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15) !important;
        }

        /* Secondary (Standard) */
        div.stButton > button[kind="secondary"] {
            background-color: white !important;
            color: #4a5568 !important;
            border: 1px solid #cbd5e0 !important;
            border-radius: 8px !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            border-color: #a0aec0 !important;
            background-color: #f7fafc !important;
        }
        
    </style>
    """, unsafe_allow_html=True)

def main():
    # --- Gestion des Actions Globales via Query Params ---
    query_params = st.query_params
    
    # Logout
    if query_params.get("action") == "logout":
        logout() # Cela nettoie la session et fait un rerun
        # Nettoyer l'action pour éviter la boucle (logout() fait déjà un rerun mais par sécurité)
        if "action" in st.query_params:
            del st.query_params["action"]
        st.rerun()

    # Navigation View
    if "view" in query_params:
        target_view = query_params["view"]
        # Gestion des listes (vieux streamlit) ou string
        if isinstance(target_view, list):
            target_view = target_view[0]
            
        # Logique de redirection
        if target_view == "Login" and st.session_state.token:
             # Si déjà connecté, Login -> Home (Dashboard)
             st.session_state.current_view = "Home"
        else:
             st.session_state.current_view = target_view
        
        # On nettoie le paramètre pour garder l'URL propre, sauf si on veut le garder pour le bookmarking
        # Pour une SPA, on peut le laisser. Ici, render_navbar utilise des liens ?view=...
        # Si on le laisse, st.query_params est synchro.
        pass

    # Initialisation Vue par défaut
    if "current_view" not in st.session_state:
        st.session_state.current_view = "Home"

    # --- Rendu UI ---
    apply_global_styles()
    
    # Navbar Fixe (SaaS Style)
    render_navbar()

    # --- Routing ---
    if not st.session_state.token:
        # --- Mode Public / Déconnecté ---
        if st.session_state.current_view == "Login":
            login.render_login()
        elif st.session_state.current_view == "About":
            about.render_about()
        else:
            # Par défaut : Landing Page
            home.render_home()
            
    else:
        # --- Mode Connecté (SaaS Dashboard) ---
        
        # Redirections de sécurité
        if st.session_state.current_view == "Login":
             st.session_state.current_view = "Home"
             st.rerun()

        # Vue Principale
        if st.session_state.current_view == "Home":
             # Nouvelle Vue Dashboard "Bonjour !"
             home.render_dashboard()
        elif st.session_state.current_view == "Chat":
             chat.render_chat()
        elif st.session_state.current_view == "Conversations":
             conversations.render_conversations()
        elif st.session_state.current_view == "Notes":
             notes.render_notes()
        elif st.session_state.current_view == "Profile":
             profile.render_profile()
        elif st.session_state.current_view == "About":
             about.render_about()
        else:
             # Fallback
             home.render_dashboard()

if __name__ == "__main__":
    main()
