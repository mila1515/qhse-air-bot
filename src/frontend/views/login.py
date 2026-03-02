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
    # Déplacé dans app.py pour éviter les conflits et assurer la cohérence globale
    
    # --- HEADER / NAVBAR ---
    # Navbar gérée globalement dans app.py, on ne l'appelle plus ici pour éviter les doublons.

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
                                st.error("Identifiants incorrects. Vérifiez votre email et mot de passe.")
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
                                elif response is None:
                                    # L'erreur a déjà été affichée par auth_client
                                    pass
                                else:
                                    try:
                                        err_data = response.json()
                                        st.error(f"Erreur : {err_data.get('detail', 'Impossible de créer le compte.')}")
                                    except Exception as e:
                                        st.error(f"Une erreur est survenue (Status: {response.status_code}). Détails : {response.text[:200]}")
                    else:
                        st.warning("Veuillez remplir tous les champs.")

            # LIEN SWITCH MODE
            st.markdown("<div style='margin-top: 1rem; text-align: center;'>", unsafe_allow_html=True)
            st.button("Déjà un compte ? Se connecter", type="tertiary", key="btn_go_login", on_click=switch_to_login)
            st.markdown("</div>", unsafe_allow_html=True)
