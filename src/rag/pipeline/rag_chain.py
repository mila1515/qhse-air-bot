import os
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from src.rag.loader.db_exporter import export_db_to_txt
from src.rag.loader.document_loader import DocumentLoader
from src.rag.splitter.text_splitter import DocumentSplitter
from src.rag.vectorstore.vector_store import VectorStoreManager
from src.rag.retriever.retriever import get_retriever
from src.rag.prompts.qhse_prompts import get_qhse_prompt
from src.monitoring.logger import logger

class RAGPipeline:
    def __init__(self):
        self.chain = None

    def ingest_data(self):
        """
        Exécute le pipeline d'ingestion complet :
        1. Export des données SQL -> Texte
        2. Chargement des fichiers (PDF, TXT)
        3. Découpage (Splitting)
        4. Indexation (VectorStore)
        """
        logger.info("🚀 Démarrage de l'ingestion des données RAG...")
        
        # 1. Export SQL
        export_db_to_txt()

        # 2. Chargement
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        loader = DocumentLoader(data_dir)
        docs = loader.load_documents()
        
        if not docs:
            logger.warning("⚠️ Aucun document trouvé. L'indexation est annulée.")
            return

        # 3. Découpage
        splitter = DocumentSplitter()
        chunks = splitter.split_documents(docs)

        # 4. Indexation
        manager = VectorStoreManager()
        manager.create_vectorstore(chunks)
        logger.info("✅ Ingestion terminée avec succès.")

    def initialize_chain(self):
        """Initialise la chaîne RAG (LLM + Retriever)."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("❌ OPENAI_API_KEY non trouvée dans les variables d'environnement.")
            raise ValueError("OPENAI_API_KEY requise pour le RAG.")

        logger.info("🔗 Initialisation du pipeline RAG...")
        
        # LLM
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        # Retriever
        retriever = get_retriever(k=4)
        
        # Prompt
        prompt = get_qhse_prompt()
        
        # Chains
        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        self.chain = create_retrieval_chain(retriever, combine_docs_chain)
        logger.info("✅ Pipeline RAG prêt.")

    def query(self, question: str) -> str:
        """Pose une question au RAG."""
        if not self.chain:
            self.initialize_chain()
        
        try:
            logger.info(f"❓ Question: {question}")
            response = self.chain.invoke({"input": question})
            answer = response["answer"]
            logger.info("💡 Réponse générée.")
            return answer
        except Exception as e:
            logger.error(f"❌ Erreur lors de la requête RAG : {e}")
            return "Désolé, une erreur est survenue lors du traitement de votre demande."

# Instance globale pour usage facile
rag_pipeline = RAGPipeline()
