import streamlit as st
import requests
import httpx
from src.frontend.services import chat_client, conversations_client

def render_chat():
    # Header Section
    col_header, col_action = st.columns([3, 1])
    with col_header:
        st.markdown("## Mon Assistant ")
    
    # Gestion de la conversation active
    if not st.session_state.current_conversation_id:
        st.divider()
        # État vide : Centré et accueillant
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("""
<div style="text-align: center; margin-top: 2rem; margin-bottom: 2rem;">
    <h3 style="color: #546e7a;">Bonjour !</h3>
    <p style="color: #78909c;">Je suis prêt à vous aider sur vos questions.</p>
</div>
""", unsafe_allow_html=True)
            
            if st.button("Démarrer une nouvelle conversation", type="primary", use_container_width=True):
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
        # Conversation active
        
        # Récupérer les détails de la conversation (statut)
        conv_status = "active"
        resp = conversations_client.get_conversation(st.session_state.current_conversation_id)
        if resp and resp.status_code == 200:
            conv_data = resp.json()
            conv_status = conv_data.get("status", "active")

        with col_action:
            # Boutons d'action : Clôturer et Retour
            c_act1, c_act2 = st.columns(2)
            with c_act1:
                if conv_status != "clos":
                    if st.button("Clôturer", key="close_conv_btn", help="Marquer comme terminée", use_container_width=True):
                        conversations_client.update_conversation(st.session_state.current_conversation_id, status="clos")
                        st.toast("Conversation marquée comme close", icon="✅")
                        st.rerun()
                else:
                    st.markdown(f"<div style='text-align: center; color: #4CAF50; font-weight: bold; padding-top: 8px; border: 1px solid #4CAF50; border-radius: 4px;'>CLOS</div>", unsafe_allow_html=True)
            
            with c_act2:
                # Bouton de retour/fermeture aligné à droite du titre
                if st.button("Retour", type="secondary", use_container_width=True):
                    st.session_state.current_conversation_id = None
                    st.session_state.messages = []
                    st.rerun()
        
        st.divider()

        # Container principal du chat
        chat_container = st.container()
        
        # Affichage de l'historique
        # Si messages vides mais conv active, charger historique
        if not st.session_state.messages and st.session_state.current_conversation_id:
            hist_resp = conversations_client.get_conversation_history(st.session_state.current_conversation_id)
            if hist_resp and hist_resp.status_code == 200:
                msgs = hist_resp.json()
                for m in msgs:
                    role = "user" if m.get("sender") == "user" else "assistant"
                    st.session_state.messages.append({"role": role, "content": m.get("content")})
    
        with chat_container:
            if not st.session_state.messages:
                st.info("La conversation est vide. Posez votre première question !")
            
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            # --- Actions de bas de page (Navigation simplifiée pour longues conversations) ---
            if len(st.session_state.messages) > 2:
                st.markdown("---")
                c_end1, c_end2, c_end3 = st.columns([1, 2, 1])
                with c_end2:
                    cb1, cb2 = st.columns(2)
                    with cb1:
                        # Bouton Clôturer (si pas déjà clos)
                        if conv_status != "clos":
                            if st.button("🔒 Clôturer", key="close_conv_btn_bottom", help="Clôturer cette conversation", use_container_width=True):
                                conversations_client.update_conversation(st.session_state.current_conversation_id, status="clos")
                                st.toast("Conversation marquée comme close", icon="✅")
                                st.rerun()
                        else:
                            st.info("Conversation close")
                    
                    with cb2:
                        # Bouton Retour
                        if st.button("⬅️ Retour", key="return_btn_bottom", use_container_width=True):
                            st.session_state.current_conversation_id = None
                            st.session_state.messages = []
                            st.rerun()
                st.markdown("<br><br>", unsafe_allow_html=True) # Espace pour éviter que ce soit caché par le chat_input

    
        # Input utilisateur
        if conv_status == "clos":
            st.info("Cette conversation est close. Vous ne pouvez plus envoyer de messages.")
        elif prompt := st.chat_input("Posez votre question QHSE..."):
            # Afficher message user
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container: # Force scroll down via rerun usually, but here we append visually
                with st.chat_message("user"):
                    st.markdown(prompt)
    
                # Appel API
                with st.chat_message("assistant"):
                    with st.spinner("Réflexion en cours..."):
                        try:
                            resp = chat_client.send_chat_message(st.session_state.current_conversation_id, prompt)
                            if resp and resp.status_code == 200:
                                data = resp.json()
                                # Supporte ancien format ("answer") et nouveau format DB ("content")
                                answer = data.get("content") or data.get("answer") or data.get("response") or "Pas de réponse."
                                st.markdown(answer)
                                st.session_state.messages.append({"role": "assistant", "content": answer})
                            elif resp and resp.status_code == 503:
                                # Maintenance / Index en cours
                                try:
                                    maintenance_msg = resp.json().get("detail", "Maintenance en cours.")
                                except:
                                    maintenance_msg = "Maintenance en cours."
                                
                                st.warning(maintenance_msg, icon="⚠️")
                                st.session_state.messages.append({"role": "assistant", "content": maintenance_msg})
                            else:
                                if resp:
                                    try:
                                        err_detail = resp.json().get("detail", resp.text)
                                    except:
                                        err_detail = resp.text
                                    status_code = resp.status_code
                                else:
                                    err_detail = "Réponse vide"
                                    status_code = "N/A"
                                    
                                err_msg = f"Erreur serveur ({status_code}): {err_detail}"
                                st.error(err_msg)
                                st.session_state.messages.append({"role": "assistant", "content": err_msg})
                        except (requests.exceptions.Timeout, httpx.ReadTimeout):
                            err_msg = (
                                "⚠️ **Délai d'attente dépassé**\n\n"
                                "Le serveur met trop de temps à répondre (> 120s).\n"
                                "Cela peut arriver si :\n"
                                "- La question est très complexe\n"
                                "- Le serveur est surchargé\n"
                                "- Le modèle IA est en cours d'initialisation\n\n"
                                "👉 *Veuillez réessayer dans quelques instants ou reformuler votre question.*"
                            )
                            st.warning(err_msg, icon="⏳")
                            st.session_state.messages.append({"role": "assistant", "content": err_msg})
                        except requests.exceptions.RequestException as e:
                            if isinstance(e, requests.exceptions.ConnectionError):
                                err_msg = "🔌 **Erreur de connexion** : Impossible de joindre le serveur backend."
                            else:
                                err_msg = f"❌ Erreur réseau : {e}"
                            
                            st.error(err_msg)
                            st.session_state.messages.append({"role": "assistant", "content": err_msg})
                        except Exception as e:
                            err_msg = f"Erreur inattendue : {e}"
                            st.error(err_msg)
                            st.session_state.messages.append({"role": "assistant", "content": err_msg})
