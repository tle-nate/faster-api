# <<PROJECT_NAME>>

This is generic FastAPI template with built in user registration and authentication. 

The app relies on PostgreSQL. A docker-compose is provided [here](../docker/backend-services/docker-compose.yml). 

## Getting Started

1. Copy `.env.example` to `.env` and adjust any variables.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```bash
   alembic revision --autogenerate -m "Initial Commit"
   alembic upgrade head
   ```
4. Start the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```


## Running the test suite 

```bash 
pytest -q --disable-warnings --maxfail=1  
```