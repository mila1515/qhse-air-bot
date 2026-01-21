import os
import pandas as pd
from evidently import Report
from evidently.presets import DataSummaryPreset
from evidently.ui.workspace import RemoteWorkspace

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "aria_cleaned.csv")
REPORT_DIR = os.path.join(BASE_DIR, "src", "data_monitoring", "reports")

def run_aria_quality():
    """
    Génère un rapport de qualité des données (Data Quality) pour ARIA.
    Vérifie la complétude des champs (ex: combien d'accidents ont une géolocalisation ?).
    """
    # 1. Chargement des données
    if not os.path.exists(DATA_PATH):
        print(f"Erreur : Le fichier de données n'existe pas : {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    current_data = df

    # 3. Configuration du rapport Evidently
    report = Report(metrics=[
        DataSummaryPreset(),
    ])

    # 4. Exécution de l'analyse
    print("Analyse de la qualité des données ARIA en cours...")
    report_result = report.run(reference_data=None, current_data=current_data)

    # 5. Sauvegarde du rapport
    # os.makedirs(REPORT_DIR, exist_ok=True)
    # report_path = os.path.join(REPORT_DIR, "aria_quality_report.html")
    # report_result.save_html(report_path)
    
    # print(f"Rapport de qualité ARIA généré avec succès : {report_path}")

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
    run_aria_quality()
