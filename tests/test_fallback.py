import unittest
from unittest.mock import MagicMock, patch
from src.rag.pipeline.rag_chain import RAGPipeline
from src.monitoring.metrics import RAG_FALLBACK_COUNT

class TestRAGFallback(unittest.TestCase):

    def setUp(self):
        # On mock l'initialisation pour ne pas charger les vrais modèles/DB
        with patch.object(RAGPipeline, 'initialize_chain'):
            self.rag = RAGPipeline()
            # On simule une initialisation manuelle des mocks
            self.rag.chain = MagicMock()
            self.rag.retriever = MagicMock()
            self.rag.combine_docs_chain = MagicMock()
            self.rag.fallback_docs_chain = MagicMock()
            self.rag.llm = MagicMock() # Pour éviter que reformulate_question ne tente d'init

    def test_fallback_mechanism_success(self):
        """Test que le fallback est activé quand le LLM principal échoue."""
        
        # 1. Configuration du scénario
        question = "Quelle est la procédure d'urgence ?"
        mock_docs = ["Doc 1", "Doc 2"]
        
        # Le retriever retourne des docs
        self.rag.retriever.invoke.return_value = mock_docs
        
        # Le LLM Principal lève une erreur (ex: OpenAI down)
        self.rag.combine_docs_chain.invoke.side_effect = Exception("OpenAI API Error 500")
        
        # Le LLM Fallback fonctionne (ex: DeepSeek ok)
        expected_response = "Réponse du fallback"
        self.rag.fallback_docs_chain.invoke.return_value = expected_response
        
        # 2. Exécution
        with patch('src.rag.pipeline.rag_chain.RAG_FALLBACK_COUNT') as mock_metric:
            response = self.rag.query(question)
            
            # 3. Vérifications
            # Le principal a été appelé
            self.rag.combine_docs_chain.invoke.assert_called_once()
            
            # Le fallback a été appelé
            self.rag.fallback_docs_chain.invoke.assert_called_once()
            
            # La métrique a été incrémentée
            mock_metric.inc.assert_called_once()
            
            # La réponse finale est celle du fallback
            self.assertEqual(response, expected_response)

    def test_no_fallback_configured(self):
        """Test le comportement quand le principal échoue et AUCUN fallback n'est configuré."""
        
        self.rag.fallback_docs_chain = None
        self.rag.combine_docs_chain.invoke.side_effect = Exception("OpenAI Error")
        self.rag.retriever.invoke.return_value = ["Doc"]
        
        # Doit retourner le message d'erreur générique (catché dans query)
        response = self.rag.query("Question")
        self.assertIn("Le système est actuellement en maintenance", response)

    def test_fallback_fails_too(self):
        """Test quand le principal ET le fallback échouent."""
        
        self.rag.combine_docs_chain.invoke.side_effect = Exception("Primary Error")
        self.rag.fallback_docs_chain.invoke.side_effect = Exception("Fallback Error")
        self.rag.retriever.invoke.return_value = ["Doc"]
        
        response = self.rag.query("Question")
        self.assertIn("Le système est actuellement en maintenance", response)

if __name__ == '__main__':
    unittest.main()
