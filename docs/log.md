# Directory Update Log

## 2026-11-22

* **Created**: Root `CLAUDE.md` with working rules for every session (read-first list, precedence, vocabulary, methodology, privacy, git).
* **Created**: `product/roadmap.md`, covering the API contract and five vertical slices with hands-on scores. Added the hands-on scale and the learn-then-hand-off rule to `development-methodology.md`.
* **Update**: Development methodology recorded: contract first, vertical slices, TDD, hands-on scores (new decision `development-methodology.md`).
* **Update**: Authentication changed from WorkOS AuthKit to Auth0, for resume recognition (authentication).
* **Update**: Authentication decided: a hosted provider with the largest free tier, WorkOS AuthKit (new decision `authentication.md`).
* **Update**: Database access decided: SQLAlchemy 2.0 + Alembic, with raw SQL for retrieval (new decision `database-access.md`).
* **Update**: Job queue decided: Celery with RabbitMQ (new decision `job-queue.md`, PRD 4.1). The open question of saving an entry and queuing its job in two systems is recorded there.
* **Update**: The observation latency budget is 8 seconds; the 5-second target was removed (observation-mode, PRD sections 7 and 8, index, retrieval-pipeline).
* **Update**: Reranker runs locally on the VPS behind a config switch (retrieval-pipeline). Added the rule to keep components separable (hosting).
* **Update**: The spend limit resets each calendar month.
* **Update**: LLM decided: Claude via the Anthropic SDK, model and $50 spend limit set by environment variables (new decision `llm-model-and-spend-limit.md`).
* **Update**: Hosting decided: one larger Hetzner VPS for everything (new decision `hosting.md`).
* **Update**: Defined "encrypted at rest" as disk and database encryption (new decision `encryption-at-rest.md`, PRD 5.2).
* **Update**: The entry timestamp can be changed only while writing, then is fixed (PRD 3.1, entry-immutability-and-deletion).
* **Update**: Moved voice notes and photos to v2 (new decision `media-deferred-to-v2.md`). Updated PRD user stories 2 and 3 and sections 3.1, 4.3, 4.5, 5.4, 6 and 7, plus the glossary's Entry definition. Confirmed from git history that the user-started mode has always been called Conversation Mode.
* **Update**: Decision docs now override the PRD (doc-precedence rewritten). Updated PRD sections 3.1 to 3.4, 4.2, 5.2, 6, 7 and 8, plus user stories 11 and 12, to match the decisions. Replaced "Path A/B" with **Observation Reply** and **Direct Conversation**. Added `product/glossary.md` as the canonical vocabulary. Renamed `conversation-path-b.md` to `conversation-entry-points.md` and `chat-transcript-retention.md` to `conversation-transcript-retention.md`.
* **Update**: Added nine decision records from the explore session. Product: observation-mode, conversation-path-b, ai-features-optional, entry-immutability-and-deletion, chat-transcript-retention, tenancy. Tech: build-vs-library, agent-harness, retrieval-pipeline. Grouped the decisions in `index.md`.
* **Fix**: Pulled the July 2026 commits that had been missed (PRD, sequence diagram, README). Moved the PRD to `product/prd.md` and added an OKF header and a precedence note. Converted `sequence-diagram.mmd` into `architecture/entry-save-sequence.md`. Added the doc-precedence decision. Corrected the current-state snapshot and the brainstorm banner.
* **Update**: Installed OpenSpec globally and initialized `openspec/` in the repo. Updated the setup status in the OpenSpec decision doc.
* **Created**: Started the docs bundle in Open Knowledge Format v0.3 with a root index, a current-state architecture snapshot, four decision records and the AI engineering stack brainstorm (imported from a handoff doc).
