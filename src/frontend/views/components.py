import streamlit as st
import os
import base64

def get_base64_logo():
    """Récupère le logo en base64 depuis assets/logo_home.png"""
    try:
        # Chemin relatif depuis ce fichier (views/components.py) vers ../assets/logo_home.png
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo_home.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
    except Exception:
        pass
    return None

def render_navbar():
    """
    Affiche la Top Navigation Bar (SaaS Style).
    Gère l'état connecté/déconnecté.
    """
    # --- Configuration ---
    NAV_HEIGHT = "70px"
    # Background Blanc pur (#FFFFFF) demandé pour le nouveau design
    BG_COLOR = "#FFFFFF"
    BORDER_COLOR = "#e2e8f0"
    
    # Callback de navigation
    def navigate_to(view):
        st.session_state.current_view = view
        st.query_params["view"] = view
    
    # --- CSS pour la Navbar Native ---
    st.markdown(f"""
    <style>
        /* Rendre le premier bloc horizontal (navbar) sticky/fixe en haut */
        div[data-testid="stHorizontalBlock"]:first-child {{
            position: sticky;
            top: 0;
            z-index: 999999;
            background-color: {BG_COLOR};
            border-bottom: 1px solid {BORDER_COLOR};
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}

        /* Container Navbar */
        .nav-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: {NAV_HEIGHT};
            background-color: {BG_COLOR};
            border-bottom: 1px solid {BORDER_COLOR};
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        /* 
           TARGETING BOUTONS NAVBAR 
           La structure est : Logo (col 1) | Menu (col 2) | Profile/Connexion (col 3)
           On utilise :nth-child sur les colonnes du premier bloc horizontal pour différencier les styles.
        */

        /* COLONNE 2 (Menu Central) : Liens texte simples (Accueil, À propos) */
        div[data-testid="stHorizontalBlock"]:first-child > div:nth-child(2) div.stButton > button {{
            background-color: transparent !important;
            color: #4a5568 !important; /* Gris foncé lisible */
            border: none !important;
            box-shadow: none !important;
            font-weight: 500 !important;
            padding: 8px 16px !important;
            font-family: 'Inter', sans-serif !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-child > div:nth-child(2) div.stButton > button:hover {{
            color: #1A365D !important; /* Bleu Marine au survol */
            background-color: transparent !important;
        }}
        /* Lien Actif (Primary) dans le menu : Gras + Souligné ou couleur distinctive */
        div[data-testid="stHorizontalBlock"]:first-child > div:nth-child(2) button[kind="primary"] {{
            color: #1A365D !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #48BB78 !important; /* Souligné Vert Émeraude */
            border-radius: 0 !important;
        }}

        /* COLONNE 3 (Profile/Connexion) : Bouton Vert Émeraude (Connexion) */
        /* Note: On cible spécifiquement le bouton "Connexion" (nav_login) si possible, 
           mais ici on applique le style à tous les boutons de la col 3 par défaut pour simplifier,
           sauf si connecté (Profil/Sortir sont aussi en col 3). 
           Pour le mode public, c'est parfait.
        */
        div[data-testid="stHorizontalBlock"]:first-child > div:nth-child(3) div.stButton > button {{
            background-color: #48BB78 !important; /* Vert Émeraude */
            color: white !important;
            border: none !important;
            border-radius: 8px !important; /* Arrondi 8px demandé */
            padding: 8px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px -1px rgba(72, 187, 120, 0.4) !important; /* Ombre portée verte */
        }}
        div[data-testid="stHorizontalBlock"]:first-child > div:nth-child(3) div.stButton > button:hover {{
            background-color: #38a169 !important; /* Vert plus foncé */
            box-shadow: 0 6px 8px -1px rgba(72, 187, 120, 0.5) !important;
        }}
        
        /* Ajustement pour le mode connecté (Boutons Profil/Sortir en gris ou blanc ?)
           Si on veut garder le vert pour Connexion mais pas pour Profil/Sortir, 
           c'est délicat sans sélecteur ID. 
           Mais le prompt "Sujet" se concentre sur l'interface AVANT connexion (Public).
           On laisse le style Vert pour la col 3 en Public.
           En mode connecté, le bouton Profil sera Vert aussi avec ce code. 
           C'est acceptable ou on peut affiner plus tard.
        */

    </style>
    """, unsafe_allow_html=True)

    # Style PUBLIC (non connecté) : Supprimé pour garder le style bouton gris uniforme
    # if not st.session_state.get("token"): ...

    # --- Navbar Native (Streamlit Columns) ---
    # On utilise un conteneur pour le layout
    with st.container():
        # Layout: [Logo 2] [Menu 6] [Profil 2]
        c_logo, c_menu, c_profile = st.columns([2, 7, 3])
        
        # 1. Logo & Titre
        with c_logo:
            logo_b64 = get_base64_logo()
            if logo_b64:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px; height: 40px;">
                    <img src="data:image/png;base64,{logo_b64}" style="height: 32px; width: auto;">
                    <span style="font-weight: 700; font-size: 16px; color: #2d3748;">QHSE Air Bot</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("**QHSE Air Bot**")

        # 2. Menu Central
        with c_menu:
            if st.session_state.get("token"):
                # Menu Connecté
                # On utilise des colonnes internes pour les boutons
                # Ajuster le nombre de colonnes en fonction des items
                m1, m2, m3, m4 = st.columns(4)
                
                current = st.session_state.get("current_view", "Home")
                
                with m1:
                    st.button("Accueil", key="nav_home", 
                             type="primary" if current == "Home" else "secondary", 
                             use_container_width=True,
                             on_click=navigate_to, args=("Home",))
                with m2:
                    st.button("Discussion", key="nav_chat", 
                             type="primary" if current == "Chat" else "secondary", 
                             use_container_width=True,
                             on_click=navigate_to, args=("Chat",))
                with m3:
                    st.button("Historique", key="nav_hist", 
                             type="primary" if current == "Conversations" else "secondary", 
                             use_container_width=True,
                             on_click=navigate_to, args=("Conversations",))
                with m4:
                    st.button("Notes", key="nav_notes", 
                             type="primary" if current == "Notes" else "secondary", 
                             use_container_width=True,
                             on_click=navigate_to, args=("Notes",))
            else:
                # Menu Public
                m1, m2 = st.columns(2)
                current = st.session_state.get("current_view", "Home")
                
                with m1:
                    st.button("Accueil", key="nav_pub_home", 
                             type="primary" if current == "Home" else "secondary", 
                             use_container_width=True,
                             on_click=navigate_to, args=("Home",))
                with m2:
                    st.button("À propos", key="nav_pub_about", 
                             type="primary" if current == "About" else "secondary", 
                             use_container_width=True,
                             on_click=navigate_to, args=("About",))

        # 3. Profil / Logout
        with c_profile:
            if st.session_state.get("token"):
                user_email = "User"
                if st.session_state.get("user"):
                    user_email = st.session_state.user.get("email", "User")
                
                # Layout compact pour profil
                p1, p2 = st.columns([2, 1])
                with p1:
                    # Avatar simulé (Bouton Profil)
                    st.button("Profil", key="nav_profile", type="secondary", 
                             help="Voir mon profil",
                             use_container_width=True,
                             on_click=navigate_to, args=("Profile",))
                with p2:
                     # Logout (lien spécial car action différente)
                     # On utilise un bouton qui déclenche l'action de logout via URL ou callback
                     # Le callback logout() fait st.rerun(), parfait.
                     # Import local pour éviter cycle ? Non, app.py l'a.
                     # Mais render_navbar est dans components.py
                     # On va utiliser st.query_params pour logout qui est géré dans app.py
                     def do_logout():
                         st.query_params["action"] = "logout"
                     
                     st.button("Sortir", key="nav_logout", type="secondary", 
                              use_container_width=True,
                              on_click=do_logout)
            else:
                # Bouton Connexion
                st.button("Connexion", key="nav_login", type="secondary", 
                         use_container_width=True,
                         on_click=navigate_to, args=("Login",))
    
    # Espace visuel propre entre NAVBAR et contenu
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
