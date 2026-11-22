---
type: Decision
title: "Frontend: React + TypeScript"
description: The frontend stays in TypeScript and uses React.
tags: [decision, frontend]
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

The frontend is written in **TypeScript** with **React**.[^ike-2026-11-22] This matches the existing `client/` (React 19 + Vite). See [Current state](../architecture/current-state.md).

# Consequences

* The frontend will talk to the new [Python + FastAPI backend](backend-python-fastapi.md) over HTTP. Types for the API could be generated from FastAPI's OpenAPI schema, which hasn't been decided yet.

[^ike-2026-11-22]: Ike: "the FE should ofc be in typescript. we can use react for it."
