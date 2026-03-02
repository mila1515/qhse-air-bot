from src.rag.vectorstore.vector_store import VectorStoreManager

def get_retriever(k: int = 3):
    """
    Retourne le retriever configuré à partir du VectorStore.
    """
    manager = VectorStoreManager()
    return manager.get_retriever(k=k)
