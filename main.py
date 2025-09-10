from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.models import TextInput, AnalysisResult
from src.services.analyzer import TextAnalyzer
from src.repository import AnalysisRepository
from src.database import get_db, create_tables

app = FastAPI(title="LLM Knowledge Extractor")

@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/")
def root():
    return {"message": "LLM Knowledge Extractor API"}

@app.post("/analyze", response_model=AnalysisResult)
def analyze_text(input_data: TextInput, db: Session = Depends(get_db)):
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        analyzer = TextAnalyzer()
        result = analyzer.analyze(input_data.text)
        
        repo = AnalysisRepository(db)
        saved_analysis = repo.save(result)
        return repo.to_model(saved_analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/search")
def search_analyses(topic: str, db: Session = Depends(get_db)):
    if not topic.strip():
        raise HTTPException(status_code=400, detail="Topic parameter cannot be empty")
    
    repo = AnalysisRepository(db)
    analyses = repo.search_by_topic(topic.strip())
    return [repo.to_model(analysis) for analysis in analyses]