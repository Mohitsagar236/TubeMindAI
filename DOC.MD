# Full Stack RAG YouTube Chat Chrome Extension — Codex Build Document

## 1. Project Goal

Build a full stack application where users can chat with the currently opened YouTube video using a Chrome Extension.

The user should be able to open any YouTube video, click the extension, and ask questions related to that video. The system should fetch the video transcript, process it using RAG, store embeddings in a vector database, and answer user questions using LangChain and an LLM.

The final product should feel like:

**“ChatGPT for YouTube videos inside a Chrome Extension.”**

---

## 2. Product Name

Use this temporary product name:

**TubeMind AI**

You can change the name later.

---

## 3. Main User Flow

1. User installs Chrome Extension.
2. User opens a YouTube video.
3. Extension automatically detects the current YouTube video URL and video ID.
4. User opens the extension popup.
5. Extension shows current video title, thumbnail, and chat box.
6. User asks a question.
7. Backend checks if the video transcript is already indexed.
8. If not indexed:

   * Fetch transcript.
   * Clean transcript.
   * Split transcript into chunks.
   * Generate embeddings.
   * Store embeddings in vector database.
9. Backend retrieves relevant transcript chunks using vector similarity search.
10. LangChain sends retrieved context and user question to LLM.
11. LLM returns answer based only on the video transcript.
12. Extension displays answer with timestamp references.
13. User can also generate summary, notes, quiz, and flashcards.

---

## 4. Core Features

### 4.1 Chrome Extension

The Chrome Extension should:

* Detect current YouTube video.
* Show current video title and thumbnail.
* Provide a modern chat interface.
* Allow users to ask questions about the current video.
* Show AI answers in a clean format.
* Show source timestamps.
* Provide buttons for:

  * Summarize Video
  * Generate Notes
  * Generate Quiz
  * Generate Flashcards
* Save basic chat state in Chrome local storage.
* Allow users to configure API provider settings if needed.

---

### 4.2 Chat With Current YouTube Video

The user can ask questions like:

* “Summarize this video.”
* “What is the main topic?”
* “Explain this in simple words.”
* “What did the speaker say about RAG?”
* “Give me interview questions from this video.”
* “Create study notes from this video.”

The answer must be generated using only the transcript of the current YouTube video.

If the answer is not present in the transcript, the system must reply:

“This information is not available in the video.”

---

### 4.3 Timestamp Sources

Each answer should include source timestamps.

Example:

Answer:

“RAG stands for Retrieval Augmented Generation. It combines information retrieval with text generation to produce grounded responses.”

Sources:

* 04:12 - 05:30
* 07:15 - 08:02

When the user clicks a timestamp, the extension should open the YouTube video at that timestamp.

---

### 4.4 Video Summary

Provide summary options:

* Short Summary
* Detailed Summary
* Key Points
* Chapter-wise Summary

The summary should be generated from transcript content only.

---

### 4.5 Study Notes Generator

Generate structured study notes with:

* Topic
* Introduction
* Key Concepts
* Important Definitions
* Step-by-step Explanation
* Examples
* Important Points
* Quick Revision Section
* Interview Questions

---

### 4.6 Quiz Generator

Generate quiz from video transcript.

Quiz types:

* MCQ
* True/False
* Short Answer

For MVP, implement MCQ first.

Each MCQ should include:

* Question
* 4 options
* Correct answer
* Explanation

---

### 4.7 Flashcard Generator

Generate flashcards from video transcript.

Each flashcard should include:

* Front: question / term
* Back: answer / explanation

---

### 4.8 Saved History

Save:

* Processed videos
* Chat sessions
* Generated notes
* Generated summaries
* Generated quizzes
* Generated flashcards

For MVP, use backend database for saved history and Chrome local storage for temporary UI state.

---

### 4.9 User API Key Support

Allow user to add their own LLM API key.

Supported providers:

* OpenAI
* Gemini
* Anthropic

For MVP, start with OpenAI.

User should be able to enter API key in settings page.

Important:

* API keys must not be logged.
* API keys should be stored securely.
* For MVP, store user API key locally in Chrome storage if backend auth is not implemented.
* In production, encrypt keys before storing.

---

## 5. Recommended Tech Stack

### Frontend Extension

Use:

* React
* TypeScript
* Vite
* Tailwind CSS
* Chrome Extension Manifest V3

### Backend

Use:

* Python
* FastAPI
* LangChain
* SQLAlchemy
* Alembic
* Pydantic

### Database

Use:

* PostgreSQL for app data
* ChromaDB for local MVP vector database

Later production option:

* Qdrant
* Pinecone
* Weaviate

### AI

Use:

* LangChain
* OpenAI Chat Model
* OpenAI Embedding Model

Recommended models:

* Chat: `gpt-4o-mini` or similar cost-effective model
* Embedding: `text-embedding-3-small`

### Transcript

Use:

* YouTube transcript API for transcript fetching
* Whisper fallback later if transcript unavailable

---

## 6. High Level Architecture

```mermaid
flowchart TD

    User[User on YouTube] --> Extension[Chrome Extension]

    Extension --> Detector[Detect Current YouTube Video]
    Detector --> Backend[FastAPI Backend]

    Backend --> VideoService[Video Processing Service]
    Backend --> ChatService[Chat Service]
    Backend --> NotesService[Notes Service]
    Backend --> QuizService[Quiz Service]

    VideoService --> TranscriptService[Transcript Service]
    TranscriptService --> YTTranscript[YouTube Transcript API]

    VideoService --> ChunkingService[Chunking Service]
    ChunkingService --> EmbeddingService[Embedding Service]
    EmbeddingService --> VectorDB[(ChromaDB Vector Store)]

    Backend --> Postgres[(PostgreSQL)]

    ChatService --> RAGPipeline[LangChain RAG Pipeline]
    RAGPipeline --> VectorDB
    RAGPipeline --> LLM[OpenAI / Gemini / Claude]

    LLM --> ChatService
    ChatService --> Backend
    Backend --> Extension
    Extension --> User
```

---

## 7. Low Level Request Flow

```mermaid
sequenceDiagram
    participant User
    participant Extension
    participant Backend
    participant VideoService
    participant TranscriptService
    participant VectorDB
    participant LangChain
    participant LLM

    User->>Extension: Opens YouTube video
    Extension->>Extension: Extract videoId from current tab URL

    User->>Extension: Ask question
    Extension->>Backend: POST /api/chat {youtubeVideoId, question}

    Backend->>VideoService: Check if video is already indexed

    alt Video not indexed
        VideoService->>TranscriptService: Fetch transcript
        TranscriptService-->>VideoService: Transcript with timestamps
        VideoService->>VideoService: Clean transcript
        VideoService->>VideoService: Split transcript into chunks
        VideoService->>VectorDB: Store chunks and embeddings
        VideoService->>Backend: Mark video as indexed
    end

    Backend->>LangChain: Run RAG with question and videoId
    LangChain->>VectorDB: Retrieve top relevant chunks
    VectorDB-->>LangChain: Relevant chunks with timestamps
    LangChain->>LLM: Send prompt with context
    LLM-->>LangChain: Answer
    LangChain-->>Backend: Answer + sources
    Backend-->>Extension: Return response
    Extension-->>User: Show answer and timestamps
```

---

## 8. Monorepo Structure

Create a monorepo with this structure:

```text
youtube-rag-extension/
│
├── README.md
├── .gitignore
├── docker-compose.yml
├── .env.example
│
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   │
│   │   ├── api/
│   │   │   ├── health_routes.py
│   │   │   ├── video_routes.py
│   │   │   ├── chat_routes.py
│   │   │   ├── notes_routes.py
│   │   │   ├── quiz_routes.py
│   │   │   └── settings_routes.py
│   │   │
│   │   ├── services/
│   │   │   ├── video_service.py
│   │   │   ├── transcript_service.py
│   │   │   ├── chunking_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── notes_service.py
│   │   │   ├── quiz_service.py
│   │   │   └── flashcard_service.py
│   │   │
│   │   ├── vector_store/
│   │   │   ├── chroma_client.py
│   │   │   └── retriever.py
│   │   │
│   │   ├── prompts/
│   │   │   ├── chat_prompt.py
│   │   │   ├── summary_prompt.py
│   │   │   ├── notes_prompt.py
│   │   │   ├── quiz_prompt.py
│   │   │   └── flashcard_prompt.py
│   │   │
│   │   └── utils/
│   │       ├── youtube.py
│   │       ├── time_utils.py
│   │       └── text_utils.py
│   │
│   └── migrations/
│
└── extension/
    ├── README.md
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── manifest.json
    │
    ├── public/
    │   ├── icons/
    │   │   ├── icon16.png
    │   │   ├── icon48.png
    │   │   └── icon128.png
    │   └── logo.png
    │
    └── src/
        ├── background.ts
        ├── contentScript.ts
        │
        ├── popup/
        │   ├── main.tsx
        │   ├── App.tsx
        │   ├── components/
        │   │   ├── Layout.tsx
        │   │   ├── Header.tsx
        │   │   ├── VideoCard.tsx
        │   │   ├── ChatWindow.tsx
        │   │   ├── MessageBubble.tsx
        │   │   ├── ChatInput.tsx
        │   │   ├── QuickActions.tsx
        │   │   ├── SourceTimestamp.tsx
        │   │   ├── LoadingState.tsx
        │   │   ├── EmptyState.tsx
        │   │   └── ErrorState.tsx
        │   │
        │   ├── pages/
        │   │   ├── ChatPage.tsx
        │   │   ├── NotesPage.tsx
        │   │   ├── QuizPage.tsx
        │   │   ├── FlashcardsPage.tsx
        │   │   └── SettingsPage.tsx
        │   │
        │   ├── api/
        │   │   └── backendClient.ts
        │   │
        │   ├── hooks/
        │   │   ├── useCurrentTab.ts
        │   │   ├── useYoutubeVideo.ts
        │   │   ├── useChat.ts
        │   │   └── useChromeStorage.ts
        │   │
        │   ├── types/
        │   │   └── index.ts
        │   │
        │   └── utils/
        │       ├── youtube.ts
        │       └── format.ts
```

---

## 9. Backend Environment Variables

Create `.env.example`:

```env
APP_NAME=TubeMind AI
APP_ENV=development
API_HOST=0.0.0.0
API_PORT=8000

DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/tubemind

CHROMA_PERSIST_DIR=./chroma_data
CHROMA_COLLECTION_NAME=youtube_transcripts

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

CORS_ORIGINS=http://localhost:5173,chrome-extension://*
```

---

## 10. Backend Dependencies

Create `backend/requirements.txt`:

```txt
fastapi
uvicorn[standard]
python-dotenv
pydantic
pydantic-settings
sqlalchemy
psycopg2-binary
alembic
langchain
langchain-openai
langchain-community
chromadb
youtube-transcript-api
httpx
python-multipart
```

---

## 11. Database Schema

Use PostgreSQL.

### 11.1 users

For MVP, user table can be optional. Still create it for future login.

```text
users
-----
id UUID primary key
email varchar unique nullable
name varchar nullable
created_at timestamp
updated_at timestamp
```

---

### 11.2 videos

```text
videos
------
id UUID primary key
youtube_video_id varchar unique not null
youtube_url text not null
title text nullable
channel_name text nullable
thumbnail_url text nullable
duration_seconds integer nullable
language varchar nullable
transcript_status varchar not null default 'pending'
indexed_status varchar not null default 'pending'
error_message text nullable
created_at timestamp
updated_at timestamp
```

Status values:

```text
pending
processing
completed
failed
```

---

### 11.3 transcript_chunks

```text
transcript_chunks
-----------------
id UUID primary key
video_id UUID foreign key videos.id
chunk_index integer not null
text text not null
start_time_seconds float nullable
end_time_seconds float nullable
metadata_json jsonb nullable
created_at timestamp
```

---

### 11.4 chat_sessions

```text
chat_sessions
-------------
id UUID primary key
video_id UUID foreign key videos.id
user_id UUID nullable
title text nullable
created_at timestamp
updated_at timestamp
```

---

### 11.5 chat_messages

```text
chat_messages
-------------
id UUID primary key
chat_session_id UUID foreign key chat_sessions.id
role varchar not null
content text not null
sources_json jsonb nullable
created_at timestamp
```

Role values:

```text
user
assistant
system
```

---

### 11.6 generated_notes

```text
generated_notes
---------------
id UUID primary key
video_id UUID foreign key videos.id
user_id UUID nullable
title text not null
content text not null
format varchar not null
created_at timestamp
updated_at timestamp
```

---

### 11.7 generated_quizzes

```text
generated_quizzes
-----------------
id UUID primary key
video_id UUID foreign key videos.id
user_id UUID nullable
quiz_json jsonb not null
created_at timestamp
updated_at timestamp
```

---

### 11.8 generated_flashcards

```text
generated_flashcards
--------------------
id UUID primary key
video_id UUID foreign key videos.id
user_id UUID nullable
flashcards_json jsonb not null
created_at timestamp
updated_at timestamp
```

---

## 12. API Endpoints

Base URL:

```text
http://localhost:8000/api
```

---

### 12.1 Health Check

```http
GET /api/health
```

Response:

```json
{
  "status": "ok",
  "app": "TubeMind AI"
}
```

---

### 12.2 Process Video

```http
POST /api/videos/process
```

Request:

```json
{
  "youtubeUrl": "https://www.youtube.com/watch?v=abc123",
  "youtubeVideoId": "abc123",
  "title": "Optional title",
  "thumbnailUrl": "Optional thumbnail"
}
```

Response:

```json
{
  "videoId": "uuid",
  "youtubeVideoId": "abc123",
  "indexedStatus": "completed",
  "transcriptStatus": "completed"
}
```

Behavior:

* Check if video already exists by `youtube_video_id`.
* If already indexed, return existing status.
* If not indexed:

  * Fetch transcript.
  * Store video record.
  * Chunk transcript.
  * Store chunks in PostgreSQL.
  * Generate embeddings.
  * Store vectors in ChromaDB.
  * Mark video as completed.

---

### 12.3 Chat With Video

```http
POST /api/chat
```

Request:

```json
{
  "youtubeUrl": "https://www.youtube.com/watch?v=abc123",
  "youtubeVideoId": "abc123",
  "question": "What is this video about?",
  "chatSessionId": null
}
```

Response:

```json
{
  "chatSessionId": "uuid",
  "answer": "This video explains...",
  "sources": [
    {
      "text": "Transcript chunk text...",
      "startTimeSeconds": 252,
      "endTimeSeconds": 318,
      "startTimeLabel": "04:12",
      "endTimeLabel": "05:18",
      "youtubeUrl": "https://www.youtube.com/watch?v=abc123&t=252s"
    }
  ]
}
```

Behavior:

* Ensure video is processed.
* Retrieve top relevant chunks using vector search.
* Build strict RAG prompt.
* Call LLM.
* Save user message and assistant response.
* Return answer with sources.

---

### 12.4 Generate Summary

```http
POST /api/videos/summary
```

Request:

```json
{
  "youtubeVideoId": "abc123",
  "summaryType": "short"
}
```

Allowed summary types:

```text
short
detailed
key_points
chapter_wise
```

Response:

```json
{
  "summary": "Video summary..."
}
```

---

### 12.5 Generate Notes

```http
POST /api/notes/generate
```

Request:

```json
{
  "youtubeVideoId": "abc123",
  "format": "study_notes"
}
```

Response:

```json
{
  "title": "Study Notes",
  "content": "Markdown notes..."
}
```

---

### 12.6 Generate Quiz

```http
POST /api/quiz/generate
```

Request:

```json
{
  "youtubeVideoId": "abc123",
  "numberOfQuestions": 10,
  "difficulty": "medium"
}
```

Response:

```json
{
  "questions": [
    {
      "question": "What is RAG?",
      "options": [
        "Retrieval Augmented Generation",
        "Random Answer Generation",
        "Rapid API Gateway",
        "Real Application Graph"
      ],
      "correctAnswer": "Retrieval Augmented Generation",
      "explanation": "The video explains that RAG means..."
    }
  ]
}
```

---

### 12.7 Generate Flashcards

```http
POST /api/flashcards/generate
```

Request:

```json
{
  "youtubeVideoId": "abc123",
  "numberOfCards": 10
}
```

Response:

```json
{
  "flashcards": [
    {
      "front": "What is RAG?",
      "back": "RAG stands for Retrieval Augmented Generation."
    }
  ]
}
```

---

### 12.8 Get Video History

```http
GET /api/videos/history
```

Response:

```json
{
  "videos": [
    {
      "youtubeVideoId": "abc123",
      "title": "Video title",
      "thumbnailUrl": "thumbnail",
      "indexedStatus": "completed",
      "createdAt": "2026-07-15T10:00:00"
    }
  ]
}
```

---

## 13. RAG Pipeline Requirements

### 13.1 Transcript Fetching

Use `youtube-transcript-api`.

Requirements:

* Fetch transcript by YouTube video ID.
* Prefer English transcript.
* If English is not available, use available transcript.
* Store transcript entries with:

  * text
  * start time
  * duration
  * end time

If transcript is unavailable, return a proper error:

```text
Transcript is not available for this video.
```

---

### 13.2 Transcript Cleaning

Clean transcript by:

* Removing extra spaces.
* Merging short lines.
* Preserving timestamps.
* Removing empty text.
* Keeping original meaning unchanged.

---

### 13.3 Chunking Strategy

Use transcript-aware chunking.

Requirements:

* Chunk size: around 800 to 1200 characters.
* Chunk overlap: 150 to 250 characters.
* Preserve start and end timestamp for each chunk.
* Do not split in a way that loses timestamp mapping.

Each chunk should contain:

```json
{
  "chunkIndex": 1,
  "text": "Chunk text...",
  "startTimeSeconds": 120,
  "endTimeSeconds": 180
}
```

---

### 13.4 Embedding Storage

Use ChromaDB collection:

```text
youtube_transcripts
```

Each vector should include metadata:

```json
{
  "youtubeVideoId": "abc123",
  "videoDbId": "uuid",
  "chunkIndex": 1,
  "startTimeSeconds": 120,
  "endTimeSeconds": 180
}
```

---

### 13.5 Retrieval

When user asks a question:

* Convert question into embedding.
* Search ChromaDB.
* Filter by `youtubeVideoId`.
* Return top 5 relevant chunks.
* Use these chunks as context for LLM.

---

## 14. Prompt Templates

### 14.1 Chat Prompt

```text
You are TubeMind AI, an assistant that answers questions using only the provided YouTube video transcript context.

Rules:
1. Answer only from the provided context.
2. If the answer is not present in the context, say: "This information is not available in the video."
3. Do not make up facts.
4. Keep the answer clear, simple, and useful.
5. If the user asks for explanation, explain step by step.
6. If relevant, mention the timestamp sources.
7. Do not mention that you are using embeddings or vector search.

Video Context:
{context}

User Question:
{question}

Answer:
```

---

### 14.2 Summary Prompt

```text
You are TubeMind AI. Generate a summary using only the provided YouTube transcript.

Rules:
1. Use only the transcript content.
2. Do not add external information.
3. Keep the summary clear and structured.
4. If the transcript is technical, explain in simple language.

Summary Type:
{summary_type}

Transcript:
{transcript}

Output:
```

---

### 14.3 Study Notes Prompt

```text
You are TubeMind AI. Convert the provided YouTube transcript into proper study notes.

Rules:
1. Use only the transcript.
2. Do not add external information.
3. Make the notes easy for students to revise.
4. Use headings, bullet points, and examples where possible.
5. Include important definitions and key takeaways.

Required format:

# Title

## 1. Introduction

## 2. Key Concepts

## 3. Detailed Explanation

## 4. Examples

## 5. Important Points

## 6. Quick Revision

## 7. Interview Questions

Transcript:
{transcript}

Study Notes:
```

---

### 14.4 Quiz Prompt

```text
You are TubeMind AI. Generate a quiz from the provided YouTube transcript.

Rules:
1. Use only the transcript.
2. Do not create questions from outside knowledge.
3. Each question must have exactly 4 options.
4. Only one option should be correct.
5. Include the correct answer and a short explanation.

Number of questions:
{number_of_questions}

Difficulty:
{difficulty}

Transcript:
{transcript}

Return valid JSON in this format:
{
  "questions": [
    {
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correctAnswer": "...",
      "explanation": "..."
    }
  ]
}
```

---

### 14.5 Flashcard Prompt

```text
You are TubeMind AI. Generate flashcards from the provided YouTube transcript.

Rules:
1. Use only the transcript.
2. Keep flashcards short and useful.
3. Front side should contain a question or term.
4. Back side should contain the answer or explanation.

Number of cards:
{number_of_cards}

Transcript:
{transcript}

Return valid JSON:
{
  "flashcards": [
    {
      "front": "...",
      "back": "..."
    }
  ]
}
```

---

## 15. Chrome Extension UI/UX Requirements

The extension UI should look modern, clean, and premium.

### 15.1 Popup Size

Use:

```text
Width: 420px
Height: 620px
```

The UI should be responsive inside popup.

---

### 15.2 Visual Style

Use:

* Clean white or soft dark theme.
* Rounded cards.
* Soft shadows.
* Modern font.
* Good spacing.
* Smooth hover states.
* Clear loading states.
* Minimal but premium design.

Suggested design direction:

```text
Dark sidebar-style header
Gradient primary button
Card-based layout
Clean chat bubbles
Timestamp chips
```

---

### 15.3 Main Layout

Extension popup should have:

1. Header
2. Current video card
3. Quick action buttons
4. Chat messages
5. Chat input

Layout:

```text
+------------------------------------------------+
| TubeMind AI                           Settings |
+------------------------------------------------+
| Current Video                                  |
| [Thumbnail] Video title...                     |
| Status: Ready / Processing / Indexed           |
+------------------------------------------------+
| [Summary] [Notes] [Quiz] [Flashcards]          |
+------------------------------------------------+
| Chat Area                                      |
|                                                |
| User message                                   |
| AI answer                                      |
| Sources: 04:12  05:18                          |
|                                                |
+------------------------------------------------+
| Ask anything about this video...        Send   |
+------------------------------------------------+
```

---

### 15.4 Header

Header should include:

* App logo
* App name
* Settings icon

Example:

```text
TubeMind AI
Chat with this video
```

---

### 15.5 Video Card

Video card should show:

* Thumbnail
* Title
* YouTube video ID
* Indexing status

Indexing statuses:

* Not processed
* Processing
* Ready
* Failed

Use color indicators:

* Gray: not processed
* Yellow: processing
* Green: ready
* Red: failed

---

### 15.6 Quick Actions

Buttons:

* Summary
* Notes
* Quiz
* Flashcards

Each button should be compact and visually clear.

When clicked:

* Send request to backend.
* Show loading state.
* Display generated content in the chat or separate page.

---

### 15.7 Chat Design

User message:

* Align right.
* Primary colored bubble.
* White text.

Assistant message:

* Align left.
* Light card bubble.
* Dark text.
* Support markdown rendering.

Sources:

* Show as small clickable timestamp chips.
* Example:

```text
Sources: 04:12  05:18  07:30
```

Clicking timestamp should open current YouTube video at that time.

---

### 15.8 Loading States

Use friendly loading messages:

```text
Processing video transcript...
Finding relevant parts...
Generating answer...
Creating study notes...
```

Use skeleton loaders or animated dots.

---

### 15.9 Empty State

When user opens extension on YouTube video but has not asked anything:

```text
Ask anything about this video.
Try:
- Summarize this video
- Explain the main concept
- Generate study notes
```

---

### 15.10 Error State

If no YouTube video is detected:

```text
Open a YouTube video to start chatting.
```

If transcript unavailable:

```text
Transcript is not available for this video.
```

If backend is unavailable:

```text
Unable to connect to TubeMind backend. Please make sure the backend server is running.
```

---

## 16. Extension Manifest V3

Create `manifest.json`:

```json
{
  "manifest_version": 3,
  "name": "TubeMind AI",
  "version": "1.0.0",
  "description": "Chat with any YouTube video using AI.",
  "permissions": ["activeTab", "storage", "tabs"],
  "host_permissions": [
    "https://www.youtube.com/*",
    "http://localhost:8000/*"
  ],
  "background": {
    "service_worker": "src/background.ts"
  },
  "content_scripts": [
    {
      "matches": ["https://www.youtube.com/*"],
      "js": ["src/contentScript.ts"]
    }
  ],
  "action": {
    "default_popup": "index.html",
    "default_title": "TubeMind AI"
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

---

## 17. Frontend Types

Create TypeScript types:

```ts
export type VideoStatus = "not_processed" | "processing" | "ready" | "failed";

export interface CurrentVideo {
  youtubeVideoId: string;
  youtubeUrl: string;
  title?: string;
  thumbnailUrl?: string;
}

export interface SourceTimestamp {
  text: string;
  startTimeSeconds: number;
  endTimeSeconds: number;
  startTimeLabel: string;
  endTimeLabel: string;
  youtubeUrl: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: SourceTimestamp[];
  createdAt: string;
}

export interface ChatResponse {
  chatSessionId: string;
  answer: string;
  sources: SourceTimestamp[];
}
```

---

## 18. YouTube Video Detection

Implement utility function:

```ts
export function extractYoutubeVideoId(url: string): string | null {
  try {
    const parsedUrl = new URL(url);

    if (parsedUrl.hostname.includes("youtube.com")) {
      return parsedUrl.searchParams.get("v");
    }

    if (parsedUrl.hostname.includes("youtu.be")) {
      return parsedUrl.pathname.replace("/", "");
    }

    return null;
  } catch {
    return null;
  }
}
```

Also extract title from tab title:

```ts
const title = tab.title?.replace(" - YouTube", "");
```

Thumbnail URL:

```ts
const thumbnailUrl = `https://img.youtube.com/vi/${youtubeVideoId}/hqdefault.jpg`;
```

---

## 19. Backend Core Logic

### 19.1 Video Processing Service

Function:

```python
async def process_video(youtube_url: str, youtube_video_id: str, title: str | None, thumbnail_url: str | None):
    # 1. Check DB if video already exists and indexed
    # 2. If indexed, return existing video
    # 3. Create or update video status to processing
    # 4. Fetch transcript
    # 5. Clean transcript
    # 6. Chunk transcript
    # 7. Save chunks in PostgreSQL
    # 8. Generate and save embeddings in ChromaDB
    # 9. Mark video as completed
    # 10. Return video
```

---

### 19.2 Chat Service

Function:

```python
async def chat_with_video(youtube_video_id: str, youtube_url: str, question: str, chat_session_id: str | None):
    # 1. Ensure video is processed
    # 2. Retrieve relevant chunks from ChromaDB
    # 3. Build context from chunks
    # 4. Run LangChain prompt with LLM
    # 5. Save chat messages
    # 6. Return answer with sources
```

---

### 19.3 Retriever

Retriever should filter by video ID:

```python
filter = {
    "youtubeVideoId": youtube_video_id
}
```

Use top K:

```python
top_k = 5
```

---

## 20. Important Backend Rules

Implement these rules strictly:

1. Do not re-index video if already indexed.
2. Always filter vector search by `youtubeVideoId`.
3. Never answer using chunks from another video.
4. Never hallucinate.
5. Always return source timestamps when available.
6. Handle transcript unavailable error gracefully.
7. Do not expose API keys in logs.
8. Validate all request bodies with Pydantic.
9. Add CORS support for Chrome Extension and localhost.
10. Add clear error messages.

---

## 21. Docker Compose

Create `docker-compose.yml`:

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16
    container_name: tubemind-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: tubemind
    ports:
      - "5432:5432"
    volumes:
      - tubemind_postgres_data:/var/lib/postgresql/data

volumes:
  tubemind_postgres_data:
```

---

## 22. Backend Run Commands

From project root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run PostgreSQL:

```bash
docker compose up -d
```

---

## 23. Extension Run Commands

From project root:

```bash
cd extension
npm install
npm run dev
npm run build
```

To load extension:

1. Open Chrome.
2. Go to:

```text
chrome://extensions/
```

3. Enable Developer Mode.
4. Click “Load unpacked”.
5. Select:

```text
extension/dist
```

---

## 24. UI Implementation Instructions for Codex

Implement UI carefully with these rules:

1. Use Tailwind CSS.
2. Make the popup clean and premium.
3. Use reusable components.
4. Use loading states for every async action.
5. Use error messages that users can understand.
6. Keep chat scrollable.
7. Keep input fixed at bottom.
8. Support markdown rendering for AI answers.
9. Make timestamp chips clickable.
10. Add settings page for backend URL and API key.
11. Use icons from `lucide-react`.
12. Use soft rounded corners and spacing.
13. Do not make UI look like a basic form.
14. Prioritize good UX.

Suggested colors:

```text
Primary: Indigo / Blue
Background: #F8FAFC
Text: #0F172A
Muted: #64748B
Card: #FFFFFF
Border: #E2E8F0
```

---

## 25. Suggested Popup UI Component Structure

### App.tsx

Responsibilities:

* Detect current tab.
* Extract YouTube video.
* Hold selected page state.
* Render layout.

Pages:

* Chat
* Notes
* Quiz
* Flashcards
* Settings

---

### Header.tsx

Show:

* Logo
* Product name
* Settings button

---

### VideoCard.tsx

Show:

* Thumbnail
* Video title
* Status badge

---

### QuickActions.tsx

Show action buttons:

* Summary
* Notes
* Quiz
* Flashcards

---

### ChatWindow.tsx

Show:

* Empty state
* Message list
* Auto scroll to latest message

---

### ChatInput.tsx

Show:

* Input field
* Send button
* Enter-to-send support
* Disabled state when loading

---

### MessageBubble.tsx

Show:

* User bubble
* Assistant bubble
* Markdown answer
* Sources below assistant answer

---

### SourceTimestamp.tsx

Click action:

```ts
chrome.tabs.update({
  url: `${youtubeUrl}&t=${startTimeSeconds}s`
});
```

---

## 26. Non-Functional Requirements

### Performance

* Do not process the same video again and again.
* Cache indexed videos.
* Keep vector search limited to top K chunks.
* Use background processing later for long videos.

### Security

* Never log API keys.
* Validate inputs.
* Use CORS carefully.
* Do not allow arbitrary URL processing except valid YouTube URLs.
* Store secrets in environment variables.
* User API key should be stored securely.

### Reliability

* Handle backend down state.
* Handle transcript unavailable state.
* Handle LLM API failure.
* Handle vector DB failure.
* Return meaningful error messages.

### Scalability

For MVP:

* FastAPI + PostgreSQL + ChromaDB is enough.

For production:

* Replace ChromaDB with Qdrant or Pinecone.
* Add Redis cache.
* Add background worker.
* Add queue system.
* Add authentication.
* Add usage limits.

---

## 27. MVP Scope

Build these first:

1. Chrome Extension detects current YouTube video.
2. Backend fetches transcript.
3. Transcript is chunked.
4. Embeddings are stored in ChromaDB.
5. User can chat with video.
6. Answer includes timestamp sources.
7. Generate summary.
8. Generate study notes.
9. Basic good UI/UX.
10. Settings page for backend URL and API key.

---

## 28. Phase 2 Features

After MVP, add:

1. Quiz generator.
2. Flashcard generator.
3. Saved chat history.
4. Export notes to PDF.
5. Playlist support.
6. Multi-video chat.
7. Whisper transcription fallback.
8. Google login.
9. Payments and usage limits.
10. Deploy backend.

---

## 29. Acceptance Criteria

The implementation is complete when:

### Extension

* Extension opens correctly on YouTube.
* Extension detects current video ID.
* Extension shows video title and thumbnail.
* User can type a question and send it.
* User receives AI answer.
* User can click timestamp source and jump to video time.
* UI is clean and user-friendly.
* Loading and error states work.

### Backend

* Health endpoint works.
* Video processing endpoint works.
* Chat endpoint works.
* Summary endpoint works.
* Notes endpoint works.
* PostgreSQL stores video and chat data.
* ChromaDB stores transcript embeddings.
* Backend does not re-index already processed video.
* Backend handles missing transcript.

### RAG

* Answers are based on transcript.
* Retrieval is filtered by current video ID.
* If transcript does not contain answer, AI says information is not available.
* Sources include timestamps.

---

## 30. Testing Checklist

### Manual Test 1

Open YouTube video with transcript.

Ask:

```text
Summarize this video.
```

Expected:

* Video gets processed.
* Summary is returned.
* No error.

---

### Manual Test 2

Ask a specific question from video.

Expected:

* Answer is related to video.
* Timestamp sources are shown.

---

### Manual Test 3

Ask unrelated question:

```text
What is the capital of Japan?
```

Expected:

```text
This information is not available in the video.
```

Unless the video itself discusses this.

---

### Manual Test 4

Click timestamp source.

Expected:

* YouTube opens at that timestamp.

---

### Manual Test 5

Open video without transcript.

Expected:

* User sees proper error message.
* App does not crash.

---

### Manual Test 6

Click Generate Notes.

Expected:

* Notes are generated in structured markdown format.

---

## 31. Codex Implementation Prompt

Use this exact prompt in Codex:

```text
You are a senior full stack engineer.

Build a production-quality MVP for a Chrome Extension + FastAPI full stack application called TubeMind AI.

Goal:
Users can open any YouTube video, open the Chrome Extension, and chat with the video using RAG, LangChain, transcripts, embeddings, and an LLM.

Use this architecture:
- Frontend: Chrome Extension Manifest V3, React, TypeScript, Vite, Tailwind CSS
- Backend: Python FastAPI, LangChain, SQLAlchemy, PostgreSQL, ChromaDB
- Transcript: youtube-transcript-api
- LLM: OpenAI chat model
- Embeddings: OpenAI embeddings

Implement the monorepo structure exactly as described in this document.

Core requirements:
1. Chrome Extension detects current YouTube video URL and video ID.
2. Extension shows clean modern popup UI with video card, quick actions, chat window, and input.
3. Backend processes YouTube transcript.
4. Backend chunks transcript with timestamps.
5. Backend stores video and chunk metadata in PostgreSQL.
6. Backend stores embeddings in ChromaDB.
7. Chat endpoint uses LangChain RAG to answer questions using only current video transcript.
8. Retrieval must filter by youtubeVideoId.
9. Answer must include source timestamps.
10. If answer is not in transcript, assistant must say: “This information is not available in the video.”
11. Add summary generation.
12. Add study notes generation.
13. Add quiz and flashcard generation if time permits.
14. Add settings page in extension for backend URL and OpenAI API key.
15. Add good loading states, error states, empty states, and polished UI/UX.
16. Do not log API keys.
17. Add README files with setup instructions.
18. Add .env.example and docker-compose.yml.
19. Make code modular, typed, clean, and maintainable.
20. Prefer reusable services and components.

Build the complete working MVP, not only placeholders.
```

---

## 32. Final Notes for Implementation

Start with backend first:

1. Health API
2. Transcript fetch
3. Video processing
4. Chroma embedding storage
5. Chat endpoint
6. Summary endpoint
7. Notes endpoint

Then build extension:

1. Manifest
2. Current tab detection
3. Video card
4. Backend client
5. Chat UI
6. Quick actions
7. Settings page
8. Timestamp click support

Use simple MVP first. Once chat works end-to-end, improve UI and add advanced features.

The most important part is this flow:

```text
Current YouTube video
        ↓
Transcript
        ↓
Chunks with timestamps
        ↓
Embeddings
        ↓
Vector search filtered by video ID
        ↓
LangChain prompt
        ↓
Answer with timestamp sources
        ↓
Chrome Extension UI
```
