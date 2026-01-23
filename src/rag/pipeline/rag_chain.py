import os
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from src.rag.loader.db_exporter import export_db_to_txt
from src.rag.loader.document_loader import DocumentLoader
from src.rag.splitter.text_splitter import DocumentSplitter
from src.rag.vectorstore.vector_store import VectorStoreManager
from src.rag.retriever.retriever import get_retriever
from src.rag.prompts.qhse_prompts import get_qhse_prompt
from src.rag.prompts.reformulation_prompt import get_reformulation_prompt
from src.rag.prompts.summary_prompt import get_summary_prompt
from src.monitoring.logger import logger

class RAGPipeline:
    def __init__(self):
        self.chain = None
        self.llm = None
        self.retriever = None
        self.combine_docs_chain = None
        self.summary_chain = None

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
        openai_api_key = os.getenv("OPENAI_API_KEY")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        google_api_key = os.getenv("GOOGLE_API_KEY")
        
        self.llm = None

        # 1. Tentative Google Gemini (Priorité si configuré)
        if google_api_key:
            try:
                logger.info("🔷 Initialisation LLM : Google Gemini")
                # On utilise gemini-flash-latest qui est confirmé comme fonctionnel
                model_name = "gemini-flash-latest"
                self.llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=google_api_key,
                    temperature=0
                )
                logger.info(f"✅ LLM Gemini initialisé avec succès ({model_name})")
            except Exception as e:
                logger.warning(f"⚠️ Erreur Google Gemini LLM : {e}")

        # 2. Tentative Azure OpenAI
        if not self.llm and azure_api_key and azure_endpoint:
            try:
                logger.info("🔷 Initialisation LLM : Azure OpenAI")
                self.llm = AzureChatOpenAI(
                    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-35-turbo"),
                    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
                    azure_endpoint=azure_endpoint,
                    api_key=azure_api_key,
                    temperature=0
                )
            except Exception as e:
                logger.warning(f"⚠️ Erreur Azure OpenAI LLM : {e}")

        # 3. Tentative OpenAI Standard
        if not self.llm and openai_api_key:
            logger.info("🟢 Initialisation LLM : OpenAI Standard (gpt-4o-mini)")
            # gpt-4o-mini est le modèle le plus économique et performant actuellement
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)
            
        if not self.llm:
            logger.error("❌ Aucune configuration LLM valide (Google, OpenAI ou Azure) trouvée.")
            # On ne lève pas d'erreur bloquante ici pour permettre le chargement du module, 
            # mais la méthode query échouera.
            raise ValueError("Configuration LLM manquante. Veuillez configurer GOOGLE_API_KEY, OPENAI_API_KEY ou les variables AZURE_OPENAI_...")

        logger.info("🔗 Initialisation du pipeline RAG...")
        
        # Retriever
        self.retriever = get_retriever(k=4)
        
        # Prompt
        prompt = get_qhse_prompt()
        summary_prompt = get_summary_prompt()
        
        # Chains
        # On garde les composants séparés pour pouvoir orchestrer manuellement (Reformulation -> Retrieval -> Answer)
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        self.summary_chain = create_stuff_documents_chain(self.llm, summary_prompt)
        
        # On garde quand même self.chain pour rétrocompatibilité si besoin, mais on va surtout utiliser les composants
        self.chain = create_retrieval_chain(self.retriever, self.combine_docs_chain)
        logger.info("✅ Pipeline RAG prêt.")

    def reformulate_question(self, question: str) -> str:
        """Reformule la question utilisateur pour optimiser la recherche vectorielle."""
        if not self.llm:
            self.initialize_chain()
            
        try:
            reformulation_prompt = get_reformulation_prompt()
            # Création d'une mini-chaîne pour la reformulation
            # invoke retourne un objet AIMessage, on veut le content
            messages = reformulation_prompt.format_messages(input=question)
            response = self.llm.invoke(messages)
            reformulated = response.content.strip()
            logger.info(f"🔄 Reformulation : '{question}' -> '{reformulated}'")
            return reformulated
        except Exception as e:
            logger.warning(f"⚠️ Échec de la reformulation : {e}. Utilisation de la question originale.")
            return question

    def query(self, question: str) -> str:
        """Pose une question au RAG avec étape de reformulation obligatoire et détection d'intention (Résumé vs Question)."""
        if not self.chain:
            self.initialize_chain()
        
        try:
            logger.info(f"❓ Question originale : {question}")
            
            # Détection d'intention simple (avant reformulation pour ne pas perdre l'intention)
            summary_keywords = ["résume", "resume", "synthèse", "synthese", "resumer", "résumer", "synthetiser", "synthétiser", "summary", "summarize"]
            is_summary = any(keyword in question.lower() for keyword in summary_keywords)
            
            # 1. Reformulation (toujours appliquée selon demande utilisateur)
            reformulated_question = self.reformulate_question(question)
            
            # 2. Récupération des documents (Retrieval) avec la question reformulée
            logger.info(f"🔍 Recherche vectorielle avec : '{reformulated_question}'")
            docs = self.retriever.invoke(reformulated_question)
            
            # 3. Sélection du prompt et génération
            if is_summary:
                logger.info("📝 Mode détecté : RÉSUMÉ (Summary Prompt)")
                # Le prompt de résumé ne prend que {context}
                response = self.summary_chain.invoke({
                    "context": docs
                })
            else:
                logger.info("📝 Mode détecté : QUESTION/RÉPONSE STANDARD (QHSE Prompt)")
                # Le prompt QHSE prend {input} et {context}
                response = self.combine_docs_chain.invoke({
                    "input": question,  # Question originale pour la réponse
                    "context": docs
                })
            
            # Gestion du format de réponse
            answer = response
            if isinstance(response, dict) and "answer" in response:
                 answer = response["answer"]
            
            logger.info("💡 Réponse générée.")
            return answer
        except Exception as e:
            logger.error(f"❌ Erreur lors de la requête RAG : {e}")
            return "Désolé, une erreur est survenue lors du traitement de votre demande."

# Instance globale pour usage facile
rag_pipeline = RAGPipeline()
