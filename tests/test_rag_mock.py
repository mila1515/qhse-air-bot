import unittest
from unittest.mock import MagicMock, patch
from src.rag.pipeline.rag_chain import rag_pipeline

class TestRAGMock(unittest.TestCase):
    
    @patch('src.rag.pipeline.rag_chain.RAGPipeline.initialize_chain')
    def test_query_mock_azure(self, mock_init):
        """
        Test unitaire simulant (MOCK) la réponse d'Azure OpenAI.
        Objectif : Vérifier la logique de l'application sans appeler l'API réelle (Coût = 0€, Latence = 0ms).
        """
        # 1. Préparation du MOCK
        # On empêche l'initialisation réelle
        mock_init.return_value = None
        
        # On injecte manuellement les composants mockés
        rag_pipeline.combine_docs_chain = MagicMock()
        rag_pipeline.retriever = MagicMock()
        rag_pipeline.llm = MagicMock() # Pour éviter l'erreur de reformulation si activée
        
        # Simulation du Retriever (renvoie une liste vide de documents)
        rag_pipeline.retriever.invoke.return_value = []
        
        # Simulation de la réponse de la chaîne (LLM)
        mock_response = {
            "answer": "Ceci est une réponse générée par un MOCK. Azure n'a pas été contacté.",
            "context": []
        }
        rag_pipeline.combine_docs_chain.invoke.return_value = mock_response
        
        # 2. Exécution
        question = "Quelle est la procédure d'urgence ?"
        response = rag_pipeline.query(question)
        
        # 3. Vérification
        self.assertEqual(response, "Ceci est une réponse générée par un MOCK. Azure n'a pas été contacté.")
        
        # On vérifie que le retriever a été appelé (preuve qu'on a cherché des docs)
        rag_pipeline.retriever.invoke.assert_called_once()
        
        # On vérifie que la chaîne a été appelée (preuve qu'on a généré une réponse)
        rag_pipeline.combine_docs_chain.invoke.assert_called_once()
        
        print("\n✅ Test MOCK réussi : Pas d'appel réseau vers Azure.")

    @patch('src.rag.pipeline.rag_chain.RAGPipeline.initialize_chain')
    def test_query_fallback_google(self, mock_init):
        """
        Test unitaire du mécanisme de FALLBACK (Azure -> Google).
        Objectif : Vérifier que si Azure plante, Google prend le relais.
        """
        # 1. Préparation du MOCK
        mock_init.return_value = None
        
        rag_pipeline.combine_docs_chain = MagicMock()
        rag_pipeline.fallback_docs_chain = MagicMock() # On simule la présence du fallback
        rag_pipeline.retriever = MagicMock()
        rag_pipeline.llm = MagicMock()
        
        # Retriever OK
        rag_pipeline.retriever.invoke.return_value = []
        
        # Azure PLANTE (Simulation d'erreur)
        rag_pipeline.combine_docs_chain.invoke.side_effect = Exception("Azure 503 Service Unavailable")
        
        # Google RÉUSSIT
        mock_fallback_response = {
            "answer": "Réponse sauvée par Google Gemini (Fallback).",
            "context": []
        }
        rag_pipeline.fallback_docs_chain.invoke.return_value = mock_fallback_response
        
        # 2. Exécution
        question = "Incident critique sur Azure ?"
        response = rag_pipeline.query(question)
        
        # 3. Vérification
        self.assertEqual(response, "Réponse sauvée par Google Gemini (Fallback).")
        
        # Vérifier qu'Azure a été tenté
        rag_pipeline.combine_docs_chain.invoke.assert_called_once()
        
        # Vérifier que Google a pris le relais
        rag_pipeline.fallback_docs_chain.invoke.assert_called_once()
        
        print("\n✅ Test FALLBACK réussi : Bascule Azure -> Google validée.")

if __name__ == '__main__':
    unittest.main()
