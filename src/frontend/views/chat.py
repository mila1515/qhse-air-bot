import streamlit as st
from src.frontend.services import chat_client, conversations_client

def render_chat():
    st.title("💬 Assistant QHSE")
    
    # Gestion de la conversation active
    if not st.session_state.current_conversation_id:
        # Option pour créer une nouvelle conversation ou en sélectionner une
        if st.button("➕ Démarrer une nouvelle conversation", type="primary", use_container_width=True):
            resp = conversations_client.create_conversation("Nouvelle discussion")
            if resp and resp.status_code in [200, 201]:
                conv = resp.json()
                st.session_state.current_conversation_id = conv["id"]
                st.session_state.messages = []
                st.rerun()
            else:
                try:
                    err = resp.json().get("detail", resp.text) if resp else "Erreur connexion"
                except:
                    err = resp.text if resp else "Erreur connexion"
                st.error(f"Impossible de créer une conversation ({resp.status_code if resp else 'N/A'}): {err}")
    else:
        # Bouton pour fermer/changer de conversation (retour liste ou clear)
        if st.sidebar.button("Fermer la conversation"):
            st.session_state.current_conversation_id = None
            st.session_state.messages = []
            st.rerun()
    
        # Affichage de l'historique
        # Si messages vides mais conv active, charger historique
        if not st.session_state.messages and st.session_state.current_conversation_id:
            hist_resp = conversations_client.get_conversation_history(st.session_state.current_conversation_id)
            if hist_resp and hist_resp.status_code == 200:
                msgs = hist_resp.json()
                for m in msgs:
                    role = "user" if m.get("sender") == "user" else "assistant"
                    st.session_state.messages.append({"role": role, "content": m.get("content")})
    
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
        # Input utilisateur
        if prompt := st.chat_input("Posez votre question QHSE..."):
            # Afficher message user
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
    
            # Appel API
            with st.chat_message("assistant"):
                with st.spinner("Réflexion en cours..."):
                    resp = chat_client.send_chat_message(st.session_state.current_conversation_id, prompt)
                    if resp and resp.status_code == 200:
                        data = resp.json()
                        # Supporte ancien format ("answer") et nouveau format DB ("content")
                        answer = data.get("content") or data.get("answer") or data.get("response") or "Pas de réponse."
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        if resp:
                            try:
                                err_detail = resp.json().get("detail", resp.text)
                            except:
                                err_detail = resp.text
                            status_code = resp.status_code
                        else:
                            err_detail = "Erreur de connexion (Serveur injoignable ou timeout)"
                            status_code = "N/A"
                            
                        err_msg = f"Erreur serveur ({status_code}): {err_detail}"
                        st.error(err_msg)
                        st.session_state.messages.append({"role": "assistant", "content": err_msg})
