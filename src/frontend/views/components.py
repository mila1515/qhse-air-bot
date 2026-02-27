import streamlit as st
import os
import base64

@st.cache_data
def get_base64_logo():
    """Récupère le logo en base64 depuis assets/logo_home.png avec mise en cache"""
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
    BG_COLOR = "#FFFFFF"
    BORDER_COLOR = "#e2e8f0"
    
    # Callback de navigation
    def navigate_to(view):
        st.session_state.current_view = view
        st.query_params["view"] = view
    
    # --- CSS SIMPLIFIÉ ET ROBUSTE --- 
    st.markdown(""" 
    <style> 
        /* 1. Navbar FIXE */ 
        /* On cible le bloc horizontal qui contient le marqueur 'navbar-marker' */
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) {
            position: fixed !important; 
            top: 0 !important; 
            left: 0 !important; 
            width: 100% !important; 
            height: 70px !important; 
            z-index: 9999 !important; 
            background: linear-gradient(90deg, #80CBC4 0%, #B2DFDB 100%) !important; /* Lighter Mint Gradient */
            border-bottom: 1px solid #4DB6AC !important; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important; 
            padding: 0.5rem 2rem !important; 
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important; 
        } 
         
        /* 2. Compenser l'espace pour le contenu */ 
        .block-container { 
            padding-top: 90px !important; /* 70px navbar + 20px padding */ 
            padding-bottom: 2rem !important; 
            max-width: 1200px !important; 
        } 
         
        /* 3. Masquer header Streamlit */ 
        header[data-testid="stHeader"] { 
            display: none !important; 
        } 
         
        /* 4. Masquer Sidebar */ 
        [data-testid="stSidebar"] { 
            display: none !important; 
        } 
         
        /* 5. Fond de page */ 
        .stApp { 
            background-color: #F8FAFC !important; 
        }
        
        /* 6. Styles des Boutons de la Navbar (Interne) */
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button {
            border: none !important;
            box-shadow: none !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            background-color: transparent !important;
            color: #102027 !important; /* Texte Bleu Nuit pour lisibilité */
            white-space: nowrap !important; /* Empêche le retour à la ligne */
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }

        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button p,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button div,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button span {
            color: #102027 !important;
        }

        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:hover {
            background-color: rgba(255, 255, 255, 0.5) !important; /* Fond blanc semi-transparent au survol */
            color: #000000 !important; /* Noir au survol */
        }

        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:hover p,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:hover div,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:hover span {
            color: #000000 !important;
        }
        
        /* Force le style même pour les boutons Primary (qui sont blancs par défaut) */
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button[kind="primary"] {
            color: #102027 !important;
            background-color: transparent !important;
        }

        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button[kind="primary"] p,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button[kind="primary"] div,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button[kind="primary"] span {
            color: #102027 !important;
        }

        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button[kind="primary"]:hover {
            color: #00796B !important; /* Darker Teal au survol pour lisibilité */
            background-color: #f1f5f9 !important;
        }

        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:active,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:focus:not(:active),
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button[kind="primary"]:active,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button[kind="primary"]:focus:not(:active) {
            background-color: rgba(255, 255, 255, 0.5) !important;
            color: #102027 !important;
            box-shadow: none !important;
        }

        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:active p,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:active div,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:active span,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:focus:not(:active) p,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:focus:not(:active) div,
        div[data-testid="stHorizontalBlock"]:has(div.navbar-marker) button:focus:not(:active) span {
            color: #102027 !important;
        }

        /* 7. Gap custom pour le menu public */
        div[data-testid="stHorizontalBlock"]:has(div.menu-group-marker) {
            gap: 10px !important;
            align-items: center !important;
        }
    </style> 
    """, unsafe_allow_html=True) 

    # --- Navbar Structure --- 
    # Note: On utilise un marqueur invisible pour que le CSS cible ce bloc spécifique
    
    # Structure simplifiée : Logo (20%) | Contenu Centré (80%)
    c_logo, c_content = st.columns([2, 8]) 
    
    # 1. Logo & Titre 
    with c_logo: 
        # Marqueur invisible pour le CSS :has()
        st.markdown('<div class="navbar-marker" style="display:none;"></div>', unsafe_allow_html=True)
        
        logo_b64 = get_base64_logo() 
        if logo_b64: 
            st.markdown(f""" 
            <div style="display: flex; align-items: center; gap: 14px; height: 60px; cursor: pointer; transform: translateY(-12px);"> 
                <img src="data:image/png;base64,{logo_b64}" style="height: 58px; width: auto;"> 
                <span style="font-weight: 700; font-size: 24px; color: #000000; letter-spacing: -0.5px;">QHSE Air Bot</span> 
            </div> 
            """, unsafe_allow_html=True) 
        else: 
            st.markdown("**QHSE Air Bot**") 

    # 2. Menu & Actions (Groupés)
    with c_content:
        if st.session_state.get("token"): 
            # --- Mode Connecté ---
            # On groupe tout : Accueil, Chat, Hist, Notes, Profil
            # Répartition équilibrée sur 5 colonnes
            c1, c2, c3, c4, c5 = st.columns(5) 
            current = st.session_state.get("current_view", "Home") 
             
            with c1: 
                st.button("Accueil", key="nav_home",  
                         type="primary" if current == "Home" else "secondary",  
                         use_container_width=True, 
                         on_click=navigate_to, args=("Home",)) 
            with c2: 
                st.button("Discussion", key="nav_chat",  
                         type="primary" if current == "Chat" else "secondary",  
                         use_container_width=True, 
                         on_click=navigate_to, args=("Chat",)) 
            with c3: 
                st.button("Historique", key="nav_hist",  
                         type="primary" if current == "Conversations" else "secondary",  
                         use_container_width=True, 
                         on_click=navigate_to, args=("Conversations",)) 
            with c4: 
                st.button("Notes", key="nav_notes",  
                         type="primary" if current == "Notes" else "secondary",  
                         use_container_width=True, 
                         on_click=navigate_to, args=("Notes",)) 
            with c5: 
                st.button("Profil", key="nav_profile", type="secondary",  
                         use_container_width=True, 
                         on_click=navigate_to, args=("Profile",))

        else: 
            # --- Mode Public ---
            # Accueil, À propos, Connexion -> Groupés au centre
            # On utilise des colonnes ajustées et le CSS 'gap: 5px'
            # Ajustement des ratios pour donner plus de place aux boutons (éviter le wrap) tout en restant centrés
            
            # Marqueur pour le CSS gap (placé AVANT les colonnes pour ne pas décaler le premier bouton)
            st.markdown('<div class="menu-group-marker" style="display:none;"></div>', unsafe_allow_html=True)
            
            _, m1, m2, m3, _ = st.columns([1.5, 1.2, 1.2, 1.2, 1.5]) 
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
            with m3:
                st.button("Connexion", key="nav_login", type="primary",
                         use_container_width=True,
                         on_click=navigate_to, args=("Login",))
