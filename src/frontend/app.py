import streamlit as st
import sys
import os

# Ajout du dossier racine au sys.path pour résoudre les imports 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.frontend.utils.session import init_session_state, logout
from src.frontend.views import login, chat, conversations, notes, home, about

# Configuration de la page
st.set_page_config(
    page_title="QHSE Air Bot",
    page_icon="🤖",
    layout="wide"
)

# Initialisation de la session
init_session_state()

def apply_global_styles():
    st.markdown("""
    <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #37474f;
        }

        /* --- Global Background --- */
        .stApp {
            background-color: #F0F8FF; /* Bleu très très clair (AliceBlue) */
        }
        
        /* Cacher le header par défaut de Streamlit pour laisser place à notre Navbar */
        header[data-testid="stHeader"] {
            display: none;
        }

        /* Padding global pour éviter que le contenu soit caché sous la Navbar fixe */
        .block-container {
            padding-top: 6rem !important;
            padding-bottom: 2rem !important;
        }

        /* --- Sidebar --- */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa; /* Gris clair */
            border-right: 1px solid #eceff1;
        }
        
        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        /* --- Headers --- */
        h1, h2, h3 {
            color: #0277bd !important; /* Bleu très clair/vif */
            font-weight: 700;
        }
        
        /* --- Buttons --- */
        /* Primary (Vert clair) */
        div.stButton > button[kind="primary"] {
            background-color: #66bb6a !important; 
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #4caf50 !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15) !important;
        }

        /* Secondary (Standard) */
        div.stButton > button[kind="secondary"] {
            background-color: white !important;
            color: #546e7a !important;
            border: 1px solid #cfd8dc !important;
            border-radius: 8px !important;
            white-space: nowrap !important; /* Force text on one line */
        }
        div.stButton > button[kind="secondary"]:hover {
            border-color: #b0bec5 !important;
            background-color: #f5f5f5 !important;
        }

        /* --- Logout Button Specifics (Targeting via CSS hack not perfect, but we can try to rely on order or just class) --- */
        /* On va utiliser une classe custom via markdown si possible, ou juste le style secondary modifié pour être 'rouge discret' si c'est le seul secondary important */
        
        /* --- Containers & Cards --- */
        [data-testid="stExpander"] {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #f0f2f6;
        }
        
        /* --- Navigation Radio --- */
        .stRadio > label {
            font-weight: 600;
            color: #455a64;
        }
        
    </style>
    """, unsafe_allow_html=True)

def main():
    # Gestion des query params pour la navigation via Navbar HTML
    try:
        # Compatible Streamlit moderne
        query_params = st.query_params
        if "view" in query_params:
            view_param = query_params["view"]
            # Si c'est une liste (anciennes versions parfois) ou string
            target_view = view_param if isinstance(view_param, str) else view_param[0]
            
            if target_view in ["Home", "Login", "About"]:
                st.session_state.current_view = target_view
                # Nettoyer l'URL pour éviter de rester bloqué sur ?view=...
                # Note: On ne force pas le rerun immédiat car le rechargement de page l'a déjà fait
    except:
        pass

    # Gestion de la navigation interne (SPA)
    if "current_view" not in st.session_state:
        # Par défaut, la première visite mène à l'accueil
        st.session_state.current_view = "Home"
    
    # Appliquer le style global
    apply_global_styles()

    if not st.session_state.token:
        # --- Utilisateur NON Connecté ---
        if st.session_state.current_view == "Login":
            login.render_login()
        elif st.session_state.current_view == "About":
            about.render_about()
        else:
            # Par défaut (ou si "Home"), afficher la page d'accueil
            home.render_home()
            
    else:
        # --- Utilisateur Connecté ---
        # Si Login, rediriger vers Chat. Si Home ou About, autoriser l'affichage.
        if st.session_state.current_view == "Login":
             st.session_state.current_view = "Chat"
             st.rerun()

        # Si l'utilisateur est sur Home ou About, on affiche la vue publique
        if st.session_state.current_view == "Home":
             home.render_home()
             return # On arrête ici pour ne pas afficher la sidebar standard
        elif st.session_state.current_view == "About":
             about.render_about()
             return

        # Si connecté, afficher la Sidebar et le contenu
        with st.sidebar:
            # En-tête Sidebar
            st.markdown("### 🤖 QHSE Air Bot")
            
            # User Card
            if st.session_state.user:
                email = st.session_state.user.get('email', 'User')
                st.markdown(f"""
                <div style="background-color: white; padding: 1rem; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 2rem;">
                    <div style="font-size: 0.8rem; color: #78909c; margin-bottom: 0.2rem;">Connecté en tant que</div>
                    <div style="font-weight: 600; color: #37474f; overflow-wrap: break-word;">{email}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Navigation
            st.markdown('<div style="margin-bottom: 0.5rem; font-weight: 600; color: #90a4ae; font-size: 0.8rem;">NAVIGATION</div>', unsafe_allow_html=True)
            
            # Options avec icônes
            nav_options = {"Chat": "💬 Discussion", "Conversations": "🗂️ Historique", "Notes": "📝 Mes Notes"}
            
            # Trouver l'index actuel
            try:
                current_index = list(nav_options.keys()).index(st.session_state.current_view)
            except ValueError:
                current_index = 0
            
            selected_label = st.radio(
                "Menu Navigation",
                options=list(nav_options.values()),
                index=current_index,
                label_visibility="collapsed"
            )
            
            # Mise à jour de la vue
            new_view = [k for k, v in nav_options.items() if v == selected_label][0]
            if new_view != st.session_state.current_view:
                st.session_state.current_view = new_view
                st.rerun()

            st.markdown("<br>" * 5, unsafe_allow_html=True) # Espaceur visuel
            st.divider()
            
            # Bouton de déconnexion (Rouge discret via style global ou simple secondaire)
            if st.button("🚪 Se déconnecter", type="secondary", use_container_width=True):
                logout()

        # Rendu de la vue sélectionnée
        if st.session_state.current_view == "Chat":
            chat.render_chat()
        elif st.session_state.current_view == "Conversations":
            conversations.render_conversations()
        elif st.session_state.current_view == "Notes":
            notes.render_notes()

if __name__ == "__main__":
    main()
