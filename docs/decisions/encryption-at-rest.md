---
type: Decision
title: Encryption at rest means disk and database encryption
description: In v1, "encrypted at rest" means disk-level and database-level encryption plus strict per-user access scoping, not per-user application-level encryption.
tags: [decision, security, privacy]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T18:47:12Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# Decision

This clarifies the PRD's "all journal data encrypted at rest" ([PRD section 5.2](../product/prd.md)) for v1:[^ike-2026-11-22]

* **Disk and database encryption.** Data on disk and in backups is encrypted, which protects against a stolen disk or a leaked backup.
* **Strict per-user scoping.** Every query is filtered by user (see [Tenancy](tenancy.md)).
* **Not per-user encryption in the app.** The server can read entries.

# Why

Per-user encryption would stop Postgres from searching text or embeddings, which breaks retrieval and every AI feature. The AI must read entries to work, and entry text already goes to the LLM provider (a known v1 trade-off in the PRD).

[^ike-2026-11-22]: Ike chose option 1 (disk and database encryption) over per-user encryption in the app.
