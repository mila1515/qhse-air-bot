import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from src.monitoring.logger import logger

class DocumentLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_documents(self) -> List[Document]:
        """Charge les documents (TXT, PDF) depuis le dossier data."""
        documents = []
        
        if not os.path.exists(self.data_dir):
            logger.warning(f"⚠️ Le dossier {self.data_dir} n'existe pas.")
            return []

        # 1. Chargement des fichiers texte (.txt)
        try:
            txt_loader = DirectoryLoader(
                self.data_dir,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"}
            )
            txt_docs = txt_loader.load()
            documents.extend(txt_docs)
            logger.info(f"📄 {len(txt_docs)} fichiers texte chargés.")
        except Exception as e:
            logger.error(f"❌ Erreur chargement TXT : {e}")

        # 2. Chargement des fichiers PDF (.pdf)
        try:
            pdf_loader = DirectoryLoader(
                self.data_dir,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader
            )
            pdf_docs = pdf_loader.load()
            documents.extend(pdf_docs)
            logger.info(f"📑 {len(pdf_docs)} fichiers PDF chargés.")
        except Exception as e:
            logger.error(f"❌ Erreur chargement PDF : {e}")

        logger.info(f"📚 Total documents chargés : {len(documents)}")
        return documents
