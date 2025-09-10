from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TextInput(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    id: Optional[int] = None
    text: str
    summary: str
    title: Optional[str] = None
    topics: List[str]
    sentiment: str
    keywords: List[str]
    created_at: Optional[datetime] = None

class SearchQuery(BaseModel):
    topic: str