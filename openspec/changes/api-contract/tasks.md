# Tasks: API contract (slice 0, score 4)

Scores follow the [hands-on scale](../../../docs/decisions/development-methodology.md).

**Who does what** (tag after each task's score):

| Tag | Meaning |
|---|---|
| 🧑 **Ike** | You do it. Claude only explains beforehand and reviews afterwards |
| 🤖 **Claude** | Claude does it and explains it (a summary at score 1, a line-by-line walkthrough at 2+) |
| 🧑→🤖 **Ike, then Claude** | You write the core until you've got the pattern, say "take over", then Claude finishes in your style |
| ✅ **Ike approves** | Claude drafts it; you confirm it describes the right behavior before anyone writes code |

Your personal work is concentrated in **3.2, 4.1 to 4.3, 5.2, 6.2, 7.2 and 8.2** (the Pydantic schemas and stub routes) plus the approvals. After you say "take over", 5.2 onwards can move to Claude.

## 1. Record the decisions

- [x] 1.1 [score 1] **🤖 Claude:** Write `docs/decisions/api-contract-conventions.md` (OKF, `type: Decision`) covering D1 to D7 in design.md, with footnotes quoting Ike's choices. Verify the frontmatter has `type`, `title`, `description`, `status` and `generated`
- [x] 1.2 [score 1] **🤖 Claude:** Update PRD 3.1 to list the optional entry title, linking the new decision. Resolve the "Open" items in `development-methodology.md` (config.yaml rules), `roadmap.md` slice 0 (streaming format) and `frontend-react-typescript.md` (type generation). Verify no "Open" item about these remains
- [x] 1.3 [score 1] **🤖 Claude:** Add the new doc to `docs/index.md` and a dated entry at the top of `docs/log.md`. Verify both links resolve

## 2. Backend skeleton

- [x] 2.1 [score 1] **🤖 Claude:** Create `backend/` with uv (Python 3.13, FastAPI, Pydantic v2, pytest, httpx, ruff) and verify `uv run pytest` runs with no tests collected
- [x] 2.2 [score 1] **🤖 Claude:** Write the failing test `tests/conventions/test_health.py` (`GET /api/v1/health` gives `200 {"status": "ok"}` without a token) and verify it fails
- [x] 2.3 [score 1] **🤖 Claude:** Add `create_app()` with the `/api/v1` router and the health route, and verify 2.2 passes
- [x] 2.4 [score 1] **🤖 Claude:** Explain what Claude wrote in group 2 (short summary)

## 3. Conventions: errors, auth stub, pagination, stubs

- [ ] 3.1 [score 3] **🤖 Claude writes · ✅ Ike approves:** Claude writes failing convention tests: problem+json shape and media type, `422 validation_error` with `errors`, `404 not_found` and `405 method_not_allowed` as problems, a missing token gives `401 unauthenticated`, `/me` with the stub token gives `501`, `limit=500` gives `422`. Ike confirms they match the api-conventions spec. Verify they fail
- [ ] 3.2 [score 3] **🧑 Ike:** Ike writes the core: the `Problem` model and `ErrorCode` enum (`app/errors.py`). Claude reviews
- [ ] 3.3 [score 3] **🤖 Claude:** Claude writes the plumbing: exception handlers, the `get_current_user` stub with `AUTH_STUB_TOKEN` (refuses to start in production), `Page[T]` and `PageParams`, a `not_implemented()` helper and the `/me` stub. Verify the 3.1 tests pass
- [ ] 3.4 [score 2] **🤖 Claude explains · 🧑 Ike explains back:** Line-by-line walkthrough of the 3.3 plumbing; Ike explains the handler flow back

## 4. Entries contract (Ike writes it, guided)

- [ ] 4.1 [score 4] **🤖 Claude teaches · 🧑 Ike decides mood:** Claude gives the Pydantic primer for entries (D14 item 1) and Ike confirms whether mood is free text or an enum
- [ ] 4.2 [score 4] **🤖 Claude writes · ✅ Ike approves:** Claude writes failing tests from entries-api: valid create gives `501`; empty content, content over 100,000 chars, title over 200, mood over 32 and future `written_at` give `422`; `PUT`/`PATCH` give `405`; list/read/delete require auth and give `501`; `limit`/`offset` are validated. Ike agrees. Verify they fail
- [ ] 4.3 [score 4] **🧑 Ike:** **Ike writes the core:** `app/schemas/entries.py` (`EntryCreate`, `Entry`, `EntrySummary`) and stub routes in `app/routers/entries.py` with `response_model`, status codes and declared error responses. Verify the 4.2 tests pass and Claude reviews
- [ ] 4.4 [score 4] **🤖 Claude:** Claude writes strict-xfail behavior tests marked `slice(1)` for the entries-api scenarios (create/read round trip, newest first, user scoping, delete then 404, reflections on read), and verify they report `xfail`

## 5. Observations contract

- [ ] 5.1 [score 4] **🤖 Claude writes · ✅ Ike approves:** Claude gives the primer (D14 item 2), then writes failing tests: the poll route documents `202`/`200`/`204`/`404`; feedback accepts `up`/`down` and rejects other values with `422`; both give `501` when valid. Ike agrees. Verify they fail
- [ ] 5.2 [score 4] **🧑 Ike:** **Ike writes the core:** `app/schemas/observations.py` (`Observation`, `Citation`, `ObservationPending`, `FeedbackRequest`) and the stub routes. Verify the 5.1 tests pass and Claude reviews
- [ ] 5.3 [score 4] **🧑→🤖 Ike, then Claude:** If Ike has said "take over", Claude writes the remaining schemas in the same style. Otherwise Ike continues. Either way, Claude adds strict-xfail `slice(4)` behavior tests (pending, then observation or silence, the 8-second budget, spend limit gives silence, feedback replaces). Verify they report `xfail`

## 6. Conversations contract (with SSE events)

- [ ] 6.1 [score 4] **🤖 Claude writes · ✅ Ike approves:** Claude gives the primer (D14 item 3), then writes failing tests: create validates `entry_id` and `observation_id`; message `content` is 1 to 10,000 chars; the messages route documents `text/event-stream`; `MessageDelta`, `ToolStarted`, `MessageCompleted` and `StreamError` appear in `components.schemas`; list takes `entry_id` plus pagination; all give `501` when valid. Ike agrees. Verify they fail
- [ ] 6.2 [score 4] **🧑→🤖 Ike, then Claude (the openapi hook is 🤖 Claude):** **Ike writes the core** (or Claude after "take over"): `app/schemas/conversations.py` and the stub routes. Claude adds the custom `openapi()` hook that registers the event models. Verify the 6.1 tests pass
- [ ] 6.3 [score 4] **🤖 Claude:** Claude writes strict-xfail behavior tests: `slice(3)` for Direct Conversation (AI opens, stream event order, `409` while streaming, spend limit gives `503` before the stream, read/resume, `410` after expiry, transcripts absent from entries) and `slice(5)` for Observation Reply (first message requires content). Verify they report `xfail`

## 7. Reflections contract

- [ ] 7.1 [score 4] **🤖 Claude writes · ✅ Ike approves:** Claude gives the primer (D14 item 4), then writes failing tests: `PUT` rejects `ai_assisted`/`cited_entry_ids` with `422`, rejects a bad `source`, and enforces content length; the draft route gives `501`. Ike agrees. Verify they fail
- [ ] 7.2 [score 4] **🧑→🤖 Ike, then Claude:** **Ike writes the core** (or Claude after "take over"): `app/schemas/reflections.py` (`ReflectionDraft`, `ReflectionSave` with `extra="forbid"`, `Reflection`) and the stub routes. Verify the 7.1 tests pass
- [ ] 7.3 [score 4] **🤖 Claude:** Claude writes strict-xfail `slice(5)` behavior tests (draft not saved, `409` with no messages, `201` then `200` on replace, `ai_assisted` from `source`, permanent after expiry, `410` on rewrite after expiry). Verify they report `xfail`

## 8. Search contract

- [ ] 8.1 [score 4] **🤖 Claude writes · ✅ Ike approves:** Claude gives the primer (D14 item 5), then writes failing tests: `query` is 1 to 1,000 chars; `limit` is 1 to 50 (default 10); `offset` is rejected; `GET /search` gives `405`; a valid request gives `501`. Ike agrees. Verify they fail
- [ ] 8.2 [score 4] **🧑→🤖 Ike, then Claude:** **Ike writes the core** (or Claude after "take over"): `app/schemas/search.py` (`SearchRequest`, `SearchFilters`, `SearchResult`, `SearchResponse`) and the stub route. Verify the 8.1 tests pass
- [ ] 8.3 [score 4] **🤖 Claude:** Claude writes strict-xfail `slice(2)` behavior tests (ranked results, user scoping, date filter, empty results). Verify they report `xfail`

## 9. Cascade and route-wide contract checks

- [ ] 9.1 [score 2] **🤖 Claude:** Claude writes strict-xfail cascade tests from entries-api "Deletion cascades through the API", one per owning slice: search `slice(2)`, conversation `slice(3)`, observation `slice(4)`, reflection `slice(5)`. Verify they report `xfail`
- [ ] 9.2 [score 2] **🤖 Claude:** Claude writes the parametrized route-table test: every non-health route gives `401` without a token and declares the bearer security scheme. Verify it passes for every route, then walk through it line by line

## 10. Contract artifacts and drift checks

- [ ] 10.1 [score 2] **🤖 Claude:** Claude writes the failing drift test `tests/test_openapi_drift.py` (live `app.openapi()` equals `contract/openapi.json`) and verify it fails because the file is missing
- [ ] 10.2 [score 2] **🤖 Claude:** Claude writes `scripts/export_openapi.py` (stable, sorted output), generates `contract/openapi.json`, and verifies the drift test passes. Line-by-line walkthrough
- [ ] 10.3 [score 1] **🤖 Claude:** Add `openapi-typescript` to `client/` with a `gen:api` script, generate `client/src/api/schema.d.ts`, and verify `npx tsc --noEmit` passes and `git diff --exit-code` is clean after regenerating
- [ ] 10.4 [score 1] **🤖 Claude (🧑 Ike approves the push):** Add the GitHub Actions workflow (ruff, pytest, OpenAPI drift, TS drift, tsc) and verify it passes on a pushed branch, once Ike asks to push

## 11. End-to-end verification

- [ ] 11.1 [score 1] **🤖 Claude runs · 🧑 Ike reviews and signs off:** From a clean checkout: `uv sync && uv run pytest` is green, with convention tests passing and behavior tests reporting only `xfail`. `uv run fastapi dev` serves `/docs` showing every v1 endpoint with its errors. Regenerating the contract and the TS types produces no diff. `openspec validate api-contract --strict` passes. Slice 1 starts only after this

## Workflow follow-up

- Update the README with how to run the backend and regenerate the contract.
- Archive the change with `openspec-archive-change` once 11.1 passes and Ike has reviewed it.
