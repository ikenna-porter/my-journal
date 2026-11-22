---
type: Decision
title: "Backend: Python + FastAPI"
description: The backend will be rewritten in Python with FastAPI, replacing the current Express server once planning is finished.
tags: [decision, backend, python]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T17:33:14Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# Decision

The backend will be written in **Python** using **FastAPI**. It will fully replace the current Express + TypeScript server.[^ike-2026-11-22]

# Timing

The rewrite happens **after planning is complete**, not right away. Until then the existing Express code stays in the repo as-is.

# Why

* The AI tools under consideration are Python-first or Python-only: LangGraph, DeepEval, Ragas and Pydantic. See the [AI engineering stack brainstorm](../brainstorming/ai-engineering-stack.md).
* One backend language is simpler to run than a TypeScript API plus a separate Python AI service.
* Ike is strengthening Python and backend fundamentals, which is a goal of the project in its own right.
* The existing Express code is mostly stubs, so replacing it costs little. See [Current state](../architecture/current-state.md).

# Open questions

* ~~Will Prisma be replaced?~~ Decided: SQLAlchemy 2.0 + Alembic. See [Database access](database-access.md).
* ~~Should the Postgres host stay the same?~~ Decided: Postgres + pgvector self-hosted on the VPS. See [Hosting](hosting.md).

[^ike-2026-11-22]: Ike: "it should be in python. Fast API is fine. so we should eventually replace the current BE with the python one... once we finish planning everything out."
