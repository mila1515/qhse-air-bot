import os
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
from evidently.ui.workspace import RemoteWorkspace

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "aria_cleaned.csv")
REPORT_DIR = os.path.join(BASE_DIR, "src", "data_monitoring", "reports")

def run_aria_drift():
    """
    Génère un rapport de dérive de données (Data Drift) pour les données ARIA (Accidents).
    Focus sur les changements de distribution des types d'accidents, localisations, etc.
    """
    # 1. Chargement des données
    if not os.path.exists(DATA_PATH):
        print(f"Erreur : Le fichier de données n'existe pas : {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Conversion des dates si nécessaire
    # Note: ARIA a souvent des dates incomplètes ou formats variés, mais ici on utilise le CSV nettoyé.
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date']) # On garde ce qui est datable pour le tri
        df.sort_values(by='date', inplace=True)

    # 2. Séparation Référence / Actuel
    split_index = int(len(df) * 0.5)
    reference_data = df.iloc[:split_index]
    current_data = df.iloc[split_index:]

    if len(reference_data) == 0 or len(current_data) == 0:
        print("Pas assez de données pour l'analyse de dérive ARIA.")
        return

    # 3. Configuration du rapport Evidently
    # Pour ARIA (données textuelles/catégorielles), le DataDriftPreset détecte auto les colonnes catégorielles.
    report = Report(metrics=[
        DataDriftPreset(),
    ])

    # 4. Exécution de l'analyse
    print("Analyse de la dérive ARIA en cours...")
    report_result = report.run(reference_data=reference_data, current_data=current_data)

    # 5. Sauvegarde du rapport
    # os.makedirs(REPORT_DIR, exist_ok=True)
    # report_path = os.path.join(REPORT_DIR, "aria_drift_report.html")
    # report_result.save_html(report_path)
    
    # print(f"Rapport de dérive ARIA généré avec succès : {report_path}")

    # 6. Sauvegarde dans le Remote Workspace (Service Docker)
    EVIDENTLY_SERVICE_URL = "http://localhost:8101"

    ws = RemoteWorkspace(EVIDENTLY_SERVICE_URL)
    project_name = "ARIA Monitoring"
    existing_projects = ws.search_project(project_name)
    if existing_projects:
        project = existing_projects[0]
    else:
        project = ws.create_project(project_name)
    
    ws.add_run(project.id, report_result)
    print(f"Rapport envoyé au service Evidently (Projet: '{project_name}') sur {EVIDENTLY_SERVICE_URL}")

if __name__ == "__main__":
    run_aria_drift()
