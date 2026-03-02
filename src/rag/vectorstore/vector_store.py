import os
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.config import get_settings
from src.monitoring.logger import logger
from src.rag.embeddings.embedding_provider import get_embeddings

settings = get_settings()

class VectorStoreManager:
    def __init__(self):
        # Récupération automatique des embeddings et du mode (openai ou local)
        self.embeddings, self.mode = get_embeddings()
        
        # Le dossier de stockage dépend du mode pour éviter les conflits de dimension
        # Ex: data/vectorstore/openai/ ou data/vectorstore/local/
        self.vectorstore_base_dir = os.path.join(settings.DATA_DIR, "vectorstore")
        self.vectorstore_dir = os.path.join(self.vectorstore_base_dir, self.mode)
        self.index_name = "qhse_faiss_index"

    def create_vectorstore(self, chunks: List[Document]):
        """Crée l'index FAISS à partir des chunks et le sauvegarde localement (avec batching)."""
        import time

        if not chunks:
            logger.warning("⚠️ Aucun chunk à indexer.")
            return

        BATCH_SIZE = 50  # Réduit pour éviter le Rate Limit
        DELAY_SECONDS = 1 # Pause entre les batchs

        try:
            logger.info(f"🧠 Création du VectorStore (FAISS) en mode {self.mode.upper()}...")
            logger.info(f"📊 Total chunks: {len(chunks)}. Batch size: {BATCH_SIZE}")
            
            vectorstore = None
            total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE

            for i in range(0, len(chunks), BATCH_SIZE):
                batch = chunks[i:i + BATCH_SIZE]
                batch_num = (i // BATCH_SIZE) + 1
                
                logger.info(f"   - Traitement batch {batch_num}/{total_batches} ({len(batch)} chunks)...")
                
                try:
                    if vectorstore is None:
                        vectorstore = FAISS.from_documents(batch, self.embeddings)
                    else:
                        vectorstore.add_documents(batch)
                    
                    # Pause pour rate limit
                    time.sleep(DELAY_SECONDS)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erreur sur le batch {batch_num} (tentative de reprise): {e}")
                    time.sleep(5) # Attente plus longue en cas d'erreur
                    if vectorstore is None:
                        vectorstore = FAISS.from_documents(batch, self.embeddings)
                    else:
                        vectorstore.add_documents(batch)

            # Sauvegarde
            if vectorstore:
                if not os.path.exists(self.vectorstore_dir):
                    os.makedirs(self.vectorstore_dir)
                    
                vectorstore.save_local(self.vectorstore_dir, self.index_name)
                logger.info(f"💾 Index FAISS sauvegardé dans {self.vectorstore_dir}")
            else:
                logger.error("❌ Aucun vectorstore créé (tous les batchs ont échoué ?)")
            
        except Exception as e:
            logger.error(f"❌ Erreur création VectorStore : {e}")
            raise e

    def get_retriever(self, k: int = 3):
        """Charge l'index local et retourne un retriever."""
        try:
            index_path = os.path.join(self.vectorstore_dir, f"{self.index_name}.faiss")
            
            if not os.path.exists(index_path):
                error_msg = f"Index FAISS introuvable pour le mode {self.mode.upper()} dans {self.vectorstore_dir}."
                logger.error(f"❌ {error_msg}")
                logger.warning("💡 Conseil : Lancez l'ingestion (`python src/rag/main.py --ingest`) avec ce mode activé.")
                raise FileNotFoundError(error_msg)

            vectorstore = FAISS.load_local(
                self.vectorstore_dir, 
                self.embeddings, 
                self.index_name,
                allow_dangerous_deserialization=True  # Sûr car nous avons généré l'index nous-mêmes
            )
            return vectorstore.as_retriever(search_kwargs={"k": k})
            
        except Exception as e:
            logger.error(f"❌ Erreur chargement VectorStore : {e}")
            raise e
