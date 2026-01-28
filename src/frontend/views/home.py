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

        /* Réduction du padding haut de page pour Home */
        div.block-container {
            padding-top: 4rem !important; /* Ajusté pour coller à la navbar (70px) */
            padding-bottom: 2rem !important;
            max-width: 1000px !important; 
        }

        /* Hero Section */
        .hero-container {
            text-align: center;
            padding: 0 !important;
            margin-top: 0; 
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .hero-logo-container {
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: center;
        }
        
        .hero-logo-img {
            max-height: 100px; /* Logo un peu plus discret */
            width: auto;
            object-fit: contain;
        }

        .hero-title {
            font-size: 2.5rem; /* Titre plus compact */
            font-weight: 800;
            color: #2e7d32;
            margin-bottom: 0.25rem; /* Collé au sous-titre */
            line-height: 1.1;
            text-align: center;
        }
        
        .hero-subtitle {
            font-size: 1.15rem;
            color: #37474f;
            margin-bottom: 1.5rem; /* Rapproche les boutons */
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
    # Navbar gérée globalement dans app.py, on ne l'appelle plus ici pour éviter les doublons.
    
    # --- Defensive Routing ---
    # Si par erreur app.py route un utilisateur connecté vers render_home, on redirige vers la bonne vue.
    if st.session_state.get("token"):
        current = st.session_state.get("current_view", "Home")
        if current == "Chat":
            from src.frontend.views import chat
            chat.render_chat()
        elif current == "Conversations":
            from src.frontend.views import conversations
            conversations.render_conversations()
        elif current == "Notes":
            from src.frontend.views import notes
            notes.render_notes()
        elif current == "Profile":
            from src.frontend.views import profile
            profile.render_profile()
        else:
            render_dashboard()
        return

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
<div style="display: flex; justify-content: center; margin-bottom: 0.5rem; margin-top: -3rem;">
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
        st.markdown("""<div class="feature-card"><div class="feature-header">Réglementation & Normes</div><div class="feature-text">Accès instantané au Code du Travail et guides INRS pour la conformité.</div></div>""", unsafe_allow_html=True)

    with c4:
        st.markdown("""<div class="feature-card"><div class="feature-header">Assistance IA Experte</div><div class="feature-text">Un assistant intelligent pour vos analyses et prises de décision QHSE.</div></div>""", unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""<div class="footer">QHSE Air Bot © 2026 — Assistant IA Professionnel</div>""", unsafe_allow_html=True)

def render_dashboard():
    """
    Affiche le tableau de bord utilisateur connecté (SaaS Style).
    Design professionnel, épuré, avec accès rapide aux fonctionnalités.
    """
    # Récupération du nom de l'utilisateur
    user = st.session_state.get("user", {})
    email = user.get("email", "")
    if email:
        # Extraction propre du nom (ex: jean.dupont -> Jean Dupont)
        raw_name = email.split("@")[0]
        name = " ".join([n.capitalize() for n in raw_name.replace(".", " ").replace("_", " ").split()])
    else:
        name = "Utilisateur"

    # --- CSS Spécifique Dashboard ---
    st.markdown("""
    <style>
        /* Container Global Dashboard */
        .dashboard-wrapper {
            max_width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }

        /* Header Section */
        .dash-header {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 3rem 2rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .dash-welcome h1 {
            color: #2c3e50;
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.5px;
        }
        
        .dash-welcome p {
            color: #64748b;
            font-size: 1.1rem;
            margin: 0;
        }

        .dash-date {
            text-align: right;
            color: #94a3b8;
            font-size: 0.9rem;
            font-weight: 500;
        }

        /* Grid Cards */
        .action-card {
            background-color: white;
            border-radius: 12px;
            padding: 2rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: default; /* Les boutons font l'action */
        }
        
        .action-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.08);
            border-color: #cbd5e1;
        }

        .card-icon {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: #38b2ac; /* Teal */
            background: #e6fffa;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 0.75rem;
        }
        
        .card-desc {
            font-size: 0.95rem;
            color: #718096;
            line-height: 1.5;
            margin-bottom: 1.5rem;
            flex-grow: 1;
        }

        /* Stats Section */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #38b2ac;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .stat-label {
            color: #64748b;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        
        /* Section Titles */
        .section-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: #4a5568;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .section-header::after {
            content: "";
            flex-grow: 1;
            height: 1px;
            background: #e2e8f0;
        }

    </style>
    """, unsafe_allow_html=True)

    from datetime import datetime
    import locale
    
    # Date du jour (Format FR si possible, sinon simple)
    date_str = datetime.now().strftime("%d %B %Y")
    
    # --- UI STRUCTURE ---
    
    # 1. Header Welcome
    st.markdown(f"""
    <div class="dash-header">
        <div class="dash-welcome">
            <h1>Bonjour, {name}</h1>
            <p>Heureux de vous revoir. Votre espace QHSE est prêt.</p>
        </div>
        <div class="dash-date">
            {date_str}<br>
            <span style="color: #38b2ac;">• En ligne</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Quick Stats (Mockup pour l'immersion pro)
    # Dans un vrai cas, on ferait des requêtes DB pour avoir les vrais chiffres
    st.markdown('<div class="section-header">VUE D\'ENSEMBLE</div>', unsafe_allow_html=True)
    
    c_stat1, c_stat2, c_stat3, c_stat4 = st.columns(4)
    with c_stat1:
        st.markdown("""
        <div class="stat-card" style="border-left-color: #4299e1;">
            <div class="stat-value">12</div>
            <div class="stat-label">Conversations</div>
        </div>
        """, unsafe_allow_html=True)
    with c_stat2:
        st.markdown("""
        <div class="stat-card" style="border-left-color: #48bb78;">
            <div class="stat-value">85%</div>
            <div class="stat-label">Conformité</div>
        </div>
        """, unsafe_allow_html=True)
    with c_stat3:
        st.markdown("""
        <div class="stat-card" style="border-left-color: #ed8936;">
            <div class="stat-value">3</div>
            <div class="stat-label">Notes actives</div>
        </div>
        """, unsafe_allow_html=True)
    with c_stat4:
        st.markdown("""
        <div class="stat-card" style="border-left-color: #9f7aea;">
            <div class="stat-value">IA</div>
            <div class="stat-label">Assistant Prêt</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

    # 3. Actions Grid
    st.markdown('<div class="section-header">ACCÈS RAPIDE</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")

    # Card 1: Chat
    with col1:
        st.markdown("""
        <div class="action-card">
            <div>
                <div class="card-icon">💬</div>
                <div class="card-title">Assistant QHSE</div>
                <div class="card-desc">
                    Interrogez vos documents, analysez les risques et obtenez des réponses normatives immédiates.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Bouton séparé pour la gestion d'état Streamlit
        if st.button("Nouvelle conversation", key="btn_chat", type="primary", use_container_width=True):
            st.session_state.current_view = "Chat"
            st.rerun()

    # Card 2: Historique
    with col2:
        st.markdown("""
        <div class="action-card">
            <div>
                <div class="card-icon">📂</div>
                <div class="card-title">Mes Dossiers</div>
                <div class="card-desc">
                    Retrouvez l'historique de vos échanges, reprenez vos analyses et exportez vos rapports.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Voir l'historique", key="btn_history", use_container_width=True):
            st.session_state.current_view = "Conversations"
            st.rerun()

    # Card 3: Notes & Outils
    with col3:
        st.markdown("""
        <div class="action-card">
            <div>
                <div class="card-icon">📝</div>
                <div class="card-title">Bloc-Notes & Profil</div>
                <div class="card-desc">
                    Gérez vos notes personnelles et configurez vos préférences utilisateur.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Double boutons pour cette carte
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("Notes", key="btn_notes", use_container_width=True):
                st.session_state.current_view = "Notes"
                st.rerun()
        with c_btn2:
            if st.button("Profil", key="btn_profile", use_container_width=True):
                st.session_state.current_view = "Profile"
                st.rerun()
