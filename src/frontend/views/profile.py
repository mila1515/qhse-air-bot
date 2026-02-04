import streamlit as st
from src.frontend.utils.session import logout

def render_profile():
    st.markdown("## Mon Profil")
    
    user = st.session_state.user or {}
    email = user.get("email", "utilisateur@exemple.com")
    
    # Section 1 : Informations et Mise à jour
    with st.container(border=True):
        st.subheader("Mise à jour du profil")
        
        # Affichage des infos de base
        st.text_input("Email", value=email, disabled=True)
        
        # Formulaire simple pour le changement de mot de passe
        with st.expander("Changer mon mot de passe"):
            with st.form("password_change"):
                st.text_input("Nouveau mot de passe", type="password")
                st.text_input("Confirmer le mot de passe", type="password")
                if st.form_submit_button("Mettre à jour", type="primary"):
                    st.info("Fonctionnalité de changement de mot de passe à venir.")

    st.markdown("---")

    # Section 2 : Déconnexion
    st.subheader("Déconnexion")
    st.write("Cliquez ci-dessous pour vous déconnecter de l'application.")
    
    if st.button("Se déconnecter", type="secondary", use_container_width=True):
        logout()
