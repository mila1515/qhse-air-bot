import streamlit as st
from src.frontend.utils.session import logout

def render_profile():
    """
    Affiche la page de profil utilisateur.
    Permet de visualiser les informations et (futurement) de les mettre à jour.
    """
    
    # --- Header ---
    st.markdown("## Mon Profil")
    st.markdown("Gérez vos informations personnelles et vos préférences.")
    st.divider()

    # --- Layout ---
    col_info, col_update = st.columns([1, 2], gap="large")

    user = st.session_state.user or {}
    email = user.get("email", "Non renseigné")
    user_id = user.get("id", "N/A")

    with col_info:
        st.markdown("### Mes Informations")
        
        # Carte d'identité visuelle
        st.markdown(f"""
        <div style="
            background-color: white; 
            padding: 2rem; 
            border-radius: 12px; 
            border: 1px solid #e0e0e0;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        ">
            <div style="
                width: 80px; 
                height: 80px; 
                background-color: #e3f2fd; 
                color: #0277bd; 
                border-radius: 50%; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                font-size: 2rem; 
                font-weight: bold;
                margin: 0 auto 1rem auto;
            ">
                {email[0].upper() if email else "?"}
            </div>
            <div style="font-weight: 600; font-size: 1.1rem; color: #37474f; margin-bottom: 0.5rem; word-break: break-all;">
                {email}
            </div>
            <div style="font-size: 0.8rem; color: #90a4ae;">
                ID: {user_id}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Se déconnecter", type="secondary", use_container_width=True):
            logout()

    with col_update:
        st.markdown("### Mettre à jour le profil")
        
        with st.container(border=True):
            st.info("La modification du profil sera disponible prochainement.")
            
            # Formulaire (Désactivé pour l'instant ou Mock)
            st.text_input("Nom d'utilisateur", value=email.split('@')[0], disabled=True)
            st.text_input("Email", value=email, disabled=True)
            
            st.markdown("#### Changer le mot de passe")
            new_pass = st.text_input("Nouveau mot de passe", type="password")
            confirm_pass = st.text_input("Confirmer le mot de passe", type="password")
            
            if st.button("Enregistrer les modifications", type="primary"):
                if new_pass != confirm_pass:
                    st.error("Les mots de passe ne correspondent pas.")
                else:
                    st.warning("Cette fonctionnalité nécessite une mise à jour du serveur.")

