import streamlit as st
import sys
import os

# Fix path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.frontend.api import auth_client
from src.frontend.utils.session import init_session_state

st.set_page_config(page_title="Login - QHSE Bot", page_icon="🔐")
init_session_state()

st.title("🔐 Authentification")

tab1, tab2 = st.tabs(["Se connecter", "Créer un compte"])

with tab1:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        submit_login = st.form_submit_button("Se connecter")
        
        if submit_login:
            if email and password:
                with st.spinner("Connexion en cours..."):
                    response = auth_client.login_user(email, password)
                    if response and response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data.get("access_token")
                        # Récupérer les infos utilisateur
                        user_resp = auth_client.get_current_user()
                        if user_resp and user_resp.status_code == 200:
                            st.session_state.user = user_resp.json()
                        st.success("Connexion réussie ! Allez sur la page 'Chat' pour commencer.")
                        st.rerun()
                    else:
                        st.error("Échec de la connexion. Vérifiez vos identifiants.")
            else:
                st.warning("Veuillez remplir tous les champs.")

with tab2:
    with st.form("register_form"):
        new_email = st.text_input("Email")
        new_password = st.text_input("Mot de passe", type="password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password")
        submit_register = st.form_submit_button("S'inscrire")
        
        if submit_register:
            if new_email and new_password:
                if new_password != confirm_password:
                    st.error("Les mots de passe ne correspondent pas.")
                else:
                    with st.spinner("Création du compte..."):
                        response = auth_client.register_user(new_email, new_password)
                        if response and response.status_code == 200: # Ou 201
                            st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                        else:
                            detail = response.json().get("detail", "Erreur inconnue") if response else "Erreur de connexion API"
                            st.error(f"Erreur lors de l'inscription : {detail}")
            else:
                st.warning("Veuillez remplir tous les champs.")
