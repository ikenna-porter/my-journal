# Proposal: API contract (slice 0)

**Roadmap slice:** 0, API contract ([roadmap](../../../docs/product/roadmap.md)).
**Hands-on score:** 4 (Ike implements; Claude writes the failing tests, gives guidance and reviews).
**Skills it teaches:** API design (resources, status codes, error contracts), Pydantic v2 schema modelling (validation, discriminated unions, response models), FastAPI routing and dependencies, OpenAPI as a contract, contract testing.

## Why

The [development methodology](../../../docs/decisions/development-methodology.md) says every v1 endpoint is designed before any slice is built, so slices 1 to 5 code against a fixed contract instead of inventing endpoints as they go. Nothing exists yet. The Express backend is being replaced, and there is no Python project, schema or shared type between the React client and the server.

## What Changes

- New Python + FastAPI project in `backend/`, replacing the Express server going forward (the Express code is left in place and not built on).
- **Code-first contract:** Pydantic models and stub FastAPI routes define every v1 endpoint. Each stub validates its request and returns `501 Not Implemented` until its slice builds it. FastAPI generates `contract/openapi.json`, which is committed, and a test fails if the code and the committed file drift apart.
- **v1 endpoints designed:** health, current user, entries (create, list, read, delete), search, observations (poll, feedback), conversations (create, read, list, send message with a streamed reply) and Collaborative Reflections (AI draft, save).
- **Conventions:** Auth0 bearer tokens on every endpoint except health; RFC 9457 `application/problem+json` errors with a stable `code`; offset pagination for lists; a plain `limit` for search; polling for observations; server-sent events (SSE) for conversation replies.
- **Generated TypeScript types** for the React client (`client/src/api/schema.d.ts`), with a check that they match `contract/openapi.json`.
- **Contract tests:** tests that pass now (every route exists, requires auth, validates input, returns problem+json), plus behavior tests for each slice, marked strict-xfail, which turn into a failure when a slice makes them pass and the marker hasn't been removed.
- `openspec/config.yaml` now carries the methodology rules (scores, TDD ordering, hand-off) so every later slice's artifacts follow them.

## Capabilities

### New Capabilities
- `api-conventions`: rules every endpoint follows: base path, authentication, error format, pagination, user scoping, stub behavior, and the contract artifacts (committed OpenAPI, generated TypeScript types, drift checks).
- `entries-api`: the HTTP contract for creating, listing, reading and deleting entries, including immutability and the deletion cascade's external behavior.
- `search-api`: the HTTP contract for searching entries by meaning.
- `observations-api`: the HTTP contract for polling an entry's observation and giving thumbs up/down feedback.
- `conversations-api`: the HTTP contract for starting an Observation Reply or Direct Conversation, sending messages, streaming replies over SSE, and the 30-day transcript lifetime.
- `reflections-api`: the HTTP contract for drafting and saving a Collaborative Reflection that closes a conversation.

### Modified Capabilities
None. There are no existing specs.

## Impact

- **New code:** `backend/` (FastAPI app, Pydantic schemas, routers, tests), `contract/openapi.json`, `client/src/api/schema.d.ts`, a CI workflow for backend tests and the drift checks.
- **New dependencies:** Python 3.13, uv, FastAPI, Pydantic v2, pytest, httpx, ruff (backend); `openapi-typescript` (client dev dependency).
- **Docs:** a new decision doc for the API conventions; updates to the roadmap (open questions resolved), the development methodology (open item resolved), the frontend decision (type generation decided), `docs/index.md` and `docs/log.md`.
- **No data, AI or Auth0 integration** in this slice: auth is a stub dependency that slice 1 replaces with real Auth0 JWT verification.
