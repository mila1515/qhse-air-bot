from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.monitoring.logger import logger

class DocumentSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Découpe les documents en chunks."""
        try:
            chunks = self.splitter.split_documents(documents)
            logger.info(f"✂️  Documents découpés en {len(chunks)} chunks.")
            return chunks
        except Exception as e:
            logger.error(f"❌ Erreur lors du découpage : {e}")
            return []
