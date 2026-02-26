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
            color: #102027 !important; /* Force Dark Text globally */
        }

        /* --- Text Visibility Fix (Force Dark Text on White Background) --- */
        /* Targets headers, paragraphs, labels to ensure they are visible even if Streamlit is in Dark Mode */
        h1, h2, h3, h4, h5, h6, p, li, label, .stMarkdown, .stText, [data-testid="stMarkdownContainer"] p {
            color: #102027 !important;
        }

        /* --- Global Background --- */
        .stApp {
            background-color: #FFFFFF !important; /* White base */
            background-image: linear-gradient(to bottom right, #B2DFDB 0%, #FFFFFF 60%, #FFFFFF 100%); /* Light Mint to White fade */
        }
        
        /* --- Header & Sidebar Hide --- */
        /* Masquer complètement la Sidebar native et son bouton */
        [data-testid="stSidebar"] {
            display: none !important;
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

        /* Padding global pour éviter que le contenu soit caché sous la Navbar fixe */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px;
        }

        /* --- Buttons --- */
        /* Target ALL buttons first to ensure a baseline */
        div.stButton > button {
            background-color: #FFFFFF !important; /* Default to White */
            color: #102027 !important; /* Default to Dark Text */
            border: 1px solid #cfd8dc !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
        }
        div.stButton > button:hover {
            border-color: #4DB6AC !important;
            color: #4DB6AC !important;
            background-color: #E0F2F1 !important;
        }
        div.stButton > button p {
            color: #102027 !important; /* Ensure text inside is dark by default */
        }

        /* Primary (Dark Navy #102027) - Specific Override */
        div.stButton > button[kind="primary"] {
            background-color: #102027 !important; 
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 6px rgba(16, 32, 39, 0.3) !important;
        }
        /* Force text inside primary button to be white */
        div.stButton > button[kind="primary"] p, 
        div.stButton > button[kind="primary"] div {
             color: white !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #37474f !important;
            box-shadow: 0 6px 12px rgba(55, 71, 79, 0.4) !important;
            transform: translateY(-1px);
            color: white !important; /* Keep text white on hover */
        }
        div.stButton > button[kind="primary"]:hover p {
            color: white !important;
        }

        /* Secondary (Standard) - Redundant if we style base button, but kept for specificity */
        div.stButton > button[kind="secondary"] {
            background-color: white !important;
            color: #102027 !important;
            border: 1px solid #102027 !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            border-color: #4DB6AC !important;
            color: #4DB6AC !important;
            background-color: #E0F2F1 !important;
        }

        /* --- Global Input Styles (Fix visibility issues) --- */
        /* Force fond blanc et texte noir partout (Profile, Login, etc.) */
        /* We use a very specific selector to override Streamlit defaults */
        .stTextInput input, .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #102027 !important; /* Texte Noir/Bleu Nuit */
            border: 1px solid #cfd8dc !important;
            caret-color: #102027 !important; /* Cursor color */
        }
        .stTextInput input:focus, .stTextInput > div > div > input:focus {
             border-color: #0277bd !important;
             box-shadow: 0 0 0 1px #0277bd !important;
        }
        .stTextInput input::placeholder {
            color: #90a4ae !important; /* Placeholder gris visible */
            opacity: 1 !important;
        }
        /* Fix label color for inputs */
        .stTextInput label, .stTextInput label p {
            color: #102027 !important;
            font-weight: 600 !important;
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
