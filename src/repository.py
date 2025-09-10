import json
from sqlalchemy.orm import Session
from .db_models import Analysis
from .models import AnalysisResult

class AnalysisRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, analysis_data: dict) -> Analysis:
        analysis = Analysis(
            text=analysis_data["text"],
            summary=analysis_data["summary"],
            title=analysis_data.get("title"),
            topics=json.dumps(analysis_data["topics"]),
            sentiment=analysis_data["sentiment"],
            keywords=json.dumps(analysis_data["keywords"])
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis
    
    def search_by_topic(self, topic: str) -> list[Analysis]:
        return self.db.query(Analysis).filter(
            Analysis.topics.contains(topic)
        ).all()
    
    def to_model(self, analysis: Analysis) -> AnalysisResult:
        return AnalysisResult(
            id=analysis.id,
            text=analysis.text,
            summary=analysis.summary,
            title=analysis.title,
            topics=json.loads(analysis.topics),
            sentiment=analysis.sentiment,
            keywords=json.loads(analysis.keywords),
            created_at=analysis.created_at
        )