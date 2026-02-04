import streamlit as st
from src.frontend.services import notes_client

def render_notes():
    # Gestion de la vue détail (Si une note est sélectionnée)
    if "current_note" in st.session_state and st.session_state.current_note:
        note = st.session_state.current_note
        
        # Header avec bouton retour
        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("← Retour"):
                del st.session_state.current_note
                st.rerun()
        
        st.markdown(f"## {note.get('title') or 'Note sans titre'}")
        st.caption(f"Créé le {note.get('created_at', '')[:10]}")
        
        st.divider()
        
        # Contenu de la note
        st.markdown(note.get('content', ''))
        
        st.divider()
        
        # Actions sur la note
        if st.button("Supprimer cette note", type="primary", key="del_current_note"):
            notes_client.delete_note(note['id'])
            del st.session_state.current_note
            st.success("Note supprimée")
            st.rerun()
            
        return

    # Vue Liste (Par défaut)
    st.markdown("## Mes Notes Personnelles")
    
    # Init form key
    if "note_form_key" not in st.session_state:
        st.session_state.note_form_key = 0

    # Formulaire d'ajout
    with st.expander("Ajouter une nouvelle note", expanded=False):
        # On utilise une clé dynamique pour forcer le reset des widgets
        with st.form(key=f"add_note_form_{st.session_state.note_form_key}", clear_on_submit=True):
            new_title = st.text_input("Titre")
            new_content = st.text_area("Contenu")
            submitted = st.form_submit_button("Sauvegarder")
            
            if submitted:
                if new_content:
                    resp = notes_client.create_note(new_title, new_content)
                    if resp and resp.status_code in [200, 201]:
                        st.success("Note créée !")
                        # Incrémenter la clé pour réinitialiser le formulaire au prochain rendu
                        st.session_state.note_form_key += 1
                        st.rerun()
                    else:
                        st.error("Erreur lors de la création.")
                else:
                    st.warning("Contenu requis.")
    
    st.divider()
    
    # Liste des notes
    resp = notes_client.get_notes()
    if resp and resp.status_code == 200:
        notes = resp.json()
        if not notes:
            st.info("Aucune note enregistrée.")
        else:
            for note in notes:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([5, 2, 1], vertical_alignment="center")
                    with c1:
                        # Afficher Titre et Date seulement
                        created = note.get('created_at', '')[:10]
                        title = note.get('title') or "Sans titre"
                        
                        st.markdown(f"**{title}**")
                        st.caption(f"Date: {created}")
                        
                    with c2:
                        # Bouton Voir
                        if st.button("Voir note", key=f"view_{note['id']}", use_container_width=True):
                            st.session_state.current_note = note
                            st.rerun()
                            
                    with c3:
                        # Bouton Supprimer
                        if st.button("Suppr.", key=f"del_note_{note['id']}", help="Supprimer la note", use_container_width=True):
                            notes_client.delete_note(note['id'])
                            st.rerun()

    else:
        st.error("Impossible de charger les notes.")
