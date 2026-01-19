# QHSE Chatbot Project

A chatbot for QHSE (Quality, Health, Safety, Environment) data analysis and monitoring.

## Structure

- `src/`: Source code
  - `etl/`: Data collection and transformation
  - `api/`: FastAPI application
  - `db/`: Database models and connection
  - `monitoring/`: Logging and metrics
- `data/`: Data storage
- `scripts/`: Execution scripts
- `tests/`: Unit and integration tests

## Docker Setup

Build and run:
```bash
docker-compose up --build
```

## Manual Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run API:
   ```bash
   python -m uvicorn src.api.main:app --reload
   ```
