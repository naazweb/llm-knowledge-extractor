from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    summary = Column(Text)
    title = Column(String)
    topics = Column(String)  # JSON string
    sentiment = Column(String)
    keywords = Column(String)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)