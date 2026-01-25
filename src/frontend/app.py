import streamlit as st
import sys
import os

# Ajout du dossier racine au sys.path pour résoudre les imports 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.frontend.utils.session import init_session_state, logout
from src.frontend.views import login, chat, conversations, notes

# Configuration de la page
st.set_page_config(
    page_title="QHSE Air Bot",
    page_icon="🤖",
    layout="wide"
)

# Initialisation de la session
init_session_state()

def main():
    # Gestion de la navigation interne (SPA)
    if "current_view" not in st.session_state:
        st.session_state.current_view = "Chat"

    if not st.session_state.token:
        # Si pas connecté, afficher uniquement la vue Login
        login.render_login()
    else:
        # Si connecté, afficher la Sidebar et le contenu
        with st.sidebar:
            st.title("🤖 QHSE Air Bot")
            if st.session_state.user:
                st.caption(f"Connecté : {st.session_state.user.get('email', 'User')}")
            
            st.divider()
            
            # Menu de navigation
            view = st.radio(
                "Menu", 
                ["Chat", "Conversations", "Notes"],
                index=["Chat", "Conversations", "Notes"].index(st.session_state.current_view)
            )
            
            # Mise à jour de l'état de la vue
            if view != st.session_state.current_view:
                st.session_state.current_view = view
                st.rerun()

            st.divider()
            if st.button("Se déconnecter", type="primary"):
                logout()

        # Rendu de la vue sélectionnée
        if st.session_state.current_view == "Chat":
            chat.render_chat()
        elif st.session_state.current_view == "Conversations":
            conversations.render_conversations()
        elif st.session_state.current_view == "Notes":
            notes.render_notes()

if __name__ == "__main__":
    main()
