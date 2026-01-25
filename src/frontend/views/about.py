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
            margin-bottom: 3rem;
        }
        .about-section-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0277bd;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
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
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #f0f2f6;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Titre
    st.markdown('<div class="about-header">À propos de QHSE Air Bot</div>', unsafe_allow_html=True)

    # Mise en page centrée
    col_spacer_l, col_content, col_spacer_r = st.columns([1, 6, 1])

    with col_content:
        # 1. Notre Vision
        st.markdown('<div class="about-section-title">Notre Vision</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-card">
            <div class="about-text">
                L'industrie moderne fait face à une complexité croissante des normes environnementales et sécuritaires. 
                Notre vision est d'intégrer l'intelligence artificielle au cœur des processus QHSE pour transformer cette contrainte en levier de performance.
            </div>
            <div class="about-text">
                Nous croyons en une technologie qui assiste l'humain sans le remplacer, en fournissant une analyse rapide et fiable pour des décisions éclairées.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # 2. Notre Mission
        st.markdown('<div class="about-section-title">Notre Mission</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-text">
            <strong>QHSE Air Bot</strong> a pour mission de centraliser et simplifier l'accès à l'information critique :
        </div>
        <ul>
            <li class="about-text">Assurer une veille réglementaire proactive et précise.</li>
            <li class="about-text">Faciliter l'interprétation des textes officiels (Code du Travail, Guides INRS).</li>
            <li class="about-text">Surveiller en temps réel les indicateurs de qualité de l'air pour la protection des collaborateurs.</li>
        </ul>
        """, unsafe_allow_html=True)

        st.divider()

        # 3. Pour qui ?
        st.markdown('<div class="about-section-title">Pour qui ?</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3, gap="medium")
        
        with c1:
            st.markdown("""
            <div class="about-card" style="height: 100%; padding: 1.5rem;">
                <div style="font-weight: 700; color: #2e7d32; margin-bottom: 1rem; font-size: 1.1rem;">Responsables QHSE</div>
                <div class="about-text" style="font-size: 0.95rem;">
                    Pour optimiser la veille réglementaire, analyser les risques et garantir la conformité des sites industriels.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown("""
            <div class="about-card" style="height: 100%; padding: 1.5rem;">
                <div style="font-weight: 700; color: #2e7d32; margin-bottom: 1rem; font-size: 1.1rem;">Techniciens & Opérateurs</div>
                <div class="about-text" style="font-size: 0.95rem;">
                    Pour obtenir des réponses immédiates sur les procédures de sécurité et les normes applicables sur le terrain.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
            <div class="about-card" style="height: 100%; padding: 1.5rem;">
                <div style="font-weight: 700; color: #2e7d32; margin-bottom: 1rem; font-size: 1.1rem;">Managers & Directeurs</div>
                <div class="about-text" style="font-size: 0.95rem;">
                    Pour piloter la performance sécurité et disposer d'une vue synthétique des enjeux environnementaux.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # 4. Technologies Utilisées
        st.markdown('<div class="about-section-title">Technologies Utilisées</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-card">
            <div class="about-text">
                Notre solution repose sur une architecture technique robuste et innovante :
            </div>
            <div class="about-text">
                <strong>Intelligence Artificielle (RAG)</strong> : Combinaison de la recherche documentaire vectorielle et de la génération de texte pour des réponses contextuelles sourcées.
            </div>
            <div class="about-text">
                <strong>Analyse de Données Temps Réel</strong> : Connexion aux API de surveillance environnementale pour une réactivité immédiate.
            </div>
            <div class="about-text">
                <strong>Interface Streamlit</strong> : Une expérience utilisateur fluide et adaptée aux standards du web moderne.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # 5. Engagement sur la Confidentialité
        st.markdown('<div class="about-section-title">Engagement sur la Confidentialité</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-card" style="border-left: 5px solid #2e7d32;">
            <div class="about-text">
                La sécurité de vos données industrielles est une priorité absolue.
            </div>
            <div class="about-text">
                <strong>Cloisonnement des données</strong> : Vos documents internes et historiques de conversations sont strictement isolés.
            </div>
            <div class="about-text">
                <strong>Pas d'entraînement public</strong> : Aucune donnée client n'est utilisée pour l'entraînement des modèles de langage publics.
            </div>
            <div class="about-text">
                <strong>Transparence</strong> : Nous appliquons des protocoles stricts de gestion des accès et de chiffrement.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Footer About
        st.markdown("""
        <div style="text-align: center; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #eceff1; color: #90a4ae; font-size: 0.9rem;">
            © QHSE Air Bot — Solution Entreprise pour l'Excellence Opérationnelle.
        </div>
        """, unsafe_allow_html=True)
