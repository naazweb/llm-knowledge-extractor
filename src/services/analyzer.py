import nltk
from collections import Counter
from src.services.llm import LLMService

class TextAnalyzer:
    def __init__(self):
        self.llm_service = LLMService()
        self._download_nltk_data()
    
    def _download_nltk_data(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
    
    def extract_keywords(self, text: str) -> list:
        tokens = nltk.word_tokenize(text.lower())
        pos_tags = nltk.pos_tag(tokens)
        nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
        return [word for word, _ in Counter(nouns).most_common(3)]
    

    
    def analyze(self, text: str) -> dict:
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            llm_result = self.llm_service.analyze_text(text)
            keywords = self.extract_keywords(text)
            
            return {
                "text": text,
                "summary": llm_result["summary"],
                "title": llm_result.get("title"),
                "topics": llm_result["topics"],
                "sentiment": llm_result["sentiment"],
                "keywords": keywords
            }
        except Exception as e:
            raise RuntimeError(f"Analysis failed: {str(e)}")