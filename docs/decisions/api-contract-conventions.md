---
type: Decision
title: API contract conventions - code-first OpenAPI, problem+json errors, offset pages, polling and SSE
description: The v1 API contract is generated from Pydantic models and FastAPI routes. Errors use RFC 9457 problem+json, lists use offset pagination, observations are polled, conversation replies stream over SSE, reflections are drafted then saved, and entries have an optional title.
tags: [decision, api, contract, backend]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T22:00:00Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Slice 0 planning conversation with Ike, 2026-11-22
  - id: rfc9457
    resource: https://www.rfc-editor.org/rfc/rfc9457
    title: "RFC 9457: Problem Details for HTTP APIs"
  - id: change
    resource: ../../openspec/changes/api-contract/design.md
    title: OpenSpec change api-contract, design D1 to D7
---

# Decision

These conventions govern every v1 endpoint. The full contract is in the OpenSpec change `api-contract`.[^change]

| # | Topic | Decision | Rejected |
|---|---|---|---|
| 1 | Source of truth | **Code-first.** Pydantic models + FastAPI routes generate `contract/openapi.json`, which is committed and checked for drift. TypeScript types are generated from it.[^code-first] | Hand-written OpenAPI YAML |
| 2 | Errors | **RFC 9457 `application/problem+json`**[^rfc9457] with a stable `code` field (e.g. `spend_limit_reached`).[^errors] | FastAPI's default `{"detail": ...}` |
| 3 | Pagination | **Offset** (`limit`, `offset`) for entries and conversations. Search returns the top `limit` with no paging.[^offset] | Cursor |
| 4 | Observation delivery | **Polling** `GET /entries/{id}/observation`: `202` pending, `200` observation, `204` silence.[^polling] | SSE, WebSocket |
| 5 | Conversation replies | **SSE** on each `POST /conversations/{id}/messages`. A conversation is created first with plain JSON, then streamed.[^sse] | WebSocket; create and stream at once |
| 6 | Collaborative Reflection | **Draft endpoint + `PUT`.** The AI draft is never saved until the user approves it. The server sets `ai_assisted` and the cited entries.[^reflection] | One endpoint that saves the AI's text directly |
| 7 | Entry fields | `content` (Markdown), **optional `title`**, optional `mood`, `written_at` (editable only at creation).[^title] | No title |

# Why

* **Code-first:** Pydantic is central to AI backend work (SDKs, tool schemas, structured outputs), and one source of truth can't drift from itself.
* **Offset over cursor:** cursor pagination helps when items are inserted while someone pages, or when tables are huge. Neither is true of one person's journal.
* **Polling for observations:** an observation is one message that arrives once within 8 seconds. Polling is the simplest thing to build, test and trace.
* **SSE for replies:** conversations are turn-based, so only the server-to-client direction streams. A WebSocket's two-way channel isn't needed.
* **Draft + PUT:** this keeps the user's approval of an AI-written reflection (human in the loop), which slice 5 builds.

# Open

* Whether `mood` is free text (assumed, up to 32 characters) or a fixed list. Ike confirms this when writing the entries schema (task 4.1).

[^change]: See `sources` (change).
[^code-first]: Ike chose option A, code-first: "option A...but i will need guidance as i write it out."
[^errors]: Ike chose "RFC 9457 problem+json".
[^offset]: Ike: "if a user is viewing all their journal entries, they will not be able to actually write a new entry. as such, there is no need for a cursor", then agreed to offset.
[^polling]: Ike: "i'm fine with just doing polling."
[^sse]: Ike chose "Create, then stream". SSE per message was proposed with the polling choice and not objected to.
[^reflection]: Ike chose "Draft endpoint + PUT".
[^title]: Ike chose "Add a title".
