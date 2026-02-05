import streamlit as st
from src.frontend.utils.session import logout

def render_profile():
    """
    Affiche la page de profil utilisateur.
    Design professionnel, épuré et cohérent avec la charte QHSE Air Bot.
    """
    
    # --- CSS Styles ---
    st.markdown("""
    <style>
        /* Profile Header Card */
        .profile-header-card {
            display: flex;
            align-items: center;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 2rem;
        }
        
        /* Avatar Circle */
        .profile-avatar {
            width: 80px;
            height: 80px;
            background: #e0f2f1; /* Teal 50 */
            color: #00695c;      /* Teal 800 */
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: 700;
            margin-right: 1.5rem;
            border: 2px solid #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* User Info Text */
        .profile-info h2 {
            margin: 0;
            color: #1e293b; /* Slate 800 */
            font-size: 1.5rem;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
        }
        
        .profile-info p {
            margin: 0.25rem 0 0 0;
            color: #64748b; /* Slate 500 */
            font-size: 0.95rem;
        }
        
        /* Section Headers inside Containers */
        .settings-header {
            font-size: 1.1rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }
        
        .settings-header svg {
            margin-right: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

    user = st.session_state.user or {}
    email = user.get("email", "utilisateur@exemple.com")
    
    # Calcul des initiales (Ex: 'admin@gmail.com' -> 'AD')
    raw_name = email.split("@")[0]
    initials = raw_name[:2].upper() if raw_name else "U"
    display_name = raw_name.replace(".", " ").replace("_", " ").title()

    # --- Header Section (Avatar + Name) ---
    st.markdown(f"""
    <div class="profile-header-card">
        <div class="profile-avatar">{initials}</div>
        <div class="profile-info">
            <h2>{display_name}</h2>
            <p>{email}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Main Content Grid ---
    # Centrage léger pour ne pas que ce soit trop large sur grand écran
    c_spacer_l, c_main, c_spacer_r = st.columns([1, 8, 1])
    
    with c_main:
        # 1. Section Informations & Sécurité
        with st.container(border=True):
            st.markdown('<div class="settings-header">🛡️ Informations & Sécurité</div>', unsafe_allow_html=True)
            
            # Email (Read-only)
            st.text_input("Identifiant (Email)", value=email, disabled=True, help="Votre identifiant unique.")
            
            st.markdown("###") # Spacer
            
            # Changement de mot de passe
            with st.expander("Modifier le mot de passe"):
                st.caption("Pour renforcer votre sécurité, choisissez un mot de passe fort.")
                with st.form("password_change_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.text_input("Nouveau mot de passe", type="password")
                    with c2:
                        st.text_input("Confirmer le mot de passe", type="password")
                    
                    submitted = st.form_submit_button("Mettre à jour le mot de passe", type="primary", use_container_width=True)
                    if submitted:
                        st.info("Cette fonctionnalité est en cours de déploiement.")

        st.markdown("###") # Vertical Space

        # 2. Section Préférences (Placeholder pour futur)
        # On garde le design "propre" donc on n'ajoute pas de faux contenu, 
        # mais on peut structurer la page.
        
        # 3. Zone de Danger / Déconnexion
        with st.container(border=True):
            st.markdown('<div class="settings-header" style="color: #ef4444;">🚪 Session</div>', unsafe_allow_html=True)
            
            col_desc, col_btn = st.columns([3, 1], vertical_alignment="center")
            
            with col_desc:
                st.write("Vous êtes connecté à votre espace personnel. N'oubliez pas de vous déconnecter.")
                
            with col_btn:
                if st.button("Se déconnecter", type="secondary", use_container_width=True):
                    logout()
