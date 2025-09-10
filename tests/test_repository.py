import pytest
from unittest.mock import Mock
from src.repository import AnalysisRepository

class TestAnalysisRepository:
    
    def test_save_analysis(self):
        mock_db = Mock()
        repo = AnalysisRepository(mock_db)
        
        analysis_data = {
            "text": "Test text",
            "summary": "Test summary",
            "title": "Test Title",
            "topics": ["topic1", "topic2"],
            "sentiment": "positive",
            "keywords": ["test", "word"]
        }
        
        result = repo.save(analysis_data)
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_search_by_topic(self):
        mock_db = Mock()
        repo = AnalysisRepository(mock_db)
        
        repo.search_by_topic("test")
        
        mock_db.query.assert_called_once()
        mock_db.query().filter.assert_called_once()
        mock_db.query().filter().all.assert_called_once()