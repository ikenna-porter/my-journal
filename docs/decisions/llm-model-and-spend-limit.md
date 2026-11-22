---
type: Decision
title: LLM - Claude via the Anthropic SDK, model and spend limit set by environment variables
description: Claude is called directly through the Anthropic SDK. The model is chosen by an environment variable (Claude Opus 5.5 for now), and a monthly spend limit in another environment variable ($50) blocks every LLM call once it's reached.
tags: [decision, ai, llm, cost, config]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T19:05:00Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# Decision

* **Provider and SDK:** Claude, called directly through the official Anthropic Python SDK. No wrapper library sits in between, because the hand-built loop needs to work with the real tool-calling protocol (see [Agent harness](agent-harness.md)).
* **Model is configuration, not code.** It's set by an environment variable, currently **`claude-opus-5-5`** (Claude Opus 5.5).[^ike-2026-11-22] Changing the model needs no code change.
* **Spend limit.** An environment variable holds a USD limit, currently **$50 per calendar month**. Once recorded spend for the month reaches the limit, **every LLM call is refused** until the next month starts or the limit is raised.[^ike-2026-11-22][^monthly]
* **The journal keeps working when the limit is hit.** Writing, saving and reading entries never call the LLM. Only the AI features stop, and they are optional anyway (see [AI features are optional](ai-features-optional.md)).

# Proposed details (not yet confirmed)

* Environment variable names: `LLM_MODEL_OBSERVATION` and `LLM_MODEL_CONVERSATION` (both `claude-opus-5-5` for now, so evals can later pick a different model for each without a code change), and `LLM_SPEND_LIMIT_USD=50`.
* Spend is counted by the app itself, before each call and after it returns, from the token usage in each response and a price table in config. It is not read from Langfuse, because the limit must work even when tracing is down.
* As a backstop, set a matching spend limit on the Anthropic Console workspace that the API key belongs to.

# Open

* Do eval runs count against the same limit, or use a separate key and limit?

[^ike-2026-11-22]: Ike: "lets make it so that the model choice is an env variable. for now let's go with opus 5.5... i want to set a spending limit (also an env variable) that will make all calls invalid if the spending limit has been surpassed... let's set the limit to $50."
[^monthly]: Ike chose a monthly limit that resets, over a lifetime total.
