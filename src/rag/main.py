import argparse
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

# Ajout du chemin racine pour les imports absolus
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.rag.pipeline.rag_chain import rag_pipeline
from src.monitoring.logger import logger

def main():
    parser = argparse.ArgumentParser(description="CLI RAG QHSE Air Bot")
    parser.add_argument("--ingest", action="store_true", help="Lancer l'ingestion des documents (DB + Fichiers)")
    parser.add_argument("--query", type=str, help="Poser une question au RAG")
    
    args = parser.parse_args()
    
    if args.ingest:
        try:
            rag_pipeline.ingest_data()
        except Exception as e:
            logger.error(f"Erreur d'ingestion : {e}")
        
    if args.query:
        try:
            print(f"\n💬 Question : {args.query}")
            answer = rag_pipeline.query(args.query)
            print("\n🤖 Réponse de l'assistant QHSE :\n")
            print(answer)
            print("\n" + "-"*50 + "\n")
        except Exception as e:
            logger.error(f"Erreur de requête : {e}")

if __name__ == "__main__":
    main()
