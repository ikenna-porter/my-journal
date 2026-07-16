# my-journal

An AI-powered multimodal journaling app that surfaces meaningful connections, patterns, and contradictions across your personal history.

Traditional journaling apps are static archives — they store entries but offer no intelligence on top of them. This app adds an AI layer that grounds every insight in your actual journal history via RAG, not general knowledge.

---

## Features

### Journal Entry Composition
- Free-form Markdown entries — no AI presence or interruptions during writing
- Attach voice notes (auto-transcribed via self-hosted Whisper) and photos
- Optional mood/energy tags and editable timestamps
- Entries stored in PostgreSQL as the source of truth

### Observation Mode (Automatic)
- Triggered silently after saving an entry
- AI surfaces 1-2 observations only when similarity scores exceed a confidence threshold — silence is the default
- Observations are framed as opening lines, not conclusions
- Thumbs up/down feedback used to tune the threshold over time

### Conversation Mode (User-Initiated)
- Always optional, always user-initiated
- Entry points: respond to an AI observation (Path A) or start fresh (Path B)
- Fully informed by your journal history via RAG throughout the conversation
- Raw transcript is not persisted — only a Collaborative Reflection is saved

### Collaborative Reflection
- A summary of each conversation session, written by you or the AI
- Appended permanently to the journal entry
- Tagged as AI-assisted in metadata so the retrieval layer can weight it appropriately, preventing feedback loops

---

## Architecture

### Stack
| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Node.js, TypeScript |
| Database | PostgreSQL + pgvector |
| Embeddings | sentence-transformers (`all-mpnet-base-v2`) — self-hosted, zero per-call cost |
| Voice transcription | Whisper — self-hosted |
| Infrastructure | Single VPS (e.g. Hetzner) |

### Ingestion Pipeline (Async)
1. Entry saved → PostgreSQL → success confirmation returned to UI immediately
2. Job queued → BE worker picks it up
3. Entry chunked by paragraph boundaries; adjacent high-similarity paragraphs merged
4. Chunks embedded via sentence-transformers → vectors stored in pgvector
5. Failed jobs retry up to 3 times before failing gracefully

### Retrieval Strategy
- Hybrid: semantic similarity search + metadata filtering (timestamp, mood, entry type)
- Observation mode — fewer chunks, recent entries weighted
- Conversation mode — more chunks, broader time range
- Similarity scores stored in PostgreSQL for threshold tuning over time

---

## Roadmap

**Phase 1 — Foundation**
Write entries, store in PostgreSQL, basic semantic search with pgvector, sentence-transformers embeddings, async ingestion pipeline.

**Phase 2 — AI Layer**
Observation engine with confidence threshold, conversation mode with RAG, Collaborative Reflection, thumbs up/down feedback.

**Phase 3 — Media & Insights**
Voice note recording and Whisper transcription, photo attachments, timeline views, topic clustering, sentiment tracking.

---

## Out of Scope (v1)
- Video support
- AI vision / photo understanding
- LLM data privacy mitigations
- Multi-user scale infrastructure
- Markdown import / export

---

## Getting Started

```bash
# Install root dependencies
npm install

# Start the client (Vite dev server)
cd client && npm install && npm run dev

# Start the server
cd server && npm install && npm run dev
```

Requires a PostgreSQL instance with the pgvector extension enabled.
