---
type: Decision
title: Retrieval pipeline - full pipeline in v1, hand-built
description: v1 ships the complete hand-built retrieval pipeline (chunking, keyword + vector search, RRF fusion, reranking, date filters), and each step is measured with evals as it's added.
tags: [decision, ai, rag, retrieval]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T18:47:12Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
  - id: prd
    resource: ../product/prd.md
    title: PRD v1, sections 4.2 to 4.4
---

# Decision

Retrieval is a plain Python function, exposed to the agent as a tool such as `search_entries(query, date_range)`. It contains no agent logic. Ike writes every step. The models are called, not built.[^ike-2026-11-22]

```
  1  chunking ............ paragraph split + semantic merge (PRD 4.3)
  2a keyword search ...... Postgres full-text search (SQL)
  2b vector search ....... pgvector similarity (SQL) + embedding model
  3  fusion .............. reciprocal rank fusion (RRF)
  4  rerank .............. reranker model scores the top ~30, keeps the top few
  +  metadata filters .... date, mood, entry type (PRD 4.2)
```

* **The whole pipeline is part of v1.**[^ike-2026-11-22]
* While building it, add the steps one at a time and run the evals after each. That shows what each step contributes and gives before/after numbers for the portfolio.
* The embedding model stays as the PRD's `all-mpnet-base-v2` (sentence-transformers, run locally) until a decision doc replaces it.[^prd]
* "Hybrid" here means keyword + vector search, plus the PRD's metadata filters.

# Reranker

* It runs **locally on the VPS** (an open BGE-family cross-encoder), not as a hosted API, so entry text stays on the server.[^reranker]
* It sits **behind a config switch**. Evals compare retrieval with and without it, and it stays on only if it earns its roughly 1 to 2 seconds of the 8-second observation latency budget.
* The reranker's relevance score is the preferred input for Observation Mode's confidence threshold, because it measures relevance better than raw vector similarity. Tune the threshold with the reranker both on and off.

# Open

* The exact reranker model (for example bge-reranker-base or bge-reranker-v2-m3), chosen by evals and latency.

[^ike-2026-11-22]: Ike: "the entire retrieval workflow should be a part of v1 of this app."
[^prd]: PRD v1, section 4.4.
[^reranker]: Ike: "in my mind it would run on the VPS with everything else."
