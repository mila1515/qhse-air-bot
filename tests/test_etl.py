import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.etl.collect import DataCollector

# On mock requests.get pour ne pas faire de vrais appels HTTP
@patch("src.etl.collect.requests.get")
def test_collect_code_travail_success(mock_get):
    """
    Teste la collecte CDTN avec un mock de réponse HTTP réussie.
    """
    # 1. Configuration du Mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Contenu HTML simulé simple pour que BeautifulSoup trouve un titre et du contenu
    mock_response.content = b"<html><h1>Titre Article</h1><div class='html'>Contenu de l'article R4222-1</div></html>"
    mock_get.return_value = mock_response

    # 2. Exécution
    collector = DataCollector()
    
    # Pour éviter d'attendre (time.sleep), on pourrait mocker time.sleep aussi, 
    # mais ici on teste surtout la logique.
    with patch("src.etl.collect.time.sleep", return_value=None):
        df = collector.collect_code_travail()
    
    # 3. Vérifications
    assert isinstance(df, pd.DataFrame)
    # Comme la liste des articles est longue dans le code, le mock répondra pour chaque appel.
    # On devrait donc avoir autant de lignes que d'articles cibles.
    # Mais vérifions juste que ce n'est pas vide.
    assert not df.empty
    assert "article_ref" in df.columns
    assert "titre" in df.columns
    assert "contenu" in df.columns
    assert df.iloc[0]["source"] == "CDTN (Scraping Web)"

@patch("src.etl.collect.requests.get")
def test_collect_inrs_success(mock_get):
    """
    Teste la collecte INRS avec un mock.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html><h1>Guide INRS Test</h1></html>"
    mock_get.return_value = mock_response

    collector = DataCollector()
    with patch("src.etl.collect.time.sleep", return_value=None):
        df = collector.collect_inrs()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "titre" in df.columns
    assert df.iloc[0]["source"] == "INRS"
