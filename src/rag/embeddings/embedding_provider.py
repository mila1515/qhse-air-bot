import os
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from src.monitoring.logger import logger
from src.config import get_settings

settings = get_settings()

def get_embeddings():
    """
    Sélectionne automatiquement le modèle d'embeddings à utiliser.
    
    Logique de fallback :
    1. Tente d'utiliser Azure OpenAI (si configuré).
    2. Tente d'utiliser OpenAIEmbeddings (payant, meilleure qualité).
    3. Si la clé API est absente ou invalide, bascule sur HuggingFaceEmbeddings (gratuit, local).
    
    Retourne :
        Une instance d'embeddings (AzureOpenAIEmbeddings, OpenAIEmbeddings ou HuggingFaceEmbeddings).
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Configuration Azure (Priorité aux variables spécifiques Embeddings)
    azure_api_key = os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
    
    forced_provider = os.getenv("RAG_EMBEDDING_PROVIDER", "").lower()

    # 1. Tentative Azure OpenAI
    if forced_provider != "local" and azure_api_key and azure_endpoint:
        try:
            logger.info("🔷 Configuration Azure OpenAI détectée. Initialisation des Embeddings Azure...")
            embeddings = AzureOpenAIEmbeddings(
                azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"),
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key
            )
            # Validation rapide
            embeddings.embed_query("test")
            logger.info("✅ Mode Embeddings : AZURE OPENAI")
            return embeddings, "azure"
        except Exception as e:
            logger.warning(f"⚠️ Échec de l'initialisation Azure OpenAI : {e}")
    else:
        logger.info("ℹ️ Configuration Azure OpenAI incomplète ou absente (API_KEY ou ENDPOINT manquants). Passage à OpenAI Standard.")


    # 2. Tentative OpenAI Standard
    if forced_provider != "local" and openai_api_key:
        try:
            logger.info("🔑 Clé OpenAI détectée. Tentative d'initialisation des Embeddings OpenAI...")
            # On initialise le modèle. Note: Cela ne valide pas la clé instantanément,
            # mais c'est l'intention qui compte ici. L'erreur surviendra à l'utilisation si la clé est mauvaise.
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-large",
                api_key=openai_api_key
            )
            # Validation de la clé avec une requête légère
            embeddings.embed_query("test") 
            
            logger.info("✅ Mode Embeddings : OPENAI (text-embedding-3-large)")
            return embeddings, "openai"
            
        except Exception as e:
            logger.warning(f"⚠️ Échec de l'initialisation OpenAI malgré la présence de la clé : {e}")
            logger.info("🔄 Basculement automatique vers le mode LOCAL.")
    else:
        logger.warning("🚫 Aucune clé OPENAI_API_KEY trouvée dans l'environnement.")
        logger.info("🔄 Basculement automatique vers le mode LOCAL.")

    # 2. Fallback Local (HuggingFace)
    try:
        logger.info("🤗 Initialisation des Embeddings Locaux (HuggingFace)...")
        logger.info("⚙️ Modèle : sentence-transformers/all-MiniLM-L6-v2")
        
        # Ce modèle est léger (~80MB), rapide et performant pour la sémantique
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        logger.info("✅ Mode Embeddings : LOCAL (HuggingFace)")
        return embeddings, "local"
        
    except Exception as e:
        logger.critical(f"❌ Erreur critique : Impossible d'initialiser les embeddings locaux : {e}")
        raise e
