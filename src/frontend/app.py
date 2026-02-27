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

        /* --- GLOBAL THEME FORCE (Light Mode) --- */
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

        /* --- Buttons (NUCLEAR OPTION: NO BLACK BACKGROUNDS EVER) --- */
        /* Target ALL buttons generic to ensure a baseline */
        div.stButton > button, button {
            background-color: #FFFFFF !important; /* Default to White */
            color: #102027 !important; /* Default to Dark Text */
            border: 1px solid #cfd8dc !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        }
        
        /* Hover State */
        div.stButton > button:hover, button:hover {
            border-color: #4DB6AC !important;
            color: #4DB6AC !important;
            background-color: #E0F2F1 !important; /* Light Teal Tint */
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        /* Active/Focus State (Clicking) - CRITICAL FIX for "Black Background" */
        div.stButton > button:active, button:active,
        div.stButton > button:focus:not(:active), button:focus:not(:active) {
            background-color: #FFFFFF !important;
            color: #00897B !important;
            border-color: #00897B !important;
            box-shadow: 0 0 0 2px rgba(0, 137, 123, 0.2) !important;
            outline: none !important;
        }

        /* Text inside buttons */
        div.stButton > button p {
            color: #102027 !important; 
        }
        div.stButton > button:hover p {
            color: #4DB6AC !important;
        }

        /* --- Primary Buttons (Teal/Mint Theme) --- */
        div.stButton > button[kind="primary"] {
            background-color: #00897B !important; /* Teal 600 */
            color: white !important;
            border: 1px solid #00897B !important;
            box-shadow: 0 4px 6px rgba(0, 137, 123, 0.3) !important;
        }
        
        /* Primary Text */
        div.stButton > button[kind="primary"] p, 
        div.stButton > button[kind="primary"] div {
             color: white !important;
        }
        
        /* Primary Hover */
        div.stButton > button[kind="primary"]:hover {
            background-color: #00796B !important; /* Teal 700 */
            border-color: #00796B !important;
            box-shadow: 0 6px 12px rgba(0, 121, 107, 0.4) !important;
            transform: translateY(-1px);
            color: white !important; 
        }
        div.stButton > button[kind="primary"]:hover p {
            color: white !important;
        }

        /* Primary Active/Focus - Ensure it stays Teal, NOT Black */
        div.stButton > button[kind="primary"]:active,
        div.stButton > button[kind="primary"]:focus:not(:active) {
            background-color: #00695C !important; /* Teal 800 */
            border-color: #00695C !important;
            color: white !important;
            box-shadow: 0 0 0 3px rgba(0, 137, 123, 0.4) !important;
        }

        /* --- Secondary Buttons (Explicitly White) --- */
        div.stButton > button[kind="secondary"] {
            background-color: white !important;
            color: #0277bd !important; /* Light Blue Text */
            border: 1px solid #b3e5fc !important;
        }
        div.stButton > button[kind="secondary"] p {
            color: #0277bd !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #e1f5fe !important; /* Very Light Blue */
            border-color: #0277bd !important;
        }
        div.stButton > button[kind="secondary"]:active,
        div.stButton > button[kind="secondary"]:focus:not(:active) {
            background-color: #b3e5fc !important;
            color: #01579b !important;
            box-shadow: 0 0 0 2px rgba(3, 169, 244, 0.3) !important;
        }

        /* --- Global Input Styles (Fix visibility issues) --- */
        /* Force fond blanc et texte noir partout (Profile, Login, etc.) */
        .stTextInput input, 
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div > div {
            background-color: #ffffff !important;
            color: #102027 !important; /* Texte Noir/Bleu Nuit */
            border: 1px solid #cfd8dc !important;
            caret-color: #102027 !important; /* Cursor color */
            border-radius: 6px !important;
        }

        .stTextInput div[data-baseweb="input"] {
            background-color: #ffffff !important;
            border-radius: 6px !important;
        }

        .stTextInput div[data-baseweb="input"] > div {
            background-color: transparent !important;
        }

        .stTextInput div[data-baseweb="input"] button {
            background-color: transparent !important;
            color: #102027 !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Fix for the container wrapping the eye icon */
        .stTextInput div[data-baseweb="input"] > div:nth-last-child(1) {
            background-color: transparent !important;
        }

        .stTextInput div[data-baseweb="input"] button:hover {
            background-color: #E0F2F1 !important;
        }

        .stTextInput div[data-baseweb="input"] svg,
        .stTextInput div[data-baseweb="input"] svg * {
            fill: #102027 !important;
            color: #102027 !important;
        }
        
        /* Focus state for inputs */
        .stTextInput input:focus, 
        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus,
        .stSelectbox > div[data-baseweb="select"] > div:focus-within {
             border-color: #00897B !important;
             box-shadow: 0 0 0 1px #00897B !important;
             background-color: #ffffff !important;
             color: #102027 !important;
        }

        /* Placeholder Visibility */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #90a4ae !important; /* Placeholder gris visible */
            opacity: 1 !important;
            -webkit-text-fill-color: #90a4ae !important;
        }
        
        /* Label Colors */
        .stTextInput label, .stTextInput label p, 
        .stTextArea label, .stTextArea label p,
        .stSelectbox label, .stSelectbox label p {
            color: #102027 !important;
            font-weight: 600 !important;
        }
        
        /* --- Login Specific Global Styles --- */
        /* Card Effect */
        .auth-card {
            background-color: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #f0f2f6;
            margin-top: 2rem;
        }
        .auth-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            color: #102027 !important;
            letter-spacing: -1px;
            line-height: 1.2;
            margin-bottom: 2rem;
            margin-top: 0;
        }

        /* --- Radio Button (Login Toggle) Fix --- */
        /* Force Text Color */
        div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
            color: #0277bd !important; /* Blue for visibility */
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }
        div[role="radiogroup"] p {
             color: #0277bd !important;
        }
        /* Center Radio Group */
        div.stRadio > div[role="radiogroup"] {
            justify-content: center;
            margin-bottom: 1rem;
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
