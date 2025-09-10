# LLM Knowledge Extractor

A prototype system that processes unstructured text using LLMs to generate summaries and extract structured metadata.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Local Development
Run the API server:
```bash
uvicorn main:app --reload
```

### Docker
Build and run with Docker:
```bash
docker-compose up --build
```

## Testing

Run tests:
```bash
pytest
```

## API Endpoints

- `POST /analyze` - Process text and return analysis
- `GET /search?topic=xyz` - Search stored analyses

## Design Choices

### Architecture
- **FastAPI**: Chosen for automatic API documentation, built-in validation with Pydantic, and async support for future scalability
- **LangChain**: Provides LLM abstraction layer, making it easy to switch between different models (OpenAI, Claude, etc.) without code changes
- **SQLite**: Lightweight database perfect for prototyping - no setup required, file-based storage, sufficient for demo purposes
- **SQLAlchemy**: ORM for database abstraction and easy migration to PostgreSQL if needed

### Code Structure
- **Separation of Concerns**: Split into services (LLM, analyzer), repository (data access), and API layers
- **Dual Model Pattern**: Separate Pydantic models (API validation) from SQLAlchemy models (database schema)
- **Dependency Injection**: FastAPI's DI system for clean testing and service management
- **TDD Approach**: Tests written first to ensure reliability and catch regressions quickly

### Trade-offs
- **Keyword Extraction**: Used simple NLTK approach instead of advanced NLP for time constraints
- **Error Handling**: Basic implementation - production would need more granular error types
- **Caching**: No LLM response caching implemented due to time limits

## Potential Enhancements

### Core Features
- **Batch Processing**: Process multiple texts in single request
- **Confidence Scoring**: Add analysis confidence metrics based on text quality
- **Advanced Search**: Multi-parameter filtering (sentiment + topic + keywords)
- **Fuzzy Search**: Partial matching for topics and keywords

### API Improvements
- **CRUD Operations**: Full analysis management (GET /analyses/{id}, DELETE /analyses/{id})
- **Pagination**: Handle large result sets efficiently
- **Analytics Endpoint**: GET /stats for usage metrics and topic distributions
- **Health Checks**: System status monitoring

### Performance & Production
- **Async Processing**: Queue long-running LLM calls with background tasks
- **Rate Limiting**: Prevent API abuse and manage costs
- **Response Caching**: Cache LLM results for identical inputs
- **Logging & Monitoring**: Request tracking and performance metrics
- **Authentication**: API key or JWT-based access control
