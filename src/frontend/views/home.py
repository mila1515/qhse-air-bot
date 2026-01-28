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
            padding-top: 6rem !important; /* Ajusté pour la navbar fixe */
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
            background-color: #ffffff; /* Fond blanc propre */
            padding: 2rem;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            height: 100%;
            min-height: 180px; /* Hauteur minimale uniforme */
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.2s ease-in-out;
        }
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            border-color: #b0bec5;
        }
        .feature-header {
            font-size: 1.25rem;
            font-weight: 700;
            color: #2e7d32; /* Vert professionnel */
            margin-bottom: 0.75rem;
            border-bottom: 2px solid #e8f5e9;
            padding-bottom: 0.5rem;
            width: 100%;
        }
        .feature-text {
            font-size: 0.95rem;
            color: #546e7a;
            line-height: 1.6;
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
                    st.session_state.auth_mode = "login"
                    st.session_state.auth_nav_radio = "Se connecter"
                    st.query_params["view"] = "Login"
                    st.rerun()
            with c_b2:
                if st.button("Créer un compte", type="secondary", use_container_width=True):
                    st.session_state.current_view = "Login"
                    st.session_state.auth_mode = "register"
                    st.session_state.auth_nav_radio = "Créer un compte"
                    st.query_params["view"] = "Login"
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

    # --- SECTION FEATURES ---
    st.markdown('<div class="section-title">Pourquoi QHSE Air Bot ?</div>', unsafe_allow_html=True)

    # Grille 2x2 organisée avec st.columns
    # Ligne 1 : Qualité de l'Air | Sécurité Industrielle
    c1, c2 = st.columns(2, gap="medium")
    
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">Qualité de l'Air</div>
            <div class="feature-text">Suivi en temps réel des indices de qualité de l'air et alertes pollution.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">Sécurité Industrielle</div>
            <div class="feature-text">Analyse des accidents et retour d'expérience sécurité.</div>
        </div>
        """, unsafe_allow_html=True)

    # Espace entre les lignes
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Ligne 2 : Réglementation & Normes | Assistance IA Experte
    c3, c4 = st.columns(2, gap="medium")
    
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">Réglementation & Normes</div>
            <div class="feature-text">Accès instantané au Code du Travail et guides INRS pour la conformité.</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">Assistance IA Experte</div>
            <div class="feature-text">Un assistant intelligent pour vos analyses et prises de décision QHSE.</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
    <div class="footer">
        QHSE Air Bot © 2026 — Assistant IA Professionnel
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    """
    Affiche le tableau de bord utilisateur connecté (SaaS Style).
    Carte blanche centrée avec 'Bonjour !' et bouton d'action.
    """
    # Style spécifique pour le dashboard
    st.markdown("""
    <style>
        .dashboard-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 60vh;
        }
        .dashboard-card {
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            padding: 3rem;
            text-align: center;
            max-width: 800px;
            width: 100%;
            border: 1px solid #e2e8f0;
        }
        .dashboard-title {
            color: #2c5282; /* Bleu demandé */
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .dashboard-subtitle {
            color: #4a5568; /* Gris demandé */
            font-size: 1.25rem;
            margin-bottom: 2.5rem;
        }
        div.stButton > button[kind="primary"] {
            background-color: #48bb78 !important; /* Vert demandé */
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.2s;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #38a169 !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(72, 187, 120, 0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Conteneur centré
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # On utilise st.columns pour centrer le contenu "Carte" (ou juste un conteneur markdown)
    # Mais on veut un bouton Streamlit interactif DEDANS.
    # Astuce : On crée la structure visuelle "Card" autour, et on place les éléments dedans.
    
    # Pour centrer parfaitement avec un bouton interactif, on utilise des colonnes vides
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Début Carte Visuelle
        st.markdown("""
        <div class="dashboard-card">
            <div class="dashboard-title">Bonjour !</div>
            <div class="dashboard-subtitle">Je suis prêt à vous aider sur vos questions.</div>
        """, unsafe_allow_html=True)
        
        # Bouton (Centré via colonnes internes ou CSS flex si possible, mais le bouton est un widget)
        # On ferme temporairement la div pour insérer le bouton, ou on le met juste après
        # Streamlit insère les widgets séquentiellement.
        
        # Pour que le bouton soit DANS la carte visuellement, c'est dur car st.button crée son propre bloc.
        # Solution : On fait tout en Markdown SAUF le bouton, et on essaie de l'intégrer.
        # OU : On utilise un st.container avec un style CSS appliqué via class.
        
        # Méthode Container
        with st.container():
             # On applique une classe à ce container via un hack CSS qui cible le parent ? Difficile.
             # On continue avec l'approche "Sandwich Markdown"
             pass
             
        # Fin de la partie haute de la carte
        # Bouton
        if st.button("Démarrer une nouvelle conversation", type="primary", use_container_width=True):
             st.session_state.current_view = "Chat"
             # Reset conversation ID if needed?
             # st.session_state.conversation_id = None 
             st.rerun()
             
        # Fin Carte
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
