import os
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "waqi_cleaned.csv")
REPORT_DIR = os.path.join(BASE_DIR, "src", "data_monitoring", "reports")

def run_waqi_drift():
    """
    Génère un rapport de dérive de données (Data Drift) pour les données WAQI.
    Compare la première moitié des données (référence) avec la seconde moitié (actuelle).
    """
    # 1. Chargement des données
    if not os.path.exists(DATA_PATH):
        print(f"Erreur : Le fichier de données n'existe pas : {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Conversion des dates
    if 'date_collecte' in df.columns:
        df['date_collecte'] = pd.to_datetime(df['date_collecte'])
    
    df.sort_values(by='date_collecte', inplace=True)

    # 2. Séparation Référence / Actuel (Simulation)
    # Dans un cas réel, "reference" serait un dataset validé statique, et "current" le dernier batch.
    # Ici, on coupe le dataset en deux.
    split_index = int(len(df) * 0.5)
    reference_data = df.iloc[:split_index]
    current_data = df.iloc[split_index:]

    if len(reference_data) == 0 or len(current_data) == 0:
        print("Pas assez de données pour l'analyse de dérive.")
        return

    # 3. Configuration du rapport Evidently
    report = Report(metrics=[
        DataDriftPreset(),
    ])

    # 4. Exécution de l'analyse
    print("Analyse de la dérive WAQI en cours...")
    report_result = report.run(reference_data=reference_data, current_data=current_data)

    # 5. Sauvegarde du rapport
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, "waqi_drift_report.html")
    report_result.save_html(report_path)
    
    print(f"Rapport de dérive WAQI généré avec succès : {report_path}")

if __name__ == "__main__":
    run_waqi_drift()
