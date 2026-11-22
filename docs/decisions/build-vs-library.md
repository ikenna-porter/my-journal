---
type: Decision
title: Build it yourself vs use a library
description: Which AI components are hand-built for learning and job-search value, and which come from frameworks or libraries.
tags: [decision, ai, learning, stack]
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

The rule: build a component by hand **only when knowing its internals matters a lot in an AI engineering job search**. Everything else comes from a framework or library.[^ike-2026-11-22]

| Build it yourself | Use a library or framework |
|---|---|
| The agent loop and tool calling (see [Agent harness](agent-harness.md)) | Langfuse: tracing, cost, scores |
| The retrieval pipeline: chunking, keyword search, vector search, fusion, the rerank step (see [Retrieval pipeline](retrieval-pipeline.md)) | DeepEval as the test runner, Ragas metrics |
| Eval design: the golden dataset and the app's own custom metrics (citation correctness, "says I don't know") | Embedding and reranker **models** (called, never trained) |
| | LangGraph's runtime: checkpointer, state, interrupts |
| | MCP protocol plumbing (SDK) |
| | Presidio and other guardrail libraries |
| | ORM and migrations, auth |

# Why

* Interviews ask about agent loops, retrieval quality and eval design, so hand-built versions of those give Ike first-hand answers.
* Writing tracing backends, test runners, checkpoint stores or protocol transports from scratch takes weeks and isn't what interviews test. For those, knowing how to use the tool well is the marketable skill.

[^ike-2026-11-22]: Ike: "I only want to build the ones that are of high impact (ie the ones that matter the most in the job search). For the rest I don't mind using a framework/library." He confirmed the split above.
