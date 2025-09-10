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

Run the API server:
```bash
uvicorn main:app --reload
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

Built with FastAPI for quick API development, LangChain for LLM abstraction, and SQLite for lightweight persistence. Used TDD approach to ensure reliability and maintainability within the 2-hour constraint.