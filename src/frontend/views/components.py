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
    BG_COLOR = "#ffffff"
    BORDER_COLOR = "#e2e8f0"
    TEXT_COLOR = "#4a5568" # Gris foncé
    ACTIVE_COLOR = "#2c7a7b" # Teal/Aqua plus foncé pour le texte actif
    ACCENT_COLOR = "#38b2ac" # Teal/Aqua clair pour la ligne
    
    current_view = st.session_state.get("current_view", "Home")
    user_email = "admin@qhse.com" # Valeur par défaut
    if st.session_state.get("user"):
        user_email = st.session_state.user.get("email", user_email)

    logo_b64 = get_base64_logo()
    logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""
    
    # --- Menu Items ---
    if st.session_state.get("token"):
        # Menu Connecté
        menu_items = [
            {"label": "Discussion", "view": "Chat"},
            {"label": "Historique", "view": "Conversations"},
            {"label": "Mes Notes", "view": "Notes"}
        ]
        
        # Right Side (Profile)
        # On utilise un avatar générique ou l'initiale
        initial = user_email[0].upper() if user_email else "U"
        
        right_section = f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="
                    width: 32px; height: 32px; border-radius: 50%; background-color: #e6fffa; color: {ACTIVE_COLOR};
                    display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;
                ">
                    {initial}
                </div>
                <div style="font-size: 14px; color: {TEXT_COLOR}; font-weight: 500;">
                    {user_email}
                </div>
            </div>
            <div style="width: 1px; height: 24px; background-color: #cbd5e0;"></div>
            <a href="?action=logout" target="_self" style="text-decoration: none; color: #e53e3e; font-size: 20px; display: flex; align-items: center;" title="Se déconnecter">
                <span style="font-size: 14px; font-weight: 500;">&times;</span>
            </a>
        </div>
        """
    else:
        # Menu Public
        menu_items = [
            {"label": "Accueil", "view": "Home"},
            {"label": "À propos", "view": "About"}
        ]
        
        right_section = f"""
        <div style="display: flex; gap: 15px;">
            <a href="?view=Login" target="_self" style="
                text-decoration: none; color: {ACTIVE_COLOR}; font-weight: 600; font-size: 14px; padding: 8px 16px;
            ">Connexion</a>
        </div>
        """

    # --- Construction du Menu HTML ---
    menu_html = ""
    for item in menu_items:
        is_active = (current_view == item["view"])
        active_style = f"color: {ACTIVE_COLOR}; border-bottom: 2px solid {ACCENT_COLOR};" if is_active else f"color: {TEXT_COLOR}; border-bottom: 2px solid transparent;"
        
        menu_html += f"""
        <a href="?view={item['view']}" target="_self" style="
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            padding: 0 4px;
            height: {NAV_HEIGHT};
            display: flex;
            align-items: center;
            margin: 0 12px;
            transition: all 0.2s ease;
            {active_style}
        ">
            {item['label']}
        </a>
        """

    # --- Rendu Final ---
    st.markdown(f"""
    <div style="
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
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    ">
        <div style="
            width: 100%;
            max-width: 1200px;
            padding: 0 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 100%;
        ">
            <!-- Left: Logo -->
            <div style="display: flex; align-items: center; gap: 12px;">
                <img src="{logo_src}" style="height: 40px; width: auto;" alt="Logo">
                <span style="font-family: 'Inter', sans-serif; font-weight: 700; font-size: 18px; color: #2d3748;">
                    QHSE Air Bot
                </span>
            </div>
            
            <!-- Center: Menu -->
            <div style="display: flex; height: 100%;">
                {menu_html}
            </div>
            
            <!-- Right: Profile/Actions -->
            <div>
                {right_section}
            </div>
        </div>
    </div>
    <div style="height: {NAV_HEIGHT};"></div> <!-- Spacer pour ne pas cacher le contenu -->
    """, unsafe_allow_html=True)
