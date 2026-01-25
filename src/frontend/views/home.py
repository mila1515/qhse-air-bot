import streamlit as st
import base64
from pathlib import Path

def render_home():
    """
    Affiche la page d'accueil (Landing Page) de l'application QHSE Air Bot.
    Respecte la charte graphique : Vert clair (dominant), Bleu très clair (secondaire), Pas d'emojis.
    """
    
    # --- CSS Personnalisé ---
    st.markdown("""
    <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: #2c3e50;
        }

        /* Réduction drastique du padding haut de page */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 1000px !important; /* Contenu plus compact */
        }

        /* Hero Section */
        .hero-container {
            text-align: center;
            padding: 2rem 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .hero-logo-container {
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: center;
        }
        
        .hero-logo-img {
            max-height: 120px;
            width: auto;
            object-fit: contain;
        }

        .hero-title {
            font-size: 3rem; /* H1 Equivalent */
            font-weight: 800;
            color: #2e7d32; /* Vert professionnel */
            margin-bottom: 0.5rem;
            line-height: 1.2;
            text-align: center;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: #37474f; /* Gris foncé professionnel */
            margin-bottom: 2rem;
            font-weight: 400;
            text-align: center;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }

        /* Boutons */
        div.stButton > button[kind="primary"] {
            background-color: #81c784 !important; /* Vert clair plus doux */
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.5rem 2rem !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
            width: 100%;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #66bb6a !important;
        }

        div.stButton > button[kind="secondary"] {
            background-color: #e3f2fd !important; /* Bleu très clair */
            color: #0277bd !important;
            border: 1px solid #b3e5fc !important;
            border-radius: 6px !important;
            padding: 0.5rem 2rem !important;
            font-weight: 600 !important;
            width: 100%;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #b3e5fc !important;
        }

        /* Features Section */
        .section-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: #2c3e50;
            margin: 4rem 0 2rem 0;
            text-align: center;
        }
        
        .feature-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #f0f2f6;
            height: 100%;
            text-align: left;
        }
        .feature-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: #2e7d32; /* Vert cohérent */
            margin-bottom: 0.5rem;
        }
        .feature-text {
            font-size: 0.95rem;
            color: #546e7a;
            line-height: 1.5;
        }

        /* Footer */
        .footer {
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #f0f2f6;
            text-align: center;
            color: #cfd8dc;
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Container Principal ---
    # Centrage vertical global si peu de contenu, mais ici on veut surtout contrôler le haut
    
    # --- HEADER / NAVBAR ---
    from src.frontend.views.components import render_navbar
    render_navbar()

    # --- MAIN CONTENT (Subtitle + Buttons) ---
    # Centered Layout for content since logo is now in navbar
    
    col_main_space, col_main_content, col_main_space2 = st.columns([1, 6, 1])
    
    with col_main_content:
        # --- LOGO CENTRAL ---
        # Chargement du logo pour affichage central
        logo_path = Path("src/frontend/assets/logo_home.png")
        logo_html = ""
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
            logo_html = f"""
            <div style="display: flex; justify-content: center; margin-bottom: 0.5rem; margin-top: -1rem;">
                <img src="data:image/png;base64,{logo_b64}" style="max-width: 180px; height: auto;" alt="QHSE Air Bot Logo">
            </div>
            """
        
        st.markdown(logo_html, unsafe_allow_html=True)

        # Sous-titre centré
        st.markdown("""
        <div class="hero-subtitle" style="text-align: center; margin-left: auto; margin-right: auto; max-width: 800px; margin-bottom: 1rem;">
            Analysez vos documents, comprenez les normes et prenez des décisions éclairées.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
        
        # Boutons d'action (Centrés)
        if not st.session_state.token:
            # Centering buttons using a single container via markdown/css hack or just wider columns
            # Using wider columns for buttons to prevent wrapping
            c_b_space1, c_b1, c_b2, c_b_space2 = st.columns([1, 3, 3, 1])
            with c_b1:
                if st.button("Connexion", type="primary", use_container_width=True):
                    st.session_state.current_view = "Login"
                    st.rerun()
            with c_b2:
                if st.button("Créer un compte", type="secondary", use_container_width=True):
                    st.session_state.current_view = "Login"
                    st.rerun()
        else:
            # Si connecté
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem; color: #2e7d32; font-weight: 600;">
                👋 Vous êtes connecté
            </div>
            """, unsafe_allow_html=True)
            # Center the button
            c_b_space1, c_b1, c_b_space2 = st.columns([3, 2, 3])
            with c_b1:
                if st.button("Accéder au Chat", type="primary", use_container_width=True):
                    st.session_state.current_view = "Chat"
                    st.rerun()

    # (Suppression de l'ancien layout 2 colonnes avec logo à droite)

    # --- SECTION FEATURES ---
    st.markdown('<div class="section-title">Pourquoi QHSE Air Bot ?</div>', unsafe_allow_html=True)

    # Grille 2x2 compacte
    f_col1, f_col2 = st.columns(2, gap="medium")
    
    with f_col1:
        st.markdown("""
        <div class="feature-card" style="margin-bottom: 1rem;">
            <div class="feature-header">Optimisation du temps</div>
            <div class="feature-text">Accès rapide à des réponses QHSE fiables via IA.</div>
        </div>
        <div class="feature-card">
            <div class="feature-header">Conformité simplifiée</div>
            <div class="feature-text">Aide à la compréhension des normes et exigences légales.</div>
        </div>
        """, unsafe_allow_html=True)

    with f_col2:
        st.markdown("""
        <div class="feature-card" style="margin-bottom: 1rem;">
            <div class="feature-header">Sécurité & Confidentialité</div>
            <div class="feature-text">Données et historiques protégés, aucun entraînement public.</div>
        </div>
        <div class="feature-card">
            <div class="feature-header">Support décisionnel</div>
            <div class="feature-text">Analyses claires pour faciliter vos actions QHSE.</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
    <div class="footer">
        QHSE Air Bot © 2026 — Assistant IA Professionnel
    </div>
    """, unsafe_allow_html=True)
