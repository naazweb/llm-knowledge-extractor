class MockLLMService:
    def analyze_text(self, text: str) -> dict:
        return {
            "summary": f"Mock summary of: {text[:50]}...",
            "title": "Mock Title" if len(text) > 20 else None,
            "topics": ["mock", "testing", "development"],
            "sentiment": "neutral"
        }