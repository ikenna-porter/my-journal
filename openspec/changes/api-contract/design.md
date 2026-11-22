# Design: API contract (slice 0)

## Context

See proposal.md (Why). The repo has a React 19 + Vite client and an Express stub server that is being replaced. There is no Python code, no tests and no CI. Requirements are in `specs/`. This design covers how the contract is produced, kept honest and handed to the client, and how Ike is guided through writing it (slice score 4).

## Goals / Non-Goals

**Goals:**
- A runnable FastAPI app whose every v1 route exists, authenticates, validates and returns `501` until built.
- A single source of truth (Pydantic + routes) with the generated `contract/openapi.json` and TypeScript types checked for drift.
- Contract tests that pass today for the conventions, plus behavior tests per slice that each slice turns on.

**Non-Goals:**
- No database, Alembic, Auth0 verification, Celery, retrieval or LLM calls (slices 1 to 5).
- No React UI and no typed fetch client wrapper yet, only generated types.
- No deployment.

## Decisions

### D1. Code-first contract: Pydantic + FastAPI generate OpenAPI
Ike chose this over hand-written OpenAPI YAML (2026-11-22). Pydantic is the skill employers look for in AI backend work, and it leaves a single source of truth. `scripts/export_openapi.py` writes `app.openapi()` to `contract/openapi.json` (sorted keys, stable output). A pytest test compares the live document to the committed file. **Recorded in:** new `docs/decisions/api-contract-conventions.md` (task 1).

### D2. Errors: RFC 9457 problem+json with a stable `code`
Ike chose this over FastAPI's default `{"detail": ...}`. One `Problem` Pydantic model, an `ErrorCode` string enum, and exception handlers that convert `HTTPException`, `RequestValidationError` (to `422 validation_error` with `errors`) and Starlette's 404/405 into problems. Each route declares its error responses with `responses={...}` so they show up in the contract. **Recorded in:** `api-contract-conventions.md`.

### D3. Pagination: offset for entries and conversations, `limit` only for search
Ike chose offset over cursor: one person's journal is small, and a user isn't writing while paging through it, so cursor's advantages don't apply. A generic `Page[T]` model returns `{items, total, limit, offset}`. **Recorded in:** `api-contract-conventions.md`.

### D4. Observation delivery: polling
Ike chose polling over SSE or WebSocket for the single observation. `202` pending (with `Retry-After: 1`), `200` observation, `204` silence. Failures and the spend limit are reported as silence to the client and recorded server-side in traces (slice 4). **Recorded in:** `api-contract-conventions.md`. This resolves the roadmap's open "streaming format" question together with D5.

### D5. Conversation replies: SSE on each message POST; create, then stream
Each `POST /conversations/{id}/messages` returns its own short-lived `text/event-stream`. Conversations are turn-based, so a WebSocket's two-way channel isn't needed. Creation is plain JSON and every streamed reply comes from one endpoint (Ike chose this over "create and stream at once"). OpenAPI can't describe SSE event payloads natively, so the event models (`MessageDelta`, `ToolStarted`, `MessageCompleted`, `StreamError`) are added to `components.schemas` with a custom `openapi()` hook. That way the TypeScript types include them, and the route documents `text/event-stream` as its `200` response. **Recorded in:** `api-contract-conventions.md`.

### D6. Reflections: draft endpoint + PUT, server decides provenance
Ike chose this over a single endpoint, keeping the human-in-the-loop approval that slice 5 builds with LangGraph interrupts. The request model forbids extra fields (`extra="forbid"`), so a client can't send `ai_assisted` or `cited_entry_ids`. **Recorded in:** `api-contract-conventions.md`.

### D7. Entry fields: optional title added
Ike chose to add an optional `title` (≤200 chars) to the PRD's content + mood + timestamp. `mood` is **assumed** to be free text (≤32 chars), which was not explicitly confirmed; see Open Questions. The timestamp field is named `written_at` to separate it from `created_at` (the save time), because date filters use `written_at`. **Recorded in:** `api-contract-conventions.md`, and PRD 3.1 is updated to list the title (task 1).

### D8. Methodology rules live in `openspec/config.yaml`
Ike chose config rules over a custom schema or none. Already applied in this change. **Recorded in:** `development-methodology.md` (its "Open" item is resolved in task 1).

### D9. Project layout and tooling (Claude's call)
```
backend/
  pyproject.toml            uv, Python 3.13, ruff, pytest
  app/main.py               create_app(), handlers, custom openapi()
  app/errors.py             Problem, ErrorCode, handlers
  app/auth.py               get_current_user dependency (stub)
  app/pagination.py         Page[T], PageParams
  app/schemas/{entries,search,observations,conversations,reflections,users}.py
  app/routers/{same}.py     stubs -> raise NotImplementedProblem
  tests/conventions/        pass in slice 0
  tests/contract/           per-slice behavior tests (strict xfail)
  tests/test_openapi_drift.py
scripts/export_openapi.py
contract/openapi.json       committed, generated
client/src/api/schema.d.ts  committed, generated by openapi-typescript
```
`contract/` sits at the repo root because both sides depend on it. uv because it's fast and keeps the lockfile reproducible.

### D10. Auth stub until slice 1
`get_current_user` requires a bearer header and, in slice 0, accepts a fixed test token from settings (`AUTH_STUB_TOKEN`), returning a fixed fake user. The OpenAPI security scheme is `HTTPBearer` with `bearerFormat: JWT`, so the contract is final. Slice 1 replaces only the dependency's body with Auth0 JWT verification.

### D11. Two kinds of contract tests
- **Convention tests (pass now):** for every route in `app.routes`, a missing token gives `401 unauthenticated`, a valid stub request gives `501 not_implemented`, an invalid body gives `422 validation_error`, and every error has the `application/problem+json` media type. Parametrized over the route table, so a new route is covered automatically.
- **Behavior tests (one module per slice):** they encode the spec scenarios and are marked `@pytest.mark.slice(n)` plus `xfail(strict=True)`. They fail as expected until slice *n*. When a slice makes one pass, strict-xfail turns it into a failure, which forces the marker to be removed. CI is green throughout, and each slice gets a ready-made checklist. Scenarios that need data or time control (expiry, cascade) are written against fixtures that slice 1 and later slices provide. In slice 0 they're stubs that fail.

### D12. TypeScript generation
`openapi-typescript` (dev dependency in `client/`) with an npm script `gen:api`. CI regenerates the types and runs `git diff --exit-code` on `client/src/api/schema.d.ts`, then `tsc --noEmit`.

### D13. CI
One GitHub Actions workflow: `uv run ruff check`, `uv run pytest` (backend), plus the TS drift check and `tsc`. Slice 2 adds the eval gate to it.

### D14. How Ike is guided (score 4, "I will need guidance as I write it")
Before each schema module, Claude gives a short primer on the Pydantic or FastAPI pattern it needs, with a tiny example that isn't from this API. Then Claude writes the failing tests, Ike writes the module, and Claude reviews. The patterns, in order:
1. `entries`: `BaseModel`, `Field` constraints, optional fields, `datetime` validation (`written_at` not in the future), separate request and response models, `response_model` and status codes.
2. `observations`: `Literal` enums, multiple responses on one route (`202`/`200`/`204`), response headers.
3. `conversations`: `model_validator` for cross-field rules, documenting a streaming response, SSE event models.
4. `reflections`: `extra="forbid"`, server-set fields that are excluded from the request model.
5. `search`: request bodies with nested filter models.
Ike can say "take over" at any point after `entries`.

### Deletion cascade
This slice adds no stored data, so nothing is deleted yet. It fixes the cascade's **external contract** (entries-api "Deletion cascades through the API") as strict-xfail behavior tests owned by slices 1 to 5, so each slice's tests prove its part of the cascade.

## Risks / Trade-offs

- [Code-first lets the contract change by accident] → The committed `openapi.json` plus the drift test makes every contract change a visible diff in review.
- [SSE events are invisible to OpenAPI tooling] → The event models are registered in components and covered by a convention test that asserts they're present.
- [Strict-xfail tests written before the data model may need rewriting] → They assert only HTTP-visible behavior from the specs, never tables. Fixtures are the one place slices fill in setup.
- [Too much up-front design before learning from slice 1] → The contract can change through later OpenSpec changes. Drift checks make that explicit rather than forbidden.
- [Auth stub could leak into production] → The stub token setting has no default, and the app refuses to start with it set when `ENV=production`.

## Migration Plan

The Express server stays in `server/`, unused. Slice 1 removes it once the FastAPI backend serves entries. Nothing is deployed in this slice.

## Open Questions

- **Mood: free text or enum?** Assumed free text (≤32 chars). Recommendation: keep it free text until search filters show a need. Tightening to an enum later is a contract change that the drift check will flag. It can be confirmed when Ike writes the `entries` schema.
- **Auth0 login methods and session handling**: slice 1 decides this. It doesn't change this contract, because bearer tokens are fixed here.
