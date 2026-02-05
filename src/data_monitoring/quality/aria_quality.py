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
    
    # Échantillonnage pour réduire la taille du payload (évite erreur 413)
    # On garde 2000 lignes max pour l'analyse de qualité
    if len(df) > 2000:
        print(f"Dataset volumineux ({len(df)} lignes). Échantillonnage à 2000 lignes.")
        df = df.sample(n=2000, random_state=42)

    current_data = df

    # 3. Configuration du rapport Evidently
    report = Report(metrics=[
        DataSummaryPreset(),
    ])

    # 4. Exécution de l'analyse
    print("Analyse de la qualité des données ARIA en cours...")
    report_result = report.run(reference_data=None, current_data=current_data)

    # 5. Tentative d'envoi + sauvegarde locale en fallback
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, "aria_quality_report.html")
    try:
        # 6. Sauvegarde dans le Remote Workspace (Service Docker)
        # Utilisation de la variable d'environnement pour Docker (http://qhse_evidently_proxy)
        # Fallback sur localhost:8102 pour le dev local
        EVIDENTLY_SERVICE_URL = os.getenv("EVIDENTLY_SERVICE_URL", "http://localhost:8102")
        ws = RemoteWorkspace(EVIDENTLY_SERVICE_URL)
        project_name = "ARIA Monitoring"
        existing_projects = ws.search_project(project_name)
        if existing_projects:
            project = existing_projects[0]
        else:
            project = ws.create_project(project_name)
        ws.add_run(project.id, report_result)
        print(f"Rapport envoyé au service Evidently (Projet: '{project_name}') sur {EVIDENTLY_SERVICE_URL}")
    except Exception as e:
        # Fallback: sauvegarde locale si l'UI refuse le payload (413)
        report_result.save_html(report_path)
        print(f"UI Evidently a refusé le snapshot (raison: {e}). Rapport HTML sauvegardé: {report_path}")

if __name__ == "__main__":
    run_aria_quality()
