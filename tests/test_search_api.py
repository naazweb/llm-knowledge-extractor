import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app

client = TestClient(app)

class TestSearchAPI:
    
    @patch('main.AnalysisRepository')
    @patch('main.get_db')
    def test_search_success(self, mock_get_db, mock_repo_class):
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        mock_repo = Mock()
        mock_repo.search_by_topic.return_value = []
        mock_repo_class.return_value = mock_repo
        
        response = client.get("/search?topic=test")
        
        assert response.status_code == 200
        assert response.json() == []
        mock_repo.search_by_topic.assert_called_once_with("test")
    
    def test_search_empty_topic(self):
        response = client.get("/search?topic=")
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_search_missing_topic(self):
        response = client.get("/search")
        
        assert response.status_code == 422