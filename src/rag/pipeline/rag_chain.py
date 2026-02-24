import os
import time
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.documents import Document
from src.db.session import SessionLocal
from src.db.models import MesureWAQI
from src.rag.loader.db_exporter import format_waqi
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
        self.fallback_docs_chain = None
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
        load_dotenv() # Ne pas utiliser override=True pour ne pas écraser les variables CI/CD
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        
        self.llm = None
        self.llm_fallback = None
        
        if openai_api_key:
            try:
                logger.info("🔷 Initialisation LLM Principal : OpenAI Standard")
                self.llm = ChatOpenAI(
                    model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
                    api_key=openai_api_key,
                    temperature=0
                )
                logger.info("✅ LLM Principal (OpenAI Standard) initialisé.")
            except Exception as e:
                logger.warning(f"⚠️ Erreur init OpenAI Standard : {e}")
        
        if not self.llm and deepseek_api_key:
            try:
                logger.info("🔷 Initialisation LLM Secondaire : DeepSeek (via OpenAI API)")
                self.llm = ChatOpenAI(
                    model=os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat"),
                    api_key=deepseek_api_key,
                    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
                    temperature=0
                )
                logger.info("✅ LLM Secondaire (DeepSeek) initialisé.")
            except Exception as e:
                logger.warning(f"⚠️ Erreur init DeepSeek : {e}")
        
        if not self.llm:
            logger.error("❌ Aucune configuration LLM valide (OpenAI ou DeepSeek) trouvée.")
            raise ValueError("Configuration LLM manquante.")

        logger.info("🔗 Initialisation du pipeline RAG...")
        
        # Retriever
        # Optimisation : k=3 pour réduire le contexte et accélérer la génération
        self.retriever = get_retriever(k=3)
        
        # Prompt
        prompt = get_qhse_prompt()
        summary_prompt = get_summary_prompt()
        
        # Chains
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        
        self.summary_chain = create_stuff_documents_chain(self.llm, summary_prompt)
        
        # On garde quand même self.chain pour rétrocompatibilité
        self.chain = create_retrieval_chain(self.retriever, self.combine_docs_chain)
        logger.info("✅ Pipeline RAG prêt.")

    def _get_realtime_waqi_doc(self, question: str):
        """Récupère les données WAQI temps réel si la question concerne la qualité de l'air."""
        question_lower = question.lower()
        keywords = ["qualité de l'air", "pollution", "waqi", "aqi", "air quality", "indice", "air"]
        
        if not any(k in question_lower for k in keywords):
            return None
            
        db = SessionLocal()
        try:
            # Chercher si une ville connue est mentionnée
            cities = db.query(MesureWAQI.ville).distinct().all()
            found_city = None
            
            # Priorité aux villes exactes
            for (city_name,) in cities:
                if city_name.lower() in question_lower:
                    found_city = city_name
                    break
            
            if found_city:
                measure = db.query(MesureWAQI).filter(MesureWAQI.ville == found_city).order_by(MesureWAQI.date_collecte.desc()).first()
                if measure:
                    # On force l'injection en haut de liste
                    content = f"--- 🚨 DONNÉES TEMPS RÉEL (Date: {measure.date_collecte}) ---\n" + format_waqi(measure)
                    logger.info(f"⚡ Injection donnée temps réel pour {found_city}")
                    return Document(page_content=content, metadata={"source": "realtime_db"})
                    
        except Exception as e:
            logger.error(f"Erreur lors de la récupération WAQI temps réel : {e}")
        finally:
            db.close()
            
        return None

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
            
            # 1. Reformulation (Désactivée pour performance DeepSeek)
            # Le modèle DeepSeek est assez intelligent pour comprendre sans reformulation
            # 1. Reformulation (Désactivée pour performance)
            # reformulated_question = self.reformulate_question(question)
            reformulated_question = question # On utilise la question directe
            
            # 2. Récupération des documents (Retrieval) avec la question ORIGINALE
            logger.info(f"🔍 Recherche vectorielle avec : '{reformulated_question}'")
            docs = self.retriever.invoke(reformulated_question)
            
            # --- AJOUT: Injection de données temps réel ---
            realtime_doc = self._get_realtime_waqi_doc(question)
            if realtime_doc:
                logger.info(f"⚡ Donnée temps réel injectée en priorité")
                docs.insert(0, realtime_doc)
            # ----------------------------------------------
            
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
                    # Chaîne Principale (DeepSeek/OpenAI)
                    response = self.combine_docs_chain.invoke({
                        "input": question,  # Question originale pour la réponse
                        "context": docs
                    })
                except Exception as e_main:
                    logger.error(f"❌ Erreur du LLM Principal : {e_main}")
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
            return "⚠️ Le système est actuellement en maintenance ou rencontre une surcharge temporaire. Veuillez réessayer plus tard."
        
        finally:
            # Enregistrement de la latence
            latency = time.time() - start_time
            RAG_QUERY_LATENCY.set(latency)
            logger.info(f"⏱️ Temps de réponse RAG : {latency:.2f}s")

# Instance globale pour usage facile
rag_pipeline = RAGPipeline()
