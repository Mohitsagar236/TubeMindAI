# TubeMind AI backend

FastAPI backend for transcript ingestion, timestamp-aware chunking, per-video RAG chat, summaries, notes, quizzes, flashcards, and saved history.

## Run locally

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Set `DATABASE_URL=sqlite:///./tubemind.db` for a zero-setup local/test database. PostgreSQL is recommended for production. The app also creates missing tables on startup for convenient local use; Alembic remains the deployment migration path.

The server API is under `http://localhost:8000/api`; interactive docs are at `/docs`. A client-owned OpenAI key may be sent as `X-OpenAI-API-Key` (recommended) or as `apiKey` on AI request bodies. Keys are never persisted or logged. Without a key, health and history remain available, while operations needing OpenAI return a clear `503`.

## Endpoints

- `GET /api/health`
- `POST /api/videos/process`
- `POST /api/chat`
- `POST /api/videos/summary`
- `POST /api/notes/generate`
- `POST /api/quiz/generate`
- `POST /api/flashcards/generate`
- `GET /api/history`
- `GET /api/settings/providers`

Vector retrieval always applies the `youtubeVideoId` Chroma filter. Incoming URLs are restricted to supported YouTube hosts and must match the claimed video ID.

## Production notes

Run migrations before each release, use PostgreSQL and a durable `CHROMA_PERSIST_DIR`, restrict CORS to known extension IDs, and put the API behind TLS/auth/rate limiting. For long videos, move ingestion to a job queue. The default synchronous request flow is intended for the MVP.
