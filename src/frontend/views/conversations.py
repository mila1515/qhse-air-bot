import streamlit as st
from src.frontend.services import conversations_client

def render_conversations():
    st.markdown("## 🗂️ Historique des Conversations")
    
    # Bouton rafraîchir
    if st.button("Rafraîchir la liste"):
        st.rerun()
    
    # Récupération des conversations
    resp = conversations_client.get_conversations()
    if resp and resp.status_code == 200:
        conversations = resp.json()
        
        if not conversations:
            st.info("Aucune conversation trouvée.")
        else:
            # Affichage sous forme de liste ou tableau
            for conv in conversations:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([5, 2, 1], vertical_alignment="center")
                    
                    with col1:
                        title = conv.get("title", "Conversation sans titre")
                        date_str = conv.get("updated_at", conv.get("created_at", "N/A"))[:10]
                        st.write(f"**{title}**")
                        st.caption(f"📅 {date_str}")
                    
                    with col2:
                        if st.button("Continuer ➡️", key=f"open_{conv['id']}", use_container_width=True):
                            st.session_state.current_conversation_id = conv['id']
                            st.session_state.messages = [] # Reset messages local cache
                            st.session_state.current_view = "Chat"
                            st.rerun()
                    
                    with col3:
                        if st.button("🗑️", key=f"del_{conv['id']}", help="Supprimer", use_container_width=True):
                            del_resp = conversations_client.delete_conversation(conv['id'])
                            if del_resp and del_resp.status_code == 200:
                                st.success("Supprimé")
                                st.rerun()
                            else:
                                st.error("Erreur")
    else:
        st.error("Impossible de récupérer les conversations.")
