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
    Affiche la barre de navigation du site avec le style demandé.
    Utilise des liens HTML avec query params pour la navigation.
    """
    NAV_BG = "#F5F5F5"
    NAV_TEXT = "#2E8B57"
    
    logo_b64 = get_base64_logo()
    logo_img_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:40px; margin-right:10px; vertical-align: middle;">' if logo_b64 else ""

    # On utilise l'URL relative pour la navigation
    # ?view=Home, ?view=Login
    
    st.markdown( 
        f""" 
        <div style="background-color:{NAV_BG}; padding:10px 20px; border-radius:8px; display:flex; align-items:center; justify-content:space-between; margin-bottom: 2rem;"> 
            <div style="display:flex; align-items:center;">
                {logo_img_html}
                <div style="font-weight:bold; font-size:20px; color:{NAV_TEXT};">QHSE Air Bot</div> 
            </div>
            <div style="display:flex; gap:30px;"> 
                <a href="?view=Home" target="_self" style="text-decoration:none; color:{NAV_TEXT}; font-size:16px;">Accueil</a> 
                <a href="?view=About" target="_self" style="text-decoration:none; color:{NAV_TEXT}; font-size:16px;">À propos</a> 
                <a href="?view=Login" target="_self" style="text-decoration:none; color:{NAV_TEXT}; font-size:16px;">Connexion</a> 
            </div> 
        </div> 
        """, 
        unsafe_allow_html=True 
    )
