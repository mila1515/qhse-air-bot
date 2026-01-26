import streamlit as st
import sys
import os

# Ajout du dossier racine au sys.path pour résoudre les imports 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.frontend.utils.session import init_session_state, logout
from src.frontend.views import login, chat, conversations, notes, home, about, profile

# Configuration de la page
st.set_page_config(
    page_title="QHSE Air Bot",
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
        
        /* --- Header & Sidebar Toggle --- */
        /* On rend le header Streamlit transparent et au-dessus de notre navbar */
        header[data-testid="stHeader"] {
            background: transparent !important;
            z-index: 1000000 !important; /* Au-dessus de la navbar (999999) */
            pointer-events: none; /* Permet de cliquer sur la navbar en dessous */
        }
        
        /* Désactiver les événements sur le conteneur principal du header pour ne pas bloquer la navbar */
        header[data-testid="stHeader"] > div {
            pointer-events: none;
        }

        /* Réactiver les événements UNIQUEMENT sur les éléments interactifs du header */
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stToolbar"],
        [data-testid="stHeaderActionElements"],
        [data-testid="stStatusWidget"] {
            pointer-events: auto !important;
        }

        /* Style du bouton de contrôle de la sidebar (Flèche/Hamburger) */
        [data-testid="stSidebarCollapsedControl"] {
            color: #2E8B57 !important; /* Vert charte */
            background-color: #ffffff !important; /* Fond blanc pour visibilité */
            border-radius: 50%;
            width: 40px;
            height: 40px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-top: 0.5rem;
            margin-left: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000002 !important; /* Au-dessus de la navbar (1000001) */
            position: relative;
        }
        
        /* Remplacement de l'icône flèche par "Trois lignes" (Hamburger) */
        [data-testid="stSidebarCollapsedControl"] svg {
            display: none !important;
        }
        [data-testid="stSidebarCollapsedControl"]::after {
            content: "☰"; /* Symbole Hamburger */
            font-size: 24px;
            color: #2E8B57;
            margin-top: -4px; /* Ajustement vertical fin */
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
            
            # FIX: Si l'utilisateur est déjà connecté et demande "Login", on le redirige vers "Chat"
            # pour éviter une boucle de redirection ou de rester bloqué sur la page de login.
            if target_view == "Login" and st.session_state.token:
                # IMPORTANT : On nettoie le paramètre de l'URL pour éviter qu'il ne force la redirection à chaque rechargement
                if "view" in st.query_params:
                    del st.query_params["view"]
                
                # On ne force le Chat que si on était effectivement sur Login (ou si on vient d'arriver)
                # Si l'utilisateur est déjà dans une navigation interne (ex: Conversations), on ne touche à rien
                if st.session_state.current_view == "Login":
                    st.session_state.current_view = "Chat"
            elif target_view in ["Home", "Login", "About"]:
                st.session_state.current_view = target_view
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
            st.markdown("### QHSE Air Bot")
            
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
            nav_options = {
                "Chat": "Discussion", 
                "Conversations": "Historique", 
                "Notes": "Mes Notes",
                "Profile": "Profil"
            }
            
            # --- Navigation Robuste avec Callback ---
            
            # 1. Synchroniser le widget Radio avec la vue actuelle (current_view)
            # Cela permet de mettre à jour le radio si la vue change par code (ex: redirect après login)
            current_label = nav_options.get(st.session_state.current_view, "Discussion")
            
            # Important : Forcer la mise à jour du widget si la vue a changé par code
            # (pour éviter que le bouton reste sur l'ancien état et ne déclenche pas on_change au clic)
            if "nav_radio" not in st.session_state or st.session_state.nav_radio != current_label:
                st.session_state.nav_radio = current_label
            
            # 2. Callback de changement
            def on_nav_change():
                selected_label = st.session_state.nav_radio
                # Trouver la clé (View Name) correspondant au label
                new_view = next((k for k, v in nav_options.items() if v == selected_label), "Chat")
                st.session_state.current_view = new_view
                
                # Nettoyer les query params pour éviter les conflits avec la navigation URL
                if "view" in st.query_params:
                    del st.query_params["view"]
            
            # 3. Widget Radio
            st.radio(
                "Menu Navigation",
                options=list(nav_options.values()),
                key="nav_radio",
                on_change=on_nav_change,
                label_visibility="collapsed",
                index=list(nav_options.values()).index(current_label) if current_label in nav_options.values() else 0
            )
            
            st.markdown("<br>" * 5, unsafe_allow_html=True) # Espaceur visuel
            st.divider()
            
            # Bouton de déconnexion (Rouge discret via style global ou simple secondaire)
            if st.button("Se déconnecter", type="secondary", use_container_width=True):
                logout()

        # Rendu de la vue sélectionnée
        if st.session_state.current_view == "Chat":
            chat.render_chat()
        elif st.session_state.current_view == "Conversations":
            conversations.render_conversations()
        elif st.session_state.current_view == "Notes":
            notes.render_notes()
        elif st.session_state.current_view == "Profile":
            profile.render_profile()

if __name__ == "__main__":
    main()
