---
okf_version: "0.3"
title: my-journal documentation
description: Architecture, decisions and planning notes for my-journal, a journaling app with an AI (RAG + agent) layer over the user's own entries.
---

# Product

* [PRD v1](product/prd.md) - Product requirements for v1, the source of truth for features and user flows (Observation Mode, Conversation Mode, Collaborative Reflection). v1 is text-only; media is v2.
* [Glossary](product/glossary.md) - The canonical product vocabulary. Every doc, spec, UI label and code identifier uses these terms and no synonyms.

# Architecture

* [Current state of the codebase](architecture/current-state.md) - A snapshot of what exists in the repo today, written before the planned Python backend rewrite.
* [Entry save and ingestion sequence](architecture/entry-save-sequence.md) - How saving a journal entry flows from the UI to Postgres, then asynchronously through the queue, chunking, embedding and vector storage.

# Decisions

* [Doc precedence](decisions/doc-precedence.md) - Decision docs override the PRD, and the PRD is kept in sync with them. Brainstorms are never authoritative.

## Product decisions

* [Observation Mode - how observations work](decisions/observation-mode.md) - Retrieval finds similar past chunks, and the LLM turns them into a single observation of about 5 sentences, with citations, within 8 seconds.
* [Conversation Mode entry points - Observation Reply and Direct Conversation](decisions/conversation-entry-points.md) - Conversation Mode has two entry points, and both are about the entry just written. In an Observation Reply the user responds to an observation; in a Direct Conversation the user starts one without an observation.
* [AI features are optional](decisions/ai-features-optional.md) - Every AI feature (observations, conversations, Collaborative Reflections) can be skipped, and the journal works fully without them.
* [Entries are immutable, and deletion cascades](decisions/entry-immutability-and-deletion.md) - Entries can't be edited, only deleted. Deleting an entry removes its chunks and embeddings plus every reflection, observation, transcript and trace that references it.
* [Conversation transcripts are kept separately for 30 days](decisions/conversation-transcript-retention.md) - Conversation transcripts are stored apart from the journal, never shown in it or retrieved, and deleted after 30 days. Langfuse traces follow the same retention. Reflections are kept permanently.
* [Voice notes and photos move to v2](decisions/media-deferred-to-v2.md) - v1 is text-only. Voice notes (Whisper transcription) and photo attachments move to v2, so v1 focuses on writing, observations and conversations.
* [Encryption at rest means disk and database encryption](decisions/encryption-at-rest.md) - In v1, "encrypted at rest" means disk-level and database-level encryption plus strict per-user access scoping, not per-user application-level encryption.
* [Multi-tenant from day one, few users at first](decisions/tenancy.md) - v1 serves Ike and a few other people, but every table and query is scoped by user so the app can grow to many tenants.

## Tech decisions

* [Backend: Python + FastAPI](decisions/backend-python-fastapi.md) - The backend will be rewritten in Python with FastAPI, replacing the current Express server once planning is finished.
* [Frontend: React + TypeScript](decisions/frontend-react-typescript.md) - The frontend stays in TypeScript and uses React.
* [Build it yourself vs use a library](decisions/build-vs-library.md) - Which AI components are hand-built for learning and job-search value, and which come from frameworks or libraries.
* [Agent harness - own nodes on the LangGraph runtime](decisions/agent-harness.md) - The agent loop is built by hand first, then its functions run as nodes in a LangGraph graph. LangGraph's prebuilt agents are not used.
* [Retrieval pipeline - full pipeline in v1, hand-built](decisions/retrieval-pipeline.md) - v1 ships the complete hand-built retrieval pipeline (chunking, keyword + vector search, RRF fusion, reranking, date filters), and each step is measured with evals as it's added.

* [LLM - Claude via the Anthropic SDK, model and spend limit set by environment variables](decisions/llm-model-and-spend-limit.md) - Claude is called directly through the Anthropic SDK. The model is chosen by an environment variable (Claude Opus 5.5 for now), and a monthly spend limit in another environment variable ($50) blocks every LLM call once it's reached.
* [Database access - SQLAlchemy 2.0 and Alembic, with raw SQL for retrieval](decisions/database-access.md) - The Python backend uses SQLAlchemy 2.0 for ordinary tables and Alembic for migrations. Retrieval queries (full-text, pgvector, fusion) are hand-written SQL. Prisma is removed along with the Express backend.
* [Authentication - Auth0](decisions/authentication.md) - Login is handled by Auth0, a hosted auth service, chosen for its ease and resume recognition. Its free tier (about 25K MAU) far exceeds v1's needs.
* [Job queue - Celery with RabbitMQ](decisions/job-queue.md) - Background jobs such as entry ingestion run as Celery tasks, with RabbitMQ as the broker. It runs on the VPS and can move to its own machine later.
* [Hosting - one larger Hetzner VPS for everything](decisions/hosting.md) - For now the app, Postgres, the local models, the agent runtime and self-hosted Langfuse all run on one larger Hetzner VPS. There is no AWS or managed cloud.

## Process decisions

* [Documentation format: Open Knowledge Format](decisions/documentation-okf.md) - All docs in this directory follow Google's Open Knowledge Format (OKF) v0.3.
* [Planning workflow: OpenSpec](decisions/planning-openspec.md) - Features are planned as OpenSpec changes (proposal, design, specs, tasks) before implementation.

# Brainstorming

* [AI engineering stack (brainstorm)](brainstorming/ai-engineering-stack.md) - Candidate tools for the AI layer (LangGraph, pgvector, Langfuse, DeepEval and others). Draft only, nothing here is final.
