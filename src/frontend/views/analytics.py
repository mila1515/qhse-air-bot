import streamlit as st
import pandas as pd
from sqlalchemy import func
from src.db.session import SessionLocal
from src.db.models import MesureWAQI

# Chargement des données depuis PostgreSQL
@st.cache_data(ttl=600)
def load_data():
    db = SessionLocal()
    try:
        # Récupération de toutes les mesures WAQI
        query = db.query(MesureWAQI).all()
        data = []
        for m in query:
            data.append({
                "Date": m.date_collecte,
                "Ville": m.ville,
                "Station": m.station,
                "AQI": m.aqi,
                "Risque": m.niveau_risque,
                "PM2.5": m.pm25,
                "PM10": m.pm10,
                "NO2": m.no2,
                "O3": m.o3
            })
        
        df = pd.DataFrame(data)
        if not df.empty:
            # Conversion en datetime si nécessaire
            df['Date'] = pd.to_datetime(df['Date'])
            # Suppression du timezone pour éviter des conflits avec streamlit charts
            if df['Date'].dt.tz is not None:
                df['Date'] = df['Date'].dt.tz_localize(None)
        return df
    except Exception as e:
        st.error(f"Erreur lors de la connexion à la base de données : {e}")
        return pd.DataFrame()
    finally:
        db.close()

def render_analytics():
    """
    Rendu de la vue analytique intégrée.
    """
    # Header de la vue
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="color: #1e293b; font-weight: 800; font-size: 2.25rem; margin-bottom: 0.5rem;">
                📊 Dashboard Analytique
            </h1>
            <p style="color: #64748b; font-size: 1.1rem;">
                Analyse de la qualité de l'air et des indicateurs QHSE.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Chargement des données
    df = load_data()

    if df.empty:
        st.warning("⚠️ Aucune donnée n'a été trouvée dans la base de données.")
        st.info("💡 Lancez vos scripts d'extraction (ETL) pour peupler la base de données PostgreSQL.")
        return

    # --- Barre de filtres (Horizontale en haut de la vue) ---
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        villes = ["Toutes"] + sorted(df['Ville'].unique().tolist())
        ville_selected = st.selectbox("📍 Sélectionner une ville", villes)
    
    with col_f2:
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        date_range = st.date_input(
            "📅 Période de temps",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Application des filtres
    filtered_df = df.copy()
    
    if ville_selected != "Toutes":
        filtered_df = filtered_df[filtered_df['Ville'] == ville_selected]
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) & 
            (filtered_df['Date'].dt.date <= end_date)
        ]

    # --- Section 1: KPI Principaux ---
    st.markdown("### 📈 Indicateurs Clés")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        avg_aqi = filtered_df['AQI'].mean()
        st.metric("AQI Moyen", f"{avg_aqi:.1f}")
        
    with kpi2:
        avg_pm25 = filtered_df['PM2.5'].mean()
        st.metric("PM2.5 Moyen", f"{avg_pm25:.1f} µg/m³")
        
    with kpi3:
        if not filtered_df.empty:
            top_risk = filtered_df['Risque'].mode()[0]
            st.metric("Risque Prédominant", top_risk)
        else:
            st.metric("Risque Prédominant", "N/A")
            
    with kpi4:
        st.metric("Total Mesures", len(filtered_df))

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Section 2: Visualisations ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 📈 Évolution de l'AQI")
        if not filtered_df.empty:
            time_df = filtered_df.sort_values('Date').set_index('Date')[['AQI']]
            st.line_chart(time_df, color="#48BB78")
        else:
            st.info("Sélectionnez une période valide.")

    with col_right:
        st.markdown("#### 🧪 Comparaison des Polluants")
        if not filtered_df.empty:
            pollutants = ['PM2.5', 'PM10', 'NO2', 'O3']
            pollutant_avg = filtered_df[pollutants].mean()
            st.bar_chart(pollutant_avg, color="#3182CE")
        else:
            st.info("Données insuffisantes.")

    # --- Section 3: Détails par Risque ---
    st.markdown("#### ⚠️ Répartition par Niveau de Risque")
    if not filtered_df.empty:
        risk_dist = filtered_df['Risque'].value_counts()
        st.bar_chart(risk_dist, color="#E53E3E")

    # --- Section 4: Tableau de données ---
    with st.expander("📋 Consulter les données détaillées"):
        st.dataframe(
            filtered_df.sort_values('Date', ascending=False),
            use_container_width=True
        )
