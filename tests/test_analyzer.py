import pytest
from unittest.mock import Mock, patch
from src.services.analyzer import TextAnalyzer

class TestTextAnalyzer:
    
    @patch.dict('os.environ', {'DEBUG': 'false'})
    @patch('src.services.analyzer.LLMService')
    def test_analyze_success(self, mock_llm_service):
        # Mock LLM response
        mock_llm_instance = Mock()
        mock_llm_instance.analyze_text.return_value = {
            "summary": "This is a test summary.",
            "title": "Test Title",
            "topics": ["topic1", "topic2", "topic3"],
            "sentiment": "positive"
        }
        mock_llm_service.return_value = mock_llm_instance
        
        analyzer = TextAnalyzer()
        
        with patch('nltk.word_tokenize', return_value=['test', 'sample', 'text', 'sample']):
            with patch('nltk.pos_tag', return_value=[('test', 'NN'), ('sample', 'NN'), ('text', 'NN'), ('sample', 'NN')]):
                result = analyzer.analyze("Test sample text")
        
        assert result["summary"] == "This is a test summary."
        assert result["title"] == "Test Title"
        assert result["topics"] == ["topic1", "topic2", "topic3"]
        assert result["sentiment"] == "positive"
        assert result["keywords"] == ["sample", "test", "text"]
    
    @patch.dict('os.environ', {'DEBUG': 'false'})
    @patch('src.services.analyzer.LLMService')
    def test_analyze_empty_text(self, mock_llm_service):
        analyzer = TextAnalyzer()
        
        with pytest.raises(ValueError, match="Text cannot be empty"):
            analyzer.analyze("")
    
    @patch.dict('os.environ', {'DEBUG': 'false'})
    @patch('src.services.analyzer.LLMService')
    def test_analyze_llm_failure(self, mock_llm_service):
        mock_llm_instance = Mock()
        mock_llm_instance.analyze_text.side_effect = RuntimeError("LLM API failed")
        mock_llm_service.return_value = mock_llm_instance
        
        analyzer = TextAnalyzer()
        
        with pytest.raises(RuntimeError, match="Analysis failed"):
            analyzer.analyze("Test text")
    
    @patch.dict('os.environ', {'DEBUG': 'false'})
    @patch('src.services.analyzer.LLMService')
    def test_extract_keywords(self, mock_llm_service):
        analyzer = TextAnalyzer()
        
        with patch('nltk.word_tokenize', return_value=['the', 'cat', 'sat', 'on', 'the', 'mat', 'cat']):
            with patch('nltk.pos_tag', return_value=[('the', 'DT'), ('cat', 'NN'), ('sat', 'VBD'), ('on', 'IN'), ('the', 'DT'), ('mat', 'NN'), ('cat', 'NN')]):
                keywords = analyzer.extract_keywords("The cat sat on the mat cat")
        
        assert keywords == ["cat", "mat"]