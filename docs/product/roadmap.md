---
type: Roadmap
title: v1 roadmap - API contract, then vertical slices
description: The build order for v1. Slice 0 designs the API contract, then five vertical slices are built end to end. Each slice lists its hands-on score, the AI engineering skills it teaches, and its open questions. Each slice is one OpenSpec change.
tags: [roadmap, v1, slices, planning]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T20:20:00Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# How to use this roadmap

* **Each slice is one OpenSpec change.** Plan it with the `openspec-propose` skill, build it with `openspec-apply-change`, and archive it when it's done. Start the next slice only when the current one passes its end-to-end tests.
* Every slice follows the [development methodology](../decisions/development-methodology.md): the contract comes first, all code is test-driven, and every task gets a 1 to 5 hands-on score (with "learn, then hand off" at 4 and 5).
* What the app does is defined in the [PRD](prd.md) and the [decision records](../decisions/). Use the terms in the [Glossary](glossary.md).
* **The main goal is AI engineering skill.** The harness (loop engineering), observability and evals come first in every design choice.[^ike-2026-11-22]

```
  [0] API contract
  [1] Entries (foundation) ............ needed, but the least AI-heavy
  [2] Search by meaning ............... RETRIEVAL + EVALS begin
  [3] Direct Conversation ............. THE HARNESS (the centrepiece) + OBSERVABILITY
  [4] Observation Mode ................ fixed workflow vs agent; evals tune the threshold
  [5] Observation Reply +
      Collaborative Reflection ........ harness grows: state, resume, human-in-the-loop
                                        --> LangGraph brought in HERE, where it's needed
```

# Slices

| # | Slice | Score | What you can test end to end | Main skills |
|---|---|---|---|---|
| 0 | API contract | 4 | The OpenAPI spec for every v1 endpoint, the generated TypeScript types, and contract tests that fail until each slice builds its part | API design, Pydantic schemas |
| 1 | Entries | 3 | Log in with Auth0, write an entry (timestamp editable only while writing), list and read entries, delete one | Schema and migrations, auth, per-user scoping, the deletion cascade |
| 2 | Search by meaning | 5 | Save entries, search them by meaning, get relevant entries back with links | **Retrieval**: chunking, full-text + pgvector, RRF, the reranker. **Evals**: golden dataset, retrieval metrics, the CI gate |
| 3 | Direct Conversation | 5 | Start a conversation about the new entry and get cited summaries of related past entries | **Loop engineering**: the hand-built loop, tools, stopping conditions, budgets, the spend limit, retries, streaming, context growth. **Observability**: Langfuse spans for everything. **Agent evals** |
| 4 | Observation Mode | 4 | Save an entry and get an observation (or silence) within 8 seconds, then rate it | **When not to use an agent**: a fixed pass. Threshold tuning with evals, LLM-as-judge on live traces |
| 5 | Observation Reply + Collaborative Reflection | 5 | Reply to an observation, then end the conversation with a reflection written by you or the AI | **Harness state**: resuming within 30 days, human-in-the-loop approval of an AI-drafted reflection. **LangGraph** checkpointer and interrupts. Writes `docs/harness-notes.md` |

## 0. API contract

* **Scope:** every v1 endpoint designed up front, covering request, response, errors and auth: entries, search, observations and feedback, conversations and messages, reflections, deletion. Includes a FastAPI skeleton whose stub endpoints match the spec, TypeScript types generated from the OpenAPI schema, and contract tests.
* **Brings in:** the FastAPI project, Pydantic schemas, OpenAPI type generation for React.
* **Open:** how the OpenSpec config encodes the methodology rules (see [Development methodology](../decisions/development-methodology.md)); streaming format for conversation responses (for example server-sent events).

## 1. Entries

* **Scope:** Docker Compose setup (Postgres + pgvector), SQLAlchemy models and the first Alembic migration (based on the old Prisma schema), Auth0 login, creating, listing, reading and deleting entries, a React app with an editor. This replaces the Express backend and Prisma.
* **Cross-cutting start:** deletion of an entry. Later slices extend it.
* **Open:** login methods; frontend and backend session handling.

## 2. Search by meaning

* **Scope:** RabbitMQ + Celery, the `ingest_entry` task (chunking, embeddings with `all-mpnet-base-v2`, storage in pgvector), the full retrieval pipeline (see [Retrieval pipeline](../decisions/retrieval-pipeline.md)), a search UI that links results to their entries.
* **Evals begin:** a synthetic test journal (never real entries), golden queries, retrieval metrics (context precision and recall), DeepEval runner, GitHub Actions gate. Add pipeline steps one at a time and record each step's before/after numbers in `docs/`.
* **Open:** what happens if the entry saves but enqueueing the job fails (see [Job queue](../decisions/job-queue.md)); the exact reranker model; whether eval runs share the $50 spend limit.

## 3. Direct Conversation

* **Scope:** the hand-built agent loop on the Anthropic SDK (see [Agent harness](../decisions/agent-harness.md)), a `search_entries` tool, cited answers, streaming to the UI, conversation transcripts with 30-day expiry, the monthly spend limit (see [LLM](../decisions/llm-model-and-spend-limit.md)).
* **Observability:** self-hosted Langfuse, with nested spans for each loop iteration, model call, tool call and retrieval step, plus cost, latency, stop reason and 30-day trace retention.
* **Evals:** tool selection, task completion, faithfulness, citation correctness, "I don't know" when the journal has no answer.
* **Cross-cutting:** deletion also removes transcripts and traces that retrieved the entry.

## 4. Observation Mode

* **Scope:** after an entry is saved, a fixed retrieve-then-generate pass, gated by the confidence threshold, returns one observation of about 5 sentences with citations within 8 seconds. Includes thumbs up/down feedback, `llm_observations` and `retrieval_events` storage (see [Observation Mode](../decisions/observation-mode.md)).
* **Evals:** threshold tuning (with the reranker on and off), observation quality, LLM-as-judge scoring of sampled live traces in Langfuse.
* **Cross-cutting:** deletion also removes observations that cited the entry.

## 5. Observation Reply + Collaborative Reflection

* **Scope:** replying to an observation starts a conversation (see [Conversation entry points](../decisions/conversation-entry-points.md)). Ending a conversation offers an optional Collaborative Reflection written by the user or drafted by the AI and approved by the user. Reflections are embedded with `ai_assisted: true` and record which entries they cite. Conversations can be resumed within 30 days.
* **LangGraph:** brought in to solve state, resuming and human-in-the-loop with your own nodes (see [Agent harness](../decisions/agent-harness.md)). `docs/harness-notes.md` compares it with the hand-built loop: what it made easier and what it hid.
* **Cross-cutting:** deletion also removes reflections that cite the entry.

# Cross-cutting rules

* **The deletion cascade grows with each slice.** Each slice extends delete to cover what it adds, and its tests prove it (see [Entry deletion](../decisions/entry-immutability-and-deletion.md)).
* **The eval CI gate grows with each AI slice**, starting in slice 2.
* **Every query is scoped to the user** (see [Tenancy](../decisions/tenancy.md)).
* **Components stay separable** (see [Hosting](../decisions/hosting.md)).
* After each slice, update the README with what was built, how to run it and the current eval scores. This doubles as portfolio material and blog material.

# After v1

Voice notes and photos ([v2](../decisions/media-deferred-to-v2.md)), guardrails, an MCP server for the journal tools, and production deployment hardening.

[^ike-2026-11-22]: Ike: "i want to develop the harness myself (and use langgraph where necessary)... this part of the project is perhaps the most important part. the observability part is also important. so is the eval part... skills relevant to that end should be at the forefront of this design."
