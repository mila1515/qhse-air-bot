import streamlit as st
import base64
from pathlib import Path
from src.frontend.services import conversations_client, notes_client
from src.frontend.views.components import get_base64_logo

def navigate_to(view_name):
    """Callback pour la navigation via boutons"""
    st.session_state.current_view = view_name
    st.query_params["view"] = view_name

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
        
        /* Hero Section */
        .hero-container {
            text-align: center;
            padding: 0 !important;
            margin-top: 0; 
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .hero-title {
            font-size: 2.5rem; 
            font-weight: 800;
            color: #000000; /* Noir Professionnel */
            margin-bottom: 1rem;
            line-height: 1.2;
            text-align: center;
            letter-spacing: -1px;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: #64748b; /* Slate 500 */
            margin-bottom: 2.5rem;
            font-weight: 400;
            text-align: center;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }

        /* Boutons Hero */
        div.stButton > button[kind="primary"] {
            background-color: #48BB78 !important; /* Vert Émeraude */
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px -1px rgba(72, 187, 120, 0.4) !important;
            width: 100%;
            font-size: 1rem !important;
            transition: all 0.2s ease;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #38a169 !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(72, 187, 120, 0.5) !important;
        }

        div.stButton > button[kind="secondary"] {
            background-color: white !important;
            color: #334155 !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            width: 100%;
            font-size: 1rem !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
            transition: all 0.2s ease;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #f8fafc !important;
            border-color: #94a3b8 !important;
            color: #0f172a !important;
            transform: translateY(-2px);
        }

        /* Features Section */
        .section-title {
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
            margin: 4rem 0 3rem 0;
            text-align: center;
            letter-spacing: -0.5px;
        }
        
        .feature-card {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0; /* Bordure épurée */
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); /* Ombre douce */
            height: 100%;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        /* Animation au survol sans passer sous la navbar (grâce au z-index navbar élevé) */
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-color: #cbd5e1;
        }
        .feature-header {
            font-size: 1.25rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.75rem;
            /* Pas d'emojis demandés */
        }
        .feature-text {
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
        }

        /* Footer */
        .footer {
            margin-top: 5rem;
            padding-top: 2rem;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            color: #94a3b8;
            font-size: 0.875rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- MAIN CONTENT ---
    # Utilisez des containers Streamlit pour isoler les sections
    with st.container():
        # Utilisation de colonnes pour centrer le logo et le texte proprement
        _, center_col, _ = st.columns([1, 4, 1])
        
        with center_col:
            logo_b64 = get_base64_logo()
            if logo_b64:
                st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <img src="data:image/png;base64,{logo_b64}" style="max-width: 160px; height: auto;">
                        <h1 class="hero-title">QHSE Air Bot</h1>
                        <p class="hero-subtitle">
                            Analysez vos documents, comprenez les normes et prenez des décisions éclairées grâce à notre assistant intelligent.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Boutons d'action (Centrés)
            c_b1, c_b2 = st.columns(2, gap="medium")
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
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Pourquoi QHSE Air Bot ?</div>', unsafe_allow_html=True)

    # Grille 2x2 organisée avec st.columns
    # Ligne 1
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">Qualité de l'Air</div>
            <div class="feature-text">Suivez en temps réel les indices de qualité de l'air et recevez des alertes pollution proactives.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">Sécurité Industrielle</div>
            <div class="feature-text">Analysez les rapports d'accidents et bénéficiez d'un retour d'expérience structuré pour améliorer la sécurité.</div>
        </div>
        """, unsafe_allow_html=True)

    # Espace entre les lignes
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # Ligne 2
    c3, c4 = st.columns(2, gap="large")
    
    with c3:
        st.markdown("""<div class="feature-card"><div class="feature-header">Réglementation & Normes</div><div class="feature-text">Accédez instantanément aux articles du Code du Travail et aux guides INRS pour garantir votre conformité.</div></div>""", unsafe_allow_html=True)

    with c4:
        st.markdown("""<div class="feature-card"><div class="feature-header">Assistance IA Experte</div><div class="feature-text">Posez vos questions techniques à un assistant intelligent spécialisé dans le domaine QHSE.</div></div>""", unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""<div class="footer">© 2026 QHSE Air Bot — Sécurité, Qualité et Environnement augmentés par l'IA.</div>""", unsafe_allow_html=True)

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
            background: linear-gradient(135deg, #e0f2f1 0%, #ffffff 100%); /* Fond plus "Air/Clean" */
            padding: 2.5rem 2rem;
            border-radius: 16px;
            border: 1px solid #b2dfdb; /* Teal très clair */
            box-shadow: 0 4px 12px -2px rgba(0, 105, 92, 0.05);
            margin-bottom: 3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .dash-welcome h1 {
            color: #004d40; /* Teal Foncé */
            font-size: 2rem;
            font-weight: 800;
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.5px;
        }
        
        .dash-welcome p {
            color: #00695c; /* Teal Medium */
            font-size: 1.05rem;
            margin: 0;
            opacity: 0.9;
        }

        .dash-date {
            text-align: right;
            color: #546e7a; /* Blue Grey */
            font-size: 0.9rem;
            font-weight: 600;
        }

        /* Grid Cards */
        .action-card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
            /* Bordure top colorée subtile */
            border-top: 4px solid transparent; 
        }
        
        .action-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-color: #b2dfdb;
            border-top-color: #0d9488; /* Teal Accent au survol */
        }

        .card-icon {
            font-size: 2.5rem;
            margin-bottom: 1.25rem;
            color: #0d9488; /* Teal 600 */
            background: #f0fdfa; /* Teal 50 */
            width: 70px;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            transition: transform 0.3s ease;
        }
        
        .action-card:hover .card-icon {
            transform: scale(1.1) rotate(5deg);
            background: #e0f2f1;
        }
        
        .card-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.75rem;
        }
        
        .card-desc {
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.6;
            margin-bottom: 2rem; /* Espace pour les boutons */
            flex-grow: 1;
        }

        /* Boutons Personnalisés via CSS Injection pour Streamlit */
        /* Cible les boutons Primary (Vert/Teal) */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px -1px rgba(13, 148, 136, 0.3) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.4) !important;
            transform: translateY(-2px) !important;
        }

        /* Cible les boutons Secondary (Contour) */
        div.stButton > button[kind="secondary"] {
            background: white !important;
            border: 2px solid #e2e8f0 !important;
            color: #475569 !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            border-color: #0d9488 !important;
            color: #0d9488 !important;
            background: #f0fdfa !important;
        }

        /* Section Titles */
        .section-header {
            font-size: 0.9rem;
            font-weight: 700;
            color: #94a3b8;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .section-header::after {
            content: "";
            flex-grow: 1;
            height: 2px;
            background: #f1f5f9;
            border-radius: 2px;
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

    # 2. Quick Stats (Données Réelles)
    # BLOC SUPPRIMÉ SUR DEMANDE UTILISATEUR
    # Récupération des données réelles via API
    # try:
    #     convs_resp = conversations_client.get_conversations()
    #     convs_count = len(convs_resp.json()) if convs_resp and convs_resp.status_code == 200 else 0
    # except:
    #     convs_count = 0
        
    # st.markdown('<div class="section-header">VUE D\'ENSEMBLE</div>', unsafe_allow_html=True)
    
    # c_stat1, c_stat2, c_stat3, c_stat4 = st.columns(4)
    # with c_stat1:
    #     st.markdown(f"""
    #     <div class="stat-card" style="border-left-color: #4299e1;">
    #         <div class="stat-value">{convs_count}</div>
    #         <div class="stat-label">Conversations</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    # with c_stat2:
    #     st.markdown("""
    #     <div class="stat-card" style="border-left-color: #48bb78;">
    #         <div class="stat-value">85%</div>
    #         <div class="stat-label">Conformité</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    # with c_stat3:
    #     st.markdown("""
    #     <div class="stat-card" style="border-left-color: #48bb78;">
    #         <div class="stat-value">1500+</div>
    #         <div class="stat-label">Sources RAG</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    # with c_stat4:
    #     st.markdown("""
    #     <div class="stat-card" style="border-left-color: #9f7aea;">
    #         <div class="stat-value">IA</div>
    #         <div class="stat-label">Assistant Prêt</div>
    #     </div>
    #     """, unsafe_allow_html=True)

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
        st.button("Nouvelle conversation", key="btn_chat", type="primary", use_container_width=True, 
                 on_click=navigate_to, args=("Chat",))

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
        st.button("Voir l'historique", key="btn_history", use_container_width=True,
                 on_click=navigate_to, args=("Conversations",))

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
            st.button("Notes", key="btn_notes", use_container_width=True,
                     on_click=navigate_to, args=("Notes",))
        with c_btn2:
            st.button("Profil", key="btn_profile", use_container_width=True,
                     on_click=navigate_to, args=("Profile",))
