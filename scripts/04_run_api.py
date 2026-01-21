"""
Script de lancement de l'API (ETL - Step 4: Run API)
Utilise uvicorn pour servir l'application FastAPI
"""

import uvicorn
import sys
from pathlib import Path

# Ajout du dossier racine au path pour les imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

if __name__ == "__main__":
    print("🚀 Démarrage de l'API QHSE Air Bot...")
    print("📚 Documentation disponible sur http://localhost:8000/docs")
    print("📊 Métriques disponibles sur http://localhost:8000/metrics")
    
    # Lancement du serveur
    # reload=True permet le redémarrage automatique si le code change (dev mode)
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
