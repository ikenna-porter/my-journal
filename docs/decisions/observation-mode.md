---
type: Decision
title: Observation Mode - how observations work
description: Retrieval finds similar past chunks, and the LLM turns them into a single observation of about 5 sentences, with citations, within 8 seconds.
tags: [decision, product, observation-mode]
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

These rules refine [PRD section 3.2](../product/prd.md).[^ike-2026-11-22]

* **Retrieval uses similarity.** Candidate past chunks are found by similarity to the new entry.
* **The insight comes from the LLM.** The LLM reasons over the retrieved chunks and surfaces evolution, stagnation, improvement, contradictions and so on, not just "you wrote something similar."
* **Format:** each observation is a single message of roughly 5 sentences or fewer, and it cites and links the past entries it draws on.
* **Latency:** observations must appear within **8 seconds** of saving, covering embedding, retrieval with reranking, and the LLM call. This is the latency budget. (An earlier 5-second target was dropped in favour of 8 seconds.)[^latency]
* **Optional:** like every AI feature, observations can be ignored or skipped. See [AI features are optional](ai-features-optional.md).

# Design consequence (proposed, not decided)

To meet the latency budget, an observation should probably be one fixed pass (retrieve, then generate) rather than a multi-step agent loop. Each extra model call adds about 2 to 4 seconds.

[^ike-2026-11-22]: Ike: "an observation should look for similarity... the agent will later use the retrieved chunks to provide thoughtful insight... an observation is a single message (no longer than 5 sentences more or less)... if this is unrealistic, we can aim for 8 second cap."
[^latency]: Ike: "remember i increased it to 8 seconds."
