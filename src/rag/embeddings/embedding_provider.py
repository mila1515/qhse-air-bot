import os
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from src.monitoring.logger import logger
from src.config import get_settings

settings = get_settings()

def get_embeddings():
    """
    Sélectionne automatiquement le modèle d'embeddings à utiliser.
    
    Logique de fallback :
    1. Tente d'utiliser OpenAIEmbeddings (text-embedding-3-small, économique).
    2. Si la clé API est absente ou invalide, bascule sur HuggingFaceEmbeddings (gratuit, local).
    
    Retourne :
        Une instance d'embeddings (OpenAIEmbeddings ou HuggingFaceEmbeddings).
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    forced_provider = os.getenv("RAG_EMBEDDING_PROVIDER", "").lower()

    if forced_provider != "local" and openai_api_key:
        try:
            logger.info("🔑 Clé OpenAI détectée. Tentative d'initialisation des Embeddings OpenAI (text-embedding-3-small)...")
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=openai_api_key
            )
            embeddings.embed_query("test") 
            
            logger.info("✅ Mode Embeddings : OPENAI (text-embedding-3-small)")
            return embeddings, "openai"
            
        except Exception as e:
            logger.warning(f"⚠️ Échec de l'initialisation OpenAI malgré la présence de la clé : {e}")
            logger.info("🔄 Basculement automatique vers le mode LOCAL.")
    else:
        logger.warning("🚫 Aucune clé OPENAI_API_KEY trouvée dans l'environnement.")
        logger.info("🔄 Basculement automatique vers le mode LOCAL.")

    try:
        logger.info("🤗 Initialisation des Embeddings Locaux (HuggingFace)...")
        logger.info("⚙️ Modèle : sentence-transformers/all-MiniLM-L6-v2")
        
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        logger.info("✅ Mode Embeddings : LOCAL (HuggingFace)")
        return embeddings, "local"
        
    except Exception as e:
        logger.critical(f"❌ Erreur critique : Impossible d'initialiser les embeddings locaux : {e}")
        raise e
