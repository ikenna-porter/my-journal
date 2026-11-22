---
type: Decision
title: Hosting - one larger Hetzner VPS for everything
description: For now the app, Postgres, the local models, the agent runtime and self-hosted Langfuse all run on one larger Hetzner VPS. There is no AWS or managed cloud.
tags: [decision, infrastructure, hosting]
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

For now, everything runs on **one larger Hetzner VPS**:[^ike-2026-11-22]

```
  +-----------------------------------------------------------+
  | Hetzner VPS                                               |
  |                                                           |
  |  FastAPI app  (includes the agent: LangGraph is a Python  |
  |               library running inside this process)        |
  |  Queue worker (chunking + embeddings)                     |
  |  Postgres + pgvector                                      |
  |  Local models: embeddings (+ reranker if local)           |
  |  Langfuse stack (its own Postgres, ClickHouse, Redis, S3) |
  +-----------------------------------------------------------+
            |
            +--> Claude API (the only outside service that sees entry text)
```

* Size: the self-hosted Langfuse stack alone is recommended to have roughly 4 CPU cores and 16 GB of RAM, so the VPS needs more headroom than the app alone.
* No AWS and no managed cloud services, in line with the PRD's cost constraint ([PRD section 5.1](../product/prd.md)).
* The agent is not deployed separately. LangGraph runs as part of the FastAPI backend.

# Keep components separable

Everything starts on one machine, but each component must be movable to its own machine later without code changes:[^decoupled]

* Each component (API, queue worker, embedding/reranker models, Postgres, Langfuse) sits behind its own interface.
* Every connection is an address set in config (an environment variable): the database URL, the model-service URL, the Langfuse host, and so on. Nothing assumes `localhost`.
* Moving a component means changing config, not code.

# Later

If Langfuse starts competing with the app for resources, move it to a second VPS. Only the trace endpoint URL changes.

[^ike-2026-11-22]: Ike chose option 1 ("for now option 1 sounds good") and wants "whatever is cheap and functional."
[^decoupled]: Ike: "we'll have to keep everything decoupled so that we can later host these services on separate machines if necessary... but to start i imagine most of them should be on the same machine."
