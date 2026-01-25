import streamlit as st
from src.frontend.services import notes_client

def render_notes():
    st.title("📝 Mes Notes Personnelles")
    
    # Formulaire d'ajout
    with st.expander("➕ Ajouter une nouvelle note", expanded=False):
        with st.form("add_note_form"):
            # new_title = st.text_input("Titre") # Titre supprimé du modèle pour l'instant
            new_content = st.text_area("Contenu")
            submitted = st.form_submit_button("Sauvegarder")
            if submitted:
                if new_content:
                    resp = notes_client.create_note(new_content)
                    if resp and resp.status_code in [200, 201]:
                        st.success("Note créée !")
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
                    c1, c2 = st.columns([6, 1], vertical_alignment="center")
                    with c1:
                        # Afficher un extrait ou la date
                        created = note.get('created_at', '')[:10]
                        excerpt = (note.get('content') or '')
                        # Si le contenu est long, on coupe
                        if len(excerpt) > 100:
                            excerpt = excerpt[:100] + "..."
                        
                        st.write(f"**{created}**")
                        st.write(excerpt)
                        
                    with c2:
                        if st.button("🗑️", key=f"del_note_{note['id']}", help="Supprimer la note", use_container_width=True):
                            notes_client.delete_note(note['id'])
                            st.rerun()
                    
                    # Mode édition (Lecture seule pour l'instant)
                    with st.expander("Voir le détail"):
                        st.info(note.get("content"))

    else:
        st.error("Impossible de charger les notes.")
