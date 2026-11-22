---
type: PRD
title: "PRD v1: AI-Powered Multimodal Journaling App"
description: Product requirements for v1, the source of truth for features and user flows (Observation Mode, Conversation Mode, Collaborative Reflection). v1 is text-only; media is v2.
tags: [prd, v1, product]
status: stable
generated:
  by: human:ike
  at: "2026-11-22T18:47:12Z"
  x-myjournal-originally-written: "2026-07-16T01:41:26Z"
  x-myjournal-updated-by: claude-code/claude-opus-5-5
sources:
  - id: prd-commits
    resource: https://github.com/ikenna-porter/my-journal/commits/main/docs/prd/PRD.md
    author: human:ike
    title: PRD commits 8e909d7 and 070fd3b, 2026-07-15
---

> **Precedence.** The decision docs in [`../decisions/`](../decisions/) override this PRD. This PRD is kept in sync with them, and each updated section links to its decision. Terms follow the [Glossary](glossary.md). The sprint dates in section 7 are historical. See [Doc precedence](../decisions/doc-precedence.md).

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

## 3. User Stories

| # | As a user, I want to... | So that... |
|---|---|---|
| 1 | Write free-form journal entries in Markdown without AI interruption | I can capture my thoughts honestly and privately |
| 2 | Attach voice notes to my entries **(v2)** | I can record thoughts when typing feels unnatural |
| 3 | Attach photos to my entries **(v2)** | I can document experiences visually alongside my written thoughts |
| 4 | Have the AI surface meaningful observations after I write | I can discover connections to my past thoughts without searching for them myself |
| 5 | Have my journal data encrypted and accessible only to me | I can write honestly without fear of exposure |
| 6 | Initiate a conversation with the AI grounded in my full journal history | I can explore my thoughts deeply with context the AI has built up over time |
| 7 | Close each AI conversation with a Collaborative Reflection | I have a permanent, distilled record of what was discussed and concluded |
| 8 | Choose whether I or the AI writes the Collaborative Reflection | I retain authorship and control over what gets permanently saved |
| 9 | Provide thumbs up/down feedback on AI observations | The system improves its relevance to me over time |
| 10 | Search my past entries by meaning rather than keywords | I can find relevant entries even when I don't remember the exact words I used |
| 11 | Delete an entry and everything derived from it | I can trust that what I remove is really gone |
| 12 | Skip any AI feature | The journal is still fully useful when I just want to write |

---

## 4. Features & User Flows

### 3.1 Journal Entry Composition
- Users write free-form entries in **Markdown**
- No AI presence, suggestions, or interruptions during writing
- **v1 entries are text only.** Attachments move to v2 ([decision](../decisions/media-deferred-to-v2.md)):
  - **Voice notes (v2)** — transcribed automatically via open-source Whisper (self-hosted, zero per-call cost)
  - **Photos (v2)** — attached and displayed (AI vision also v2)
- Optional metadata: mood/energy tag, timestamp (auto-set; the user can change it **while writing**, for example to backdate, but it's fixed once saved — [decision](../decisions/entry-immutability-and-deletion.md))
- Entries are saved to **PostgreSQL** as the source of truth
- **Entries are immutable.** Once saved, an entry can't be edited, only deleted ([decision](../decisions/entry-immutability-and-deletion.md))
- **Deleting an entry cascades.** It removes the entry's chunks and embeddings, its reflections, reflections on other entries that cite it, observations that cited it, and conversation transcripts and traces that retrieved it. Nothing new is ever generated from deleted text ([decision](../decisions/entry-immutability-and-deletion.md))

### 3.2 Observation Mode (Automatic)
- Triggered silently after the user saves an entry
- The AI processes the entry through the ingestion pipeline asynchronously
- Retrieval finds past chunks **similar** to the new entry. If the top retrieval score exceeds the **confidence threshold**, the AI surfaces **one observation** ([decision](../decisions/observation-mode.md))
- An observation is a **single message of about 5 sentences or fewer**. The LLM reasons over the retrieved chunks and surfaces evolution, stagnation, improvement or contradiction, not just similarity, and **cites and links** the past entries it draws on
- Observations are framed as **opening lines** — invitations to explore, not conclusions
- Not every entry triggers an observation — silence is the default
- Users can provide thumbs up/down feedback on each observation
- Observations are optional and can be ignored ([decision](../decisions/ai-features-optional.md))
- If the user responds to an observation, that starts an **Observation Reply** in Conversation Mode — the observation and user response are carried into the conversation as opening context

### 3.3 Conversation Mode (User-Initiated)
- User can initiate a conversation at any time after writing. Every conversation is **about the entry just written** ([decision](../decisions/conversation-entry-points.md))
- Two entry points:
  - **Observation Reply:** User responds to an observation — the observation becomes opening context
  - **Direct Conversation:** User starts a conversation about the new entry without an observation
- In both, the agent retrieves chunks related to the new entry and summarizes them with links to their entries, so the user can see how their thinking has evolved, stagnated or improved
- The AI is fully informed by the user's journal history throughout the conversation via RAG retrieval
- Retrieval uses deeper context than observation mode (more chunks, broader time range)
- Open-ended conversations not tied to an entry are out of scope
- The **conversation transcript** is stored separately from the journal, never shown in it or retrieved, and **deleted after 30 days** (or right away if its entry is deleted). Langfuse traces follow the same retention. The Collaborative Reflection (see 3.4) is the permanent record ([decision](../decisions/conversation-transcript-retention.md))

### 3.4 Collaborative Reflection
- Closes each conversation. **Optional**: if the user leaves without one, nothing is saved ([decision](../decisions/ai-features-optional.md))
- Records which entries it cites, so deleting a cited entry also deletes the reflection
- A **summary** of the conversation — not the full transcript — written by either the **user** or the **AI** (user decides in the moment)
- Appended to the journal entry permanently in PostgreSQL
- Gets chunked and embedded into pgvector, tagged in metadata as AI-assisted content
- AI-assisted tag allows the retrieval layer to treat reflections differently from raw entries — weighted lower in observation mode, fully available in conversation mode — preventing the AI from creating a feedback loop by referencing its own previous outputs

---

## 4. Technical Architecture

### 4.1 Ingestion Pipeline (Async)
1. User saves entry → stored in **PostgreSQL** → success confirmation returned to UI immediately
2. Job added to **message queue** (RabbitMQ, with Celery workers — [decision](../decisions/job-queue.md))
3. BE worker picks up job → performs chunking internally
4. Chunks sent to **sentence-transformers** → vectors returned
5. Vectors stored in **pgvector** with chunk ID referencing PostgreSQL record
6. Worker acknowledges job completion to queue
7. Failed jobs retry up to **3 times** before failing gracefully

### 4.2 Retrieval Strategy
- **Hybrid retrieval:** keyword (full-text) search + semantic similarity search, merged with reciprocal rank fusion, then reranked, plus metadata filtering (timestamp, mood, entry type). The full pipeline ships in v1 ([decision](../decisions/retrieval-pipeline.md))
- Every query is scoped to the current user ([decision](../decisions/tenancy.md))
- Two retrieval modes:
  - **Observation mode** — fewer chunks, recent entries weighted, automatic
  - **Conversation mode** — more chunks, broader time range, user-initiated
- Confidence threshold: observations only surface when the highest similarity score exceeds a defined minimum threshold (tunable)
- Similarity scores stored in PostgreSQL for analysis and threshold tuning over time

### 4.3 Chunking Strategy
- Entries chunked by paragraph boundaries as primary split
- Semantic chunking applied: adjacent paragraphs with high similarity scores are merged into a single chunk
- Chunking logic lives entirely in the BE worker — no external chunking service
- In v2, voice note transcripts will flow through the same chunking pipeline as text entries

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
| VPS local storage | Photos and audio files (**v2**; not needed in v1) — migrate to Cloudflare R2 when user base grows |

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
- All journal data **encrypted at rest**: disk-level and database-level encryption, not per-user encryption in the app ([decision](../decisions/encryption-at-rest.md))
- All client-server communication over **HTTPS** (TLS)
- **User authentication** required — users can only access their own entries
- **Multi-tenant from day one:** v1 serves Ike and a few other people, but all data and every retrieval query are scoped by user ([decision](../decisions/tenancy.md))
- Journal entries pass through the chosen LLM API for observations and conversation — third party data exposure acknowledged and deferred to v2 for mitigation

### 5.3 Data Format
- All journal entries written and stored in **Markdown** format
- Entries stored in PostgreSQL as the source of truth

### 5.4 Media
- **v1 is text only.** Voice notes and photos move to v2 ([decision](../decisions/media-deferred-to-v2.md))
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
- Voice notes and photo attachments (moved to v2)
- Application logging infrastructure
- LLM data privacy mitigations
- User engagement analytics
- Kubernetes / container orchestration
- Multi-user **scale** infrastructure (high-load infrastructure only; the app itself supports multiple users)
- Editing entries after they're saved
- Open-ended conversations not tied to an entry
- Markdown import / export functionality

---

## 7. Roadmap & Sprints

Planning period: July 15 – July 20
Target completion: late August 2026
Sprint duration: ~2 weeks each

### Sprint 1 — Foundation (July 20 – August 3)
Goal: A working journaling app with no AI. By end of sprint, entries can be written, saved, and retrieved.

- Project setup — VPS provisioning, repo, CI/CD pipeline
- Database setup — PostgreSQL with pgvector extension, schema migrations
- User authentication — registration, login, session management, encryption at rest
- Journal entry composition — Markdown editor, mood/energy tag, timestamp
- Entry save flow — POST endpoint, PostgreSQL persistence, sub-500ms confirmation
- Async ingestion pipeline — message queue setup, BE worker, chunking logic, sentence-transformers embeddings, vector storage in pgvector
- Basic semantic search — embed a query, retrieve nearest chunks from pgvector

### Sprint 2 — AI Layer (August 3 – August 17)
Goal: The AI is alive. Observations surface, conversations happen, reflections are saved.

- Observation engine — confidence threshold evaluation, similarity score storage, llm_observations table
- Observation UI — surface 1-2 observations post-save, thumbs up/down feedback
- Retrieval events table — log each vector DB query, scores, threshold outcome
- Conversation mode — RAG retrieval pipeline, LLM context injection, real-time response
- Observation Reply and Direct Conversation entry points
- Collaborative Reflection — user or AI writes summary, appended to entry in PostgreSQL, embedded with ai_assisted:true metadata tag
- Integration tests for ingestion and retrieval pipelines

### Sprint 3 — Polish (August 17 – August 26)
Goal: Full v1 feature set. Tests passing, deployed and stable. (Voice and photos moved to v2.)

- HTTPS setup — TLS certificate via Let's Encrypt
- Unit and integration test coverage to ≥ 85%
- End-to-end testing of full user flows
- Performance tuning — confirm 500ms save, 8s observation, 8s conversation targets
- Deployment stability — uptime monitoring, embedding job retry logic confirmed
- Bug fixes and UX polish


---

## 8. Success Metrics

| Metric | Target |
|---|---|
| Entry save confirmation time | < 500ms |
| Observation surface time (post-save) | < 8 seconds ([decision](../decisions/observation-mode.md)) |
| Conversation response time | < 8 seconds |
| Observation thumbs up rate | ≥ 80% |
| System uptime | ≥ 99.5% |
| Test coverage (unit + integration) | ≥ 85% |
| Failed embedding job retries | 3 attempts before graceful failure |

Similarity scores and user feedback stored in PostgreSQL and reviewed periodically to tune confidence threshold and improve retrieval quality over time.