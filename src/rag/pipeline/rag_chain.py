import os
import time
from langchain_openai import AzureChatOpenAI
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
from src.monitoring.metrics import RAG_QUERY_LATENCY, RAG_FALLBACK_COUNT

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
        # Recharger les variables d'environnement au cas où elles auraient changé
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        google_api_key = os.getenv("GOOGLE_API_KEY")
        
        self.llm = None
        self.llm_fallback = None

        # 1. Initialisation Azure OpenAI (LLM Principal)
        if azure_api_key and azure_endpoint:
            try:
                logger.info("🔷 Initialisation LLM Principal : Azure OpenAI")
                self.llm = AzureChatOpenAI(
                    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4.1-mini"),
                    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
                    azure_endpoint=azure_endpoint,
                    api_key=azure_api_key,
                    temperature=0,
                    request_timeout=30, # Timeout standard avant bascule
                    max_retries=1 # On limite les retries car on a un fallback
                )
                logger.info("✅ LLM Principal (Azure) initialisé.")
            except Exception as e:
                logger.warning(f"⚠️ Erreur init Azure OpenAI : {e}")

        # 2. Initialisation Google Gemini (LLM Fallback)
        if google_api_key:
            try:
                logger.info("🔷 Initialisation LLM Fallback : Google Gemini")
                model_name = "gemini-pro"
                self.llm_fallback = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=google_api_key,
                    temperature=0
                )
                logger.info(f"✅ LLM Fallback (Google) initialisé.")
            except Exception as e:
                logger.warning(f"⚠️ Erreur init Google Gemini : {e}")
        
        # Si Azure a échoué mais Google est là, Google devient le principal par défaut
        if not self.llm and self.llm_fallback:
             logger.warning("⚠️ Azure indisponible au démarrage. Google Gemini devient le LLM principal.")
             self.llm = self.llm_fallback
             self.llm_fallback = None # Pas besoin de fallback si c'est déjà le principal

        if not self.llm:
            logger.error("❌ Aucune configuration LLM valide (Google ou Azure) trouvée.")
            raise ValueError("Configuration LLM manquante.")

        logger.info("🔗 Initialisation du pipeline RAG...")
        
        # Retriever
        self.retriever = get_retriever(k=4)
        
        # Prompt
        prompt = get_qhse_prompt()
        summary_prompt = get_summary_prompt()
        
        # Chains
        # Chaîne Principale (Azure par défaut)
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        
        # Chaîne de Fallback (Google) - Uniquement si un fallback existe
        if self.llm_fallback:
             self.fallback_docs_chain = create_stuff_documents_chain(self.llm_fallback, prompt)
             logger.info("🛡️  Circuit de secours (Fallback Chain) activé.")
        
        self.summary_chain = create_stuff_documents_chain(self.llm, summary_prompt)
        
        # On garde quand même self.chain pour rétrocompatibilité
        self.chain = create_retrieval_chain(self.retriever, self.combine_docs_chain)
        logger.info("✅ Pipeline RAG prêt.")

    def reformulate_question(self, question: str) -> str:
        """Reformule la question utilisateur pour optimiser la recherche vectorielle."""
        if not self.llm:
            self.initialize_chain()
            
        try:
            reformulation_prompt = get_reformulation_prompt()
            formatted_prompt = reformulation_prompt.format(input=question)
            response = self.llm.invoke(formatted_prompt)
            reformulated = response.content.strip()
            logger.info(f"🔄 Reformulation : '{question}' -> '{reformulated}'")
            return reformulated
        except Exception as e:
            logger.warning(f"⚠️ Échec de la reformulation : {e}. Utilisation de la question originale.")
            return question

    def query(self, question: str) -> str:
        """Pose une question au RAG avec étape de reformulation obligatoire et détection d'intention (Résumé vs Question)."""
        start_time = time.time()
        
        if not self.chain:
            self.initialize_chain()
        
        try:
            logger.info(f"❓ Question originale : {question}")
            
            # Détection d'intention simple (avant reformulation pour ne pas perdre l'intention)
            summary_keywords = ["résume", "resume", "synthèse", "synthese", "resumer", "résumer", "synthetiser", "synthétiser", "summary", "summarize"]
            is_summary = any(keyword in question.lower() for keyword in summary_keywords)
            
            # 1. Reformulation (Réactivée)
            reformulated_question = self.reformulate_question(question)
            
            # 2. Récupération des documents (Retrieval) avec la question REFORMULÉE
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
                
                try:
                    # Tentative 1 : Chaîne Principale (Azure)
                    response = self.combine_docs_chain.invoke({
                        "input": question,  # Question originale pour la réponse
                        "context": docs
                    })
                except Exception as e_main:
                    # Si erreur et si un fallback existe
                    if self.fallback_docs_chain:
                        logger.warning(f"⚠️ Échec du LLM Principal ({e_main}). Bascule sur le Fallback (Google)...")
                        RAG_FALLBACK_COUNT.inc() # Incrément de la métrique
                        response = self.fallback_docs_chain.invoke({
                            "input": question,
                            "context": docs
                        })
                        logger.info("✅ Réponse générée par le Fallback (Google).")
                    else:
                        # Pas de fallback, on remonte l'erreur
                        raise e_main
            
            # Gestion du format de réponse
            answer = response
            if isinstance(response, dict) and "answer" in response:
                answer = response["answer"]
            elif hasattr(response, "content"):
                answer = response.content
                
            return answer

        except Exception as e:
            logger.error(f"❌ Erreur RAG : {e}")
            return f"Je suis désolé, une erreur est survenue lors du traitement de votre demande : {str(e)}"
        
        finally:
            # Enregistrement de la latence
            latency = time.time() - start_time
            RAG_QUERY_LATENCY.set(latency)
            logger.info(f"⏱️ Temps de réponse RAG : {latency:.2f}s")

# Instance globale pour usage facile
rag_pipeline = RAGPipeline()
