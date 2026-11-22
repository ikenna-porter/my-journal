---
type: Brainstorm
title: AI engineering stack (brainstorm)
description: Candidate tools for the AI layer (LangGraph, pgvector, Langfuse, DeepEval and others). Draft only, nothing here is final.
tags: [brainstorm, ai, rag, agents, observability, evals]
status: draft
generated:
  by: claude/unknown
  at: "2026-11-22T17:33:14Z"
sources:
  - id: handoff
    resource: process:handoff-doc
    author: claude/unknown
    title: "AI Engineering Stack: Handoff for the Journaling App (written by another Claude session)"
---

> **⚠️ BRAINSTORMING DOCUMENT: NOT FINAL.**
> Another AI session wrote this as a handoff, without seeing the repo.[^handoff] Nothing here is decided. Every choice below is a candidate and may change during planning (see [Planning workflow: OpenSpec](../decisions/planning-openspec.md)).
>
> * **What matters most here:** the **tools** Ike wants to learn and use.
> * **Not being followed:** the "Before you start" and "Build order" sections. They're kept only as a record of the original handoff.
> * **The [PRD](../product/prd.md) wins on features.** This doc was written without the PRD, so wherever the two disagree on what the app does, follow the PRD. See [Doc precedence](../decisions/doc-precedence.md).
> * **Already decided:** the backend language, now settled in [Backend: Python + FastAPI](../decisions/backend-python-fastapi.md), and the frontend, settled in [Frontend: React + TypeScript](../decisions/frontend-react-typescript.md).

# Purpose

This document records the technology decisions for the AI layer of the journaling app. The app uses RAG over the user's own journal entries. The project has two goals:

1. Ship a working, production-quality AI feature set for the app.
2. Give the developer (Ike) hands-on experience with the tools AI engineering employers ask for most, especially in London, Berlin, Amsterdam and NYC job postings.

Because of goal 2, **use the named tools, not substitutes**, even where a simpler option exists. Where this doc says "build it yourself first," that is deliberate and is for learning.

# Before you start (Claude Code)

*(Kept for the record; not being followed. See the banner above.)*

The author of this doc has **not seen the repo**. Before making changes:

1. Inspect the repo and summarize the current stack: language, framework, database, how entries are stored, deployment setup and any existing AI code.
2. List every place where the repo conflicts with this doc (for example, the backend isn't Python, or the database isn't Postgres).
3. **Stop and confirm with Ike before** changing the language, framework or database, or adding infrastructure (Docker services, new hosted accounts).
4. Then follow the build order at the end of this doc, one phase at a time, with a short summary after each phase.

Ike is strengthening his Python and backend fundamentals. Prefer clear, readable code over clever code. Explain non-obvious design choices in comments or PR descriptions, especially async code, retries and state handling.

# Core constraint: privacy

Journal entries are highly personal. This drives several decisions below:

* Do not send entry text to third-party services unless it's needed: the LLM provider, and the embedding provider if one is used.
* Observability is **self-hosted** so traces containing entry text stay on infrastructure Ike controls.
* Never log raw entry text to stdout or general application logs. Traces go to Langfuse only.
* Keep secrets in environment variables (`.env`, git-ignored). Never commit keys.

# 1. Harness / orchestration

**Candidate: custom agent loop first (Phase 1), then port to LangGraph (Phase 4).**

Why:

* Building the loop by hand teaches the internals: model call, tool execution, appending results, stopping conditions, error handling.
* LangGraph is the agent framework employers name most often, so the app should end up on it.
* Porting from a custom loop to LangGraph shows clearly what the framework handles: state, checkpointing, retries, human-in-the-loop.

Phase 1 requirements (custom loop):

* Plain Python on the model provider's official SDK. Default to the Anthropic SDK (Claude) unless the repo already uses another provider.
* Explicit loop: send messages and tool definitions → if the model requests tools, run them → append the results → repeat.
* Stopping conditions: final answer, max iterations (configurable, default about 8), token/cost budget, unrecoverable error.
* Tool calls are validated with Pydantic before running. Tool errors go back to the model as tool results, not as crashes.
* Structured outputs are validated with Pydantic schemas.
* Keep it small, roughly a few hundred lines, with a clear module boundary (for example `agent/loop.py`, `agent/tools.py`) so it can be swapped for LangGraph later.

Phase 4 requirements (LangGraph port):

* Recreate the same behavior as a LangGraph graph. Add persistent state through a checkpointer (Postgres-backed if possible) and at least one human-in-the-loop checkpoint where it makes sense.
* Keep the Phase 1 loop in the repo (or in git history with a tag) for comparison.
* Write a short `docs/harness-notes.md` comparing the two: what LangGraph made easier, and what it hid.

Optional, later: expose the journal tools (search entries, get entry by date, list themes) through an **MCP server** so other clients, such as Claude Desktop, can use them.

# 2. RAG

**Candidate: Postgres + pgvector, with hybrid search and a reranker.**

Why: Postgres + pgvector came up most often in job postings, and keeping vectors next to the entry data in one database is simpler to run.

Requirements:

* **Storage:** the `pgvector` extension in the app's Postgres. A chunks table that references the entry, with at least: `entry_id`, `chunk_text`, `embedding`, `entry_date`, `chunk_index`, plus any existing tags or mood fields as metadata.
* **Index:** HNSW index on the embedding column.
* **Chunking:** most journal entries are short. Keep short entries as one chunk. Split long entries on paragraph boundaries with a little overlap. Always keep entry date and metadata on each chunk.
* **Embeddings:** put the provider behind a small interface so it can be swapped. Hosted default: OpenAI `text-embedding-3-small`. For privacy, an open-source local model (for example a BGE model via `sentence-transformers`) is also acceptable. Ask Ike which he prefers, and record the choice in this doc.
* **Hybrid search:** combine Postgres full-text search (`tsvector`) with vector similarity using reciprocal rank fusion (RRF).
* **Reranking:** rerank the top candidates (for example the top 30 down to the top 5) with a cross-encoder reranker. Cohere Rerank (hosted) or an open BGE reranker (local). Same swap-friendly interface as embeddings.
* **Date-aware retrieval:** support filters like "entries from last March" through metadata filters, not embeddings alone.
* **Citations:** every answer must cite the entries it used (entry id and date), and the UI should be able to link to them.
* **Ingestion:** re-embed an entry whenever it's created or edited. Never leave stale vectors behind.

# 3. Observability / tracing

**Candidate: Langfuse, self-hosted, with OpenTelemetry-compatible instrumentation.**

Why: Langfuse is the most widely used open-source LLM observability platform and was named in target job postings. The self-hosted open-source edition is free with no usage limits, and self-hosting keeps journal text private.

Requirements:

* Run Langfuse locally with its official Docker Compose setup for development. Production hosting is TBD with Ike. Don't create a hosted account without asking.
* Use one Langfuse instance for both development and production. Tag every trace with `environment` (`dev` / `prod`) and a release or version string.
* Trace the full pipeline as nested spans: request → retrieval (full-text search, vector search, fusion, rerank) → each model call → each tool call → final answer.
* Record on each trace: model name, input/output tokens, cost, latency, number of retrieved chunks and their ids, loop iteration count, stop reason.
* Prompts live in version control (or Langfuse prompt management) with a version id attached to traces.
* Add a simple user feedback hook (thumbs up/down) that writes a score to the trace.

# 4. Evals

**Candidate: DeepEval as the test runner and CI gate, with RAG-specific metrics in the Ragas style, plus online scoring in Langfuse.**

Why: DeepEval is among the most-downloaded eval frameworks and supports CI gating natively (`deepeval test run`). Ragas-style metrics are the standard way to measure RAG quality. Langfuse covers scoring of live traffic.

Requirements:

* **Golden dataset:** create `evals/datasets/` with about 30 to 50 question/answer cases built from a **synthetic or test journal**, never Ike's real entries. Cover: simple lookup, date-filtered questions, theme questions across many entries, questions with no answer in the journal (the app must say so, not make one up), and multi-step questions that need tools.
* **Retrieval metrics:** context precision and context recall against labeled relevant entries.
* **Generation metrics:** faithfulness/groundedness to the retrieved entries, answer relevancy, and citation correctness (cited entries actually support the answer).
* **Agent metrics:** task completion, correct tool selection, number of loop iterations.
* **CI:** a GitHub Actions workflow runs the eval suite on pull requests and **fails the build** if key metrics drop below thresholds. Store thresholds in config, start them modestly and tighten over time.
* **Online evals:** score a sample of production traces in Langfuse with LLM-as-judge for faithfulness.
* Keep eval cost visible. Use a cheaper judge model where quality allows, and record the eval run cost.

# 5. Guardrails

**Candidate: deferred.** Don't add a guardrails library yet.

Leave clear hook points in the pipeline (pre-model input check, post-model output check, pre-tool-call check) so guardrails can be added later without a rewrite. Expected later candidates: Microsoft Presidio for PII, a prompt-injection classifier, and schema validation of outputs. Since this is a journaling app, a later phase should also include careful handling of entries or questions that touch on mental health crises. Don't build this now, but don't design anything that makes it hard to add.

# 6. Supporting stack

* **Language:** Python for the AI layer. *(Now decided for the whole backend; see [Backend: Python + FastAPI](../decisions/backend-python-fastapi.md).)*
* **API:** FastAPI. *(Decided, same doc.)*
* **Validation:** Pydantic everywhere: tool inputs, structured outputs, config.
* **Containers:** Docker Compose for local Postgres + pgvector and Langfuse.
* **CI:** GitHub Actions for tests, lint and eval gating.
* **Config:** environment variables for model names, thresholds, budgets and provider choices, so nothing is hard-coded.

# Build order

*(Kept for the record; **not being followed**. Sequencing will come out of OpenSpec planning.)*

1. **Phase 0, survey:** inspect the repo and report conflicts with this doc (see "Before you start").
2. **Phase 1, minimal end to end:** ingestion → pgvector (vector search only) → custom agent loop with one search tool → answer with citations.
3. **Phase 2, observability:** self-hosted Langfuse, full nested tracing, environment tags, cost and latency recorded.
4. **Phase 3, evals:** synthetic test journal, golden dataset, DeepEval suite, CI gate.
5. **Phase 3b, better retrieval:** add hybrid search, RRF and reranking. Use the eval suite to show the before/after improvement, and record the numbers in `docs/`.
6. **Phase 4, LangGraph port:** same behavior on LangGraph with a checkpointer. Write `docs/harness-notes.md`.
7. **Later:** MCP server for journal tools, guardrails, production deployment.

After each phase, update the README with what was built, how to run it locally, and current eval scores. These records double as portfolio material.

# Open questions for Ike

* Embedding and reranking: hosted (OpenAI/Cohere) or local open-source models?
* Where will production run, and will Langfuse be hosted next to it?
* Is the app single-user (just Ike) or multi-user? This affects data isolation and auth in retrieval.
* Which AI features should the app have first: Q&A over entries, periodic reflections or summaries, theme or pattern detection?

[^handoff]: Handoff doc pasted into a Claude Code session by Ike on 2026-11-22. Its original author was a separate Claude session, model unknown.
