---
type: Sequence Diagram
title: Entry save and ingestion sequence
description: How saving a journal entry flows from the UI to Postgres, then asynchronously through the queue, chunking, embedding and vector storage.
tags: [architecture, ingestion, sequence-diagram]
status: stable
generated:
  by: human:ike
  at: "2026-07-15T11:55:47Z"
sources:
  - id: diagram-commits
    resource: https://github.com/ikenna-porter/my-journal/commits/main/docs/sequence-diagram.mmd
    author: human:ike
    title: Sequence diagram commits 75dc29c and 073c944, 2026-07-14 to 2026-07-15
---

# Overview

This diagram shows the ingestion pipeline described in the [PRD, section 4.1](../product/prd.md). The entry is saved and confirmed to the user right away. Chunking and embedding happen afterwards in a worker that takes its jobs from a message queue.[^diagram-commits]

In the PRD, the "Vector Database" is pgvector inside the same Postgres instance. The diagram shows it as a separate participant only to make the steps clearer.

# Diagram

```mermaid
sequenceDiagram
actor User
participant UI
participant BE
participant PG as Postgres
participant MQ as MessageQueue
participant EM as Embedding Model
participant VD as Vector Database

User->>UI: Submit journal entry
UI->>BE: POST journal-entry{id}
BE->>PG: Save journal entry


alt stored successfully
    PG -->>BE: Confirm entry saved
    BE ->> UI: Success message
    UI ->> User: Positive feedback
    BE ->> MQ: Add journal entry to queue
    MQ -->> BE: Worker picks up job
    Note over BE: Worker performs chunking
    BE ->> EM: Send chunks
    EM -->> BE: Return vectors
    BE ->> VD: Store embedding
    VD -->> BE: Embedding stored
    BE ->> MQ: Acknowledge job complete
else error
    PG -->>BE: Entry not saved
    BE ->> UI: Error message
    UI ->> User: Negative feedback
end
```

[^diagram-commits]: Originally `docs/sequence-diagram.mmd`, converted to an OKF document on 2026-11-22 without changing the diagram.
