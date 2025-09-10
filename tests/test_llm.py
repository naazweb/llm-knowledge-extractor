import pytest
from unittest.mock import Mock, patch
from src.services.llm import LLMService

class TestLLMService:
    
    @patch('src.services.llm.ChatOpenAI')
    def test_analyze_text_success(self, mock_chat_openai):
        # Mock LangChain response
        mock_response = Mock()
        mock_response.content = '{"summary": "Test summary", "title": "Test Title", "topics": ["topic1", "topic2", "topic3"], "sentiment": "positive"}'
        
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_openai.return_value = mock_llm_instance
        
        service = LLMService()
        result = service.analyze_text("Test text")
        
        assert result["summary"] == "Test summary"
        assert result["title"] == "Test Title"
        assert result["topics"] == ["topic1", "topic2", "topic3"]
        assert result["sentiment"] == "positive"
    
    @patch('src.services.llm.ChatOpenAI')
    def test_analyze_text_api_failure(self, mock_chat_openai):
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.side_effect = Exception("API Error")
        mock_chat_openai.return_value = mock_llm_instance
        
        service = LLMService()
        
        with pytest.raises(RuntimeError, match="LLM API call failed"):
            service.analyze_text("Test text")
    
    @patch('src.services.llm.ChatOpenAI')
    def test_analyze_text_invalid_json(self, mock_chat_openai):
        mock_response = Mock()
        mock_response.content = 'invalid json'
        
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_openai.return_value = mock_llm_instance
        
        service = LLMService()
        
        with pytest.raises(RuntimeError, match="LLM API call failed"):
            service.analyze_text("Test text")