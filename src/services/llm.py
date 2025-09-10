import os
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo",
            temperature=0
        )
    
    def analyze_text(self, text: str) -> dict:
        prompt = f"""
        Analyze this text and return a JSON response with:
        - summary: 1-2 sentence summary
        - title: extract title if available, null if not
        - topics: array of 3 key topics
        - sentiment: "positive", "neutral", or "negative"
        
        Text: {text}
        
        Return only valid JSON.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return json.loads(response.content)
        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {str(e)}")