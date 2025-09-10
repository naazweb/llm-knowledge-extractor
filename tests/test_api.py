import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app

client = TestClient(app)

class TestAnalyzeAPI:
    
    @patch('main.TextAnalyzer')
    def test_analyze_success(self, mock_analyzer):
        mock_instance = Mock()
        mock_instance.analyze.return_value = {
            "text": "Test text",
            "summary": "Test summary",
            "title": "Test Title",
            "topics": ["topic1", "topic2", "topic3"],
            "sentiment": "positive",
            "keywords": ["test", "sample", "word"]
        }
        mock_analyzer.return_value = mock_instance
        
        response = client.post("/analyze", json={"text": "Test text"})
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Test summary"
        assert data["topics"] == ["topic1", "topic2", "topic3"]
        assert data["sentiment"] == "positive"
    
    def test_analyze_empty_text(self):
        response = client.post("/analyze", json={"text": ""})
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_analyze_missing_text(self):
        response = client.post("/analyze", json={})
        
        assert response.status_code == 422
    
    @patch('main.TextAnalyzer')
    def test_analyze_service_failure(self, mock_analyzer):
        mock_instance = Mock()
        mock_instance.analyze.side_effect = RuntimeError("Analysis failed")
        mock_analyzer.return_value = mock_instance
        
        response = client.post("/analyze", json={"text": "Test text"})
        
        assert response.status_code == 500
        assert "failed" in response.json()["detail"].lower()