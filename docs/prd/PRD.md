# Product Requirements Document
## AI-Powered Multimodal Journaling App
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** July 2026

---

## 1. Problem Statement

Users have no reliable way to track, trace, and understand the evolution of their own thoughts, opinions, and experiences over time. Traditional journaling apps are static document archives — they store entries but offer no intelligence on top of them. This app solves that by combining free-form journaling with an AI layer that surfaces meaningful connections, patterns, and contradictions across a user's entire personal history.

The app is a multimodal journaling platform that leverages AI to provide users with insights about their previous thoughts and experiences. Insights are delivered in two distinct modes: **Observation Mode** (automatic, AI-initiated) and **Conversation Mode** (user-initiated). All retrieval is powered by **Retrieval-Augmented Generation (RAG)**, grounding every AI response in the user's actual journal history rather than general knowledge.

---

## 2. Core Design Principles

- **AI earns its presence.** The AI is silent during writing and only speaks when it has something meaningful to say.
- **The user is always in control.** Conversation is always optional and user-initiated.
- **Honesty over performance.** The writing experience should feel private and unfiltered — the user should never feel like they are writing for an audience.
- **Retrieval quality is everything.** Without accurate, relevant retrieval, the AI layer has no value. Chunking strategy and similarity scoring are first-class architectural concerns.

---

## 3. Features & User Flows

### 3.1 Journal Entry Composition
- Users write free-form entries in **Markdown**
- No AI presence, suggestions, or interruptions during writing
- Users can attach:
  - **Voice notes** — transcribed automatically via open-source Whisper (self-hosted, zero per-call cost)
  - **Photos** — attached and displayed (AI vision deferred to v2)
- Optional metadata: mood/energy tag, timestamp (auto-set, user-editable)
- Entries are saved to **PostgreSQL** as the source of truth

### 3.2 Observation Mode (Automatic)
- Triggered silently after the user saves an entry
- The AI processes the entry through the ingestion pipeline asynchronously
- If the highest similarity score between the new entry and past entries exceeds the **confidence threshold**, the AI surfaces 1-2 observations immediately after writing
- Observations are framed as **opening lines** — invitations to explore, not conclusions
- Not every entry triggers an observation — silence is the default
- Users can provide thumbs up/down feedback on each observation
- If the user responds to an observation, that response becomes the entry point into Conversation Mode (Path A) — the observation and user response are carried into the conversation as opening context

### 3.3 Conversation Mode (User-Initiated)
- User can initiate a conversation at any time after writing
- Two entry points:
  - **Path A:** User responds to an AI observation — observation becomes opening context
  - **Path B:** User initiates fresh conversation without an observation
- The AI is fully informed by the user's journal history throughout the conversation via RAG retrieval
- Retrieval uses deeper context than observation mode (more chunks, broader time range)
- The raw conversation transcript is not persisted — only the Collaborative Reflection (see 3.4) is saved

### 3.4 Collaborative Reflection
- Closes each conversation session
- A **summary** of the conversation — not the full transcript — written by either the **user** or the **AI** (user decides in the moment)
- Appended to the journal entry permanently in PostgreSQL
- Gets chunked and embedded into pgvector, tagged in metadata as AI-assisted content
- AI-assisted tag allows the retrieval layer to treat reflections differently from raw entries — weighted lower in observation mode, fully available in conversation mode — preventing the AI from creating a feedback loop by referencing its own previous outputs

---

## 4. Technical Architecture

### 4.1 Ingestion Pipeline (Async)
1. User saves entry → stored in **PostgreSQL** → success confirmation returned to UI immediately
2. Job added to **message queue**
3. BE worker picks up job → performs chunking internally
4. Chunks sent to **sentence-transformers** → vectors returned
5. Vectors stored in **pgvector** with chunk ID referencing PostgreSQL record
6. Worker acknowledges job completion to queue
7. Failed jobs retry up to **3 times** before failing gracefully

### 4.2 Retrieval Strategy
- **Hybrid retrieval:** semantic similarity search + metadata filtering (timestamp, mood, entry type)
- Two retrieval modes:
  - **Observation mode** — fewer chunks, recent entries weighted, automatic
  - **Conversation mode** — more chunks, broader time range, user-initiated
- Confidence threshold: observations only surface when the highest similarity score exceeds a defined minimum threshold (tunable)
- Similarity scores stored in PostgreSQL for analysis and threshold tuning over time

### 4.3 Chunking Strategy
- Entries chunked by paragraph boundaries as primary split
- Semantic chunking applied: adjacent paragraphs with high similarity scores are merged into a single chunk
- Chunking logic lives entirely in the BE worker — no external chunking service
- Voice note transcripts flow through the same chunking pipeline as text entries

### 4.4 Embedding Model
- **sentence-transformers** (e.g. `all-mpnet-base-v2`) — open source, runs locally, no per-call cost
- Runs as part of the BE — no separate service or API call required
- No model training required — pre-trained models used out of the box
- Migration path to hosted embedding API available if retrieval quality proves insufficient

### 4.5 Data Storage
| Store | Responsibility |
|---|---|
| PostgreSQL | Entry text, chunk text, metadata, similarity scores, user feedback, AI observations (`llm_observations` table), retrieval events (`retrieval_events` table) |
| pgvector (Postgres extension) | Embeddings (vectors) with chunk IDs |
| VPS local storage | Photos and audio files (v1) — migrate to Cloudflare R2 when user base grows |

### 4.6 User Feedback Loop
- Thumbs up/down on observations stored in PostgreSQL
- Used to tune confidence threshold over time
- Foundation for adaptive retrieval in future versions (v2+)

---

## 5. Constraints & Limitations

### 5.1 Cost
- Self-hosted on a **single VPS** (e.g. Hetzner) — no managed cloud services
- sentence-transformers over hosted embedding APIs — zero per-call embedding cost
- pgvector over hosted vector DB (e.g. Pinecone) — no subscription cost
- Single VPS limitation: not designed for high concurrent load in v1

### 5.2 Privacy & Security
- All journal data **encrypted at rest**
- All client-server communication over **HTTPS** (TLS)
- **User authentication** required — users can only access their own entries
- Journal entries pass through the chosen LLM API for observations and conversation — third party data exposure acknowledged and deferred to v2 for mitigation

### 5.3 Data Format
- All journal entries written and stored in **Markdown** format
- Entries stored in PostgreSQL as the source of truth

### 5.4 Media
- Voice notes and photos supported in v1
- **Video excluded from v1**
- AI vision for photos (image understanding) deferred to v2

### 5.5 AI Behavior
- AI is **silent during writing** — no interruptions
- Observations surface **only when confidence threshold is exceeded**
- Not every entry triggers an observation
- AI conversation is always **optional and user-initiated**

---

## 6. Out of Scope (v1)

- Video support
- AI vision / photo understanding
- Application logging infrastructure
- LLM data privacy mitigations
- User engagement analytics
- Kubernetes / container orchestration
- Multi-user scale infrastructure
- Markdown import / export functionality

---

## 7. Build Phases

### Phase 1 — Foundation
Write entries, store in PostgreSQL, basic semantic search with pgvector, sentence-transformers embeddings, async ingestion pipeline via message queue.

### Phase 2 — AI Layer
Observation engine with confidence threshold, conversation mode with RAG, Collaborative Reflection, thumbs up/down feedback, similarity score storage.

### Phase 3 — Media & Insights
Voice note recording and Whisper transcription, photo attachments, timeline views, topic clustering, sentiment tracking over time.

---

## 8. Success Metrics

| Metric | Target |
|---|---|
| Entry save confirmation time | < 500ms |
| Observation surface time (post-save) | < 5 seconds |
| Conversation response time | < 8 seconds |
| Observation thumbs up rate | ≥ 80% |
| System uptime | ≥ 99.5% |
| Test coverage (unit + integration) | ≥ 85% |
| Failed embedding job retries | 3 attempts before graceful failure |

Similarity scores and user feedback stored in PostgreSQL and reviewed periodically to tune confidence threshold and improve retrieval quality over time.