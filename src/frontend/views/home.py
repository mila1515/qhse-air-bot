import streamlit as st

def render_home():
    """
    Affiche la page d'accueil (Landing Page) de l'application QHSE Air Bot.
    Respecte la charte graphique : Vert clair (dominant), Bleu très clair (secondaire), Pas d'emojis.
    """
    
    # --- CSS Personnalisé ---
    st.markdown("""
    <style>
        /* Import Font (optionnel, sinon utilise font système) */
        
        /* Global Container Styles */
        .main-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #2c3e50;
        }

        /* Réduction du padding par défaut de Streamlit en haut de page */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }

        /* Hero Section Text Styling */
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            color: #1b5e20; /* Vert encore plus profond pour le contraste */
            margin-bottom: 0.5rem;
            line-height: 1.1;
            text-align: left;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            color: #2e7d32;
            margin-bottom: 1rem;
            font-weight: 600;
            text-align: left;
        }
        .hero-desc {
            font-size: 1.1rem;
            color: #546e7a;
            margin-bottom: 2rem;
            line-height: 1.6;
            text-align: left;
            max-width: 90%;
        }

        /* Visual Placeholder in Right Column */
        .hero-visual {
            background: linear-gradient(135deg, #e8f5e9 0%, #e3f2fd 100%);
            border-radius: 20px;
            padding: 2rem;
            height: 100%;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            border: 1px solid #f1f8e9;
        }
        .hero-visual-text {
            color: #2e7d32;
            font-weight: 700;
            font-size: 1.2rem;
            text-align: center;
            opacity: 0.8;
        }
        
        /* Section Cards */
        .section-title {
            font-size: 2rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 2rem;
            margin-top: 3rem;
            text-align: center;
            position: relative;
        }
        .section-title::after {
            content: '';
            display: block;
            width: 60px;
            height: 4px;
            background-color: #66bb6a;
            margin: 10px auto 0;
            border-radius: 2px;
        }

        .feature-card {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #f0f2f6;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            height: 100%;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.05);
            border-color: #81d4fa;
        }
        .feature-header {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0277bd;
            margin-bottom: 1rem;
        }
        .feature-text {
            color: #546e7a;
            font-size: 1rem;
            line-height: 1.6;
        }

        /* Hack CSS pour forcer la couleur du bouton Primary (Connexion) en Vert Clair */
        div.stButton > button[kind="primary"],
        div.stButton button[kind="primary"],
        button[kind="primary"] {
            background-color: #66bb6a !important; /* Vert clair vibrant */
            color: white !important;
            border: none !important;
            border-radius: 8px !important; /* Arrondi standard plus pro */
            padding: 0.5rem 1.5rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            transition: all 0.2s ease !important;
            width: 100% !important; /* Prend la largeur de sa colonne */
        }
        div.stButton > button[kind="primary"]:hover,
        div.stButton button[kind="primary"]:hover,
        button[kind="primary"]:hover {
            background-color: #4caf50 !important; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        }
        
        /* Hack CSS pour le bouton Secondary (Créer un compte) */
         div.stButton > button[kind="secondary"],
         div.stButton button[kind="secondary"],
         button[kind="secondary"] {
            background-color: #e1f5fe !important; /* Fond bleu très pâle au lieu de transparent */
            border: 1px solid #81d4fa !important;
            color: #0277bd !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.5rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
         }
         div.stButton > button[kind="secondary"]:hover,
         div.stButton button[kind="secondary"]:hover,
         button[kind="secondary"]:hover {
            border-color: #4fc3f7 !important;
            color: #01579b !important;
            background-color: #b3e5fc !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
         }

        /* Footer */
        .footer {
            text-align: center;
            padding: 3rem 0;
            margin-top: 4rem;
            border-top: 1px solid #f0f2f6;
            color: #90a4ae;
            font-size: 0.85rem;
        }
        
        /* Message connecté */
        .connected-box {
            background-color: #f1f8e9;
            border: 1px solid #c5e1a5;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .connected-text {
            color: #2e7d32;
            font-weight: 600;
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Container Principal ---
    main_container = st.container()

    with main_container:
        # --- Gestion Utilisateur Connecté ---
        if st.session_state.token:
            st.markdown("""
            <div class="connected-box">
                <div class="connected-text">👋 Bonjour ! Vous êtes déjà connecté.</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Bouton d'accès direct au Chat (un peu isolé pour être clair)
            col_action, _ = st.columns([1, 2])
            with col_action:
                if st.button("Accéder au Chat", type="primary", use_container_width=True):
                    st.session_state.current_view = "Chat"
                    st.rerun()
            
            st.markdown("---") # Séparateur discret

        # --- Section Hero (2 Colonnes) ---
        col_hero_text, col_hero_visual = st.columns([1.2, 0.8], gap="large")

        with col_hero_text:
            # Titre H1
            st.markdown('<div class="hero-title">QHSE Air Bot</div>', unsafe_allow_html=True)
            # Sous-titre H2
            st.markdown('<div class="hero-subtitle">Votre assistant intelligent pour la qualité de l’air</div>', unsafe_allow_html=True)
            # Description
            st.markdown('<div class="hero-desc">Analysez vos documents, comprenez les normes et prenez des décisions éclairées grâce à une IA spécialisée en conformité QHSE.</div>', unsafe_allow_html=True)

            # Boutons d'action (Si non connecté)
            if not st.session_state.token:
                col_btn_login, col_btn_register, _ = st.columns([1, 1, 0.1], gap="small")
                
                with col_btn_login:
                    if st.button("Connexion", type="primary", use_container_width=True):
                        st.session_state.current_view = "Login"
                        st.rerun()
                
                with col_btn_register:
                    if st.button("Créer un compte", type="secondary", use_container_width=True):
                        st.session_state.current_view = "Login"
                        st.rerun()

        with col_hero_visual:
            # Image Logo + Texte
            import os
            # Chemin absolu vers l'image
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(current_dir, "..", "assets", "logo_home.png")
            
            # Conteneur pour l'image
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
            else:
                st.warning("Image logo_home.png introuvable")

            # Texte en dessous
            st.markdown("""
            <div class="hero-visual-text" style="margin-top: 1rem;">
                Analyse • Conformité • Sécurité
            </div>
            """, unsafe_allow_html=True)

        # --- Section "Pourquoi QHSE Air Bot ?" ---
        st.markdown('<div class="section-title">Pourquoi QHSE Air Bot ?</div>', unsafe_allow_html=True)

        row1_col1, row1_col2 = st.columns(2, gap="medium")
        
        with row1_col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-header">Optimisation du temps</div>
                <div class="feature-text">
                    Accédez instantanément à des réponses précises sur vos procédures et réglementations, sans perdre des heures à chercher dans vos documents.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True) # Spacer

            st.markdown("""
            <div class="feature-card">
                <div class="feature-header">Conformité simplifiée</div>
                <div class="feature-text">
                    Déchiffrez facilement les normes complexes (ISO 14001, 45001, etc.) et assurez-vous que vos opérations respectent les exigences légales.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with row1_col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-header">Sécurité et confidentialité</div>
                <div class="feature-text">
                    Vos données sensibles restent protégées. Notre architecture garantit que vos documents internes ne servent pas à entraîner des modèles publics.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True) # Spacer

            st.markdown("""
            <div class="feature-card">
                <div class="feature-header">Support décisionnel</div>
                <div class="feature-text">
                    Transformez vos données brutes en plans d'action concrets. L'IA vous aide à prioriser les risques et à identifier les opportunités d'amélioration.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
    <div class="footer">
        QHSE Air Bot — Plateforme Interne de Gestion QHSE<br>
        © 2026 Tous droits réservés
    </div>
    """, unsafe_allow_html=True)
