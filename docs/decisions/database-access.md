---
type: Decision
title: Database access - SQLAlchemy 2.0 and Alembic, with raw SQL for retrieval
description: The Python backend uses SQLAlchemy 2.0 for ordinary tables and Alembic for migrations. Retrieval queries (full-text, pgvector, fusion) are hand-written SQL. Prisma is removed along with the Express backend.
tags: [decision, database, backend]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T19:25:00Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# Decision

* **SQLAlchemy 2.0 ORM** for ordinary tables: users, entries, tags, observations, Collaborative Reflections, conversation transcripts, spend records.[^ike-2026-11-22]
* **Hand-written SQL** (run through SQLAlchemy) for retrieval: full-text search, pgvector similarity search and fusion. The SQL behind the hand-built retrieval pipeline stays visible (see [Retrieval pipeline](retrieval-pipeline.md)).
* **Alembic** for schema migrations.
* **pgvector** column support through the `pgvector` Python package's SQLAlchemy integration.
* **Prisma is removed** together with the Express backend (see [Backend: Python + FastAPI](backend-python-fastapi.md)). The existing `schema.prisma` is the starting point for the first Alembic migration.

# Why

SQLAlchemy is the most common Python ORM in job postings. Using raw SQL for retrieval keeps the parts worth learning visible, while the ORM avoids boilerplate for basic CRUD.

[^ike-2026-11-22]: Ike accepted SQLAlchemy 2.0 + Alembic ("yes that works") over SQLModel and plain psycopg.
