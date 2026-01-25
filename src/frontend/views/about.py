import streamlit as st

def render_about():
    """
    Affiche la page "À propos" de l'application QHSE Air Bot.
    """
    
    # --- HEADER / NAVBAR ---
    # La navbar doit être affichée même ici pour la cohérence de navigation
    from src.frontend.views.components import render_navbar
    render_navbar()

    # --- Contenu Principal ---
    st.markdown("""
    <style>
        .about-header {
            font-size: 2.5rem;
            font-weight: 800;
            color: #2e7d32;
            text-align: center;
            margin-bottom: 2rem;
        }
        .about-section-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0277bd;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .about-text {
            font-size: 1rem;
            line-height: 1.6;
            color: #37474f;
            margin-bottom: 1rem;
            text-align: justify;
        }
        .about-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #f0f2f6;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Titre
    st.markdown('<div class="about-header">À propos de QHSE Air Bot</div>', unsafe_allow_html=True)

    # Mise en page centrée
    col_spacer_l, col_content, col_spacer_r = st.columns([1, 6, 1])

    with col_content:
        # Mission
        st.markdown('<div class="about-section-title">🌍 Notre Mission</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-card">
            <div class="about-text">
                <strong>QHSE Air Bot</strong> est né d'une volonté simple : rendre la gestion de la Qualité, de l'Hygiène, de la Sécurité et de l'Environnement (QHSE) accessible, rapide et intelligente.
            </div>
            <div class="about-text">
                Dans un monde industriel complexe, la conformité réglementaire et la sécurité des opérations sont primordiales. Notre assistant IA vous accompagne au quotidien pour décrypter les normes, surveiller la qualité de l'air et analyser les risques, afin de vous permettre de prendre des décisions éclairées et sécurisées.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Fonctionnalités Clés
        st.markdown('<div class="about-section-title">⚡ Fonctionnalités Clés</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3, gap="medium")
        
        with c1:
            st.markdown("""
            <div class="about-card" style="height: 100%;">
                <div style="font-weight: 600; color: #2e7d32; margin-bottom: 0.5rem;">💨 Qualité de l'Air (WAQI)</div>
                <div class="about-text">
                    Accédez aux données en temps réel sur la qualité de l'air dans vos villes d'intervention. Surveillez les indices de pollution et protégez la santé de vos collaborateurs.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown("""
            <div class="about-card" style="height: 100%;">
                <div style="font-weight: 600; color: #2e7d32; margin-bottom: 0.5rem;">📚 Base Réglementaire</div>
                <div class="about-text">
                    Interrogez instantanément le Code du Travail et les guides de l'INRS. Fini les recherches fastidieuses : posez votre question, obtenez la référence légale.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
            <div class="about-card" style="height: 100%;">
                <div style="font-weight: 600; color: #2e7d32; margin-bottom: 0.5rem;">⚠️ Sécurité Industrielle (ARIA)</div>
                <div class="about-text">
                    Analysez les accidents passés grâce à la base de données ARIA. Apprenez des retours d'expérience pour prévenir les risques futurs dans vos installations.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Technologie & Confidentialité
        st.markdown('<div class="about-section-title">🔒 Technologie & Confidentialité</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-card">
            <div class="about-text">
                Nous utilisons les dernières avancées en matière de <strong>LLM (Large Language Models)</strong> et d'architecture RAG (Retrieval-Augmented Generation) pour garantir la pertinence des réponses.
            </div>
            <div class="about-text">
                La confidentialité de vos données est notre priorité absolue. Vos documents et échanges ne servent pas à l'entraînement public des modèles. L'architecture est conçue pour cloisonner et sécuriser vos informations sensibles.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Footer About
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; color: #90a4ae; font-size: 0.9rem;">
            QHSE Air Bot — Développé pour l'excellence opérationnelle.
        </div>
        """, unsafe_allow_html=True)
