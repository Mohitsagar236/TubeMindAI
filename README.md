# TubeMind AI

TubeMind AI is a Chrome Manifest V3 extension and FastAPI service for chatting with the transcript of the current YouTube video. The backend indexes timestamped transcript chunks, retrieves only chunks belonging to the active video, and returns grounded answers with clickable sources.

## Repository layout

- `backend/` — FastAPI, SQLAlchemy, transcript processing, ChromaDB, and OpenAI integration
- `extension/` — React, TypeScript, Vite, and Tailwind Chrome extension
- `tests/` — offline backend utility and API-contract tests
- `DOC.MD` — product and architecture specification

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker Desktop (recommended for PostgreSQL)
- An OpenAI API key for embedding and generation features

## Run locally

1. Copy `.env.example` to `.env`, then set `OPENAI_API_KEY`.
2. Start PostgreSQL:

   ```bash
   docker compose up -d
   ```

3. Start the backend:

   ```bash
   cd backend
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. In another terminal, build the extension:

   ```bash
   cd extension
   npm install
   npm run build
   ```

5. Open `chrome://extensions`, enable Developer mode, choose **Load unpacked**, and select `extension/dist`.

The API health check is available at `http://localhost:8000/api/health`. The extension defaults to this backend address.

## Tests

After installing the backend requirements and `pytest`, run from the repository root:

```bash
python -m pytest
```

The root test suite is intentionally offline: it does not call YouTube, OpenAI, ChromaDB, or PostgreSQL.

## Configuration and security

Runtime settings come from `.env`; see `.env.example` for supported values. Never commit `.env`, API keys, local databases, Chroma data, or extension build output. A user-supplied API key is accepted only as a request secret and must not be logged or serialized into API responses.

## MVP behavior

- Only valid YouTube URLs are accepted, and their video ID must match the request.
- Retrieval is scoped by `youtubeVideoId` to prevent cross-video context leakage.
- Answers are grounded in transcript context and include timestamp sources when available.
- When the transcript lacks an answer, the assistant returns: `This information is not available in the video.`

