import streamlit as st
from src.frontend.services import auth_client
from src.frontend.utils.session import save_token
import os
import base64

def render_login():
    """
    Affiche la page d'authentification (Login/Register).
    Design sobre, professionnel et centré, sans emojis.
    Utilise st.radio pour la navigation et des liens pour basculer entre les modes.
    """
    
    # --- Init Session State ---
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Initialisation explicite de la clé du widget pour éviter le warning Streamlit
    if "auth_nav_radio" not in st.session_state:
        st.session_state.auth_nav_radio = "Se connecter" if st.session_state.auth_mode == "login" else "Créer un compte"

    # --- CSS Personnalisé ---
    st.markdown("""
    <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: #2c3e50;
        }

        /* Conteneur principal plus large pour la navbar */
        .block-container {
            padding-top: 6rem !important; /* Ajusté pour la navbar fixe */
            padding-bottom: 2rem !important;
            max-width: 1000px !important; /* Largeur augmentée pour la navbar */
            background-color: transparent;
        }

        /* Card Effect */
        .auth-card {
            background-color: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #f0f2f6;
        }

        /* Titre principal */
        .hero-title {
            font-size: 3rem; /* H1 Equivalent */
            font-weight: 800;
            color: #2e7d32; /* Vert professionnel */
            margin-bottom: 0.5rem;
            line-height: 1.2;
            text-align: center;
        }

        .auth-title {
            text-align: center;
            font-size: 1.8rem;
            font-weight: 700;
            color: #1b5e20;
            margin-bottom: 2rem;
            margin-top: 1rem;
        }

        /* Style des inputs */
        .stTextInput > div > div > input {
            border-radius: 6px;
            border: 1px solid #cfd8dc;
            padding: 0.5rem 1rem;
        }
        .stTextInput > div > div > input:focus {
            border-color: #81c784;
            box-shadow: 0 0 0 1px #81c784;
        }

        /* Boutons */
        div.stButton > button {
            width: 100%;
            border-radius: 6px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            margin-top: 0.5rem;
        }

        /* Bouton Login (Primary - Vert) */
        div.stButton > button[kind="primary"] {
            background-color: #81c784 !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #66bb6a !important;
        }

        /* Bouton Register (Secondary - Bleu) */
        div.stButton > button[kind="secondary"] {
            background-color: #e3f2fd !important;
            color: #0277bd !important;
            border: 1px solid #b3e5fc !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #b3e5fc !important;
        }

        /* Centrer le radio button horizontal */
        div.stRadio > div[role="radiogroup"] {
            justify-content: center;
            margin-bottom: 1rem;
        }
        
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER / NAVBAR ---
    from src.frontend.views.components import render_navbar
    render_navbar()

    # --- Callbacks pour le changement de mode ---
    def switch_to_register():
        st.session_state.auth_mode = "register"
        st.session_state.auth_nav_radio = "Créer un compte"

    def switch_to_login():
        st.session_state.auth_mode = "login"
        st.session_state.auth_nav_radio = "Se connecter"

    # --- Header Navigation (Bouton Retour) ---
    # Centered Layout for content to keep the form look nice
    col_spacer_left, col_content, col_spacer_right = st.columns([1, 1.5, 1])

    with col_content:
        # --- Titre ---
        st.markdown('<div class="auth-title">Authentification</div>', unsafe_allow_html=True)
        
        # --- Navigation Tabs (Radio) ---
        selected_tab = st.radio(
            "Mode d'authentification",
            ["Se connecter", "Créer un compte"],
            horizontal=True,
            label_visibility="collapsed",
            key="auth_nav_radio"
        )

        # Sync state from Radio input (if user clicked radio)
        if selected_tab == "Se connecter":
            st.session_state.auth_mode = "login"
        else:
            st.session_state.auth_mode = "register"

        # --- Render Forms ---
        if st.session_state.auth_mode == "login":
            # LOGIN FORM
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Mot de passe", type="password")
                
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                
                # Bouton "Se connecter" (Vert / Primary)
                submit_login = st.form_submit_button("Se connecter", type="primary")
                
                if submit_login:
                    if email and password:
                        with st.spinner("Connexion en cours..."):
                            response = auth_client.login_user(email, password)
                            if response and response.status_code == 200:
                                data = response.json()
                                save_token(data.get("access_token"))
                                
                                # Récupérer user info
                                user_resp = auth_client.get_current_user()
                                if user_resp and user_resp.status_code == 200:
                                    st.session_state.user = user_resp.json()
                                
                                st.success("Connexion réussie !")
                                st.rerun() 
                            else:
                                st.error("Identifiants incorrects.")
                    else:
                        st.warning("Veuillez remplir tous les champs.")

            # LIEN SWITCH MODE
            st.markdown("<div style='margin-top: 1rem; text-align: center;'>", unsafe_allow_html=True)
            st.button("Pas encore de compte ? S'inscrire ici", type="tertiary", key="btn_go_register", on_click=switch_to_register)
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            # REGISTER FORM
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            with st.form("register_form"):
                new_username = st.text_input("Nom d'utilisateur")
                new_email = st.text_input("Email")
                new_password = st.text_input("Mot de passe", type="password")
                confirm_password = st.text_input("Confirmer le mot de passe", type="password")
                
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                
                # Bouton "Créer un compte" (Bleu / Secondary)
                submit_register = st.form_submit_button("Créer un compte", type="secondary")
                
                if submit_register:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("Les mots de passe ne correspondent pas.")
                        else:
                            with st.spinner("Création du compte..."):
                                response = auth_client.register_user(new_email, new_password, new_username)
                                if response and response.status_code == 200:
                                    st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                                    # Optional: Auto switch to login
                                    # st.session_state.auth_mode = "login"
                                    # st.session_state.auth_nav_radio = "Se connecter"
                                    # st.rerun()
                                else:
                                    try:
                                        err_data = response.json()
                                        st.error(f"Erreur : {err_data.get('detail', 'Impossible de créer le compte.')}")
                                    except:
                                        st.error("Une erreur est survenue lors de la création du compte.")
                    else:
                        st.warning("Veuillez remplir tous les champs.")

            # LIEN SWITCH MODE
            st.markdown("<div style='margin-top: 1rem; text-align: center;'>", unsafe_allow_html=True)
            st.button("Déjà un compte ? Se connecter", type="tertiary", key="btn_go_login", on_click=switch_to_login)
            st.markdown("</div>", unsafe_allow_html=True)
