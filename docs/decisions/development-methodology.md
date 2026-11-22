---
type: Decision
title: "Development methodology: contract first, vertical slices, TDD, hands-on scores"
description: The API contract is designed first. Features are then built as end-to-end vertical slices, all code is test-driven, and every slice and task gets a 1 to 5 hands-on score for how much of it Ike writes himself.
tags: [decision, process, tdd, learning]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T20:20:00Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# Decision

Four rules govern how v1 is built:[^ike-2026-11-22]

1. **Contract first.** Every API endpoint the app needs is designed (request, response, errors, auth) before any slice is built. Slices and everything that depends on them code against that contract.
2. **Vertical slices.** The app is split into slices that each deliver one feature end to end: UI, API, data and any AI. Each slice is tested end to end before the next begins.
3. **TDD for all code.** A failing test is written before the code that makes it pass, with no exceptions.
4. **Hands-on scores.** Every slice, and every task within a slice, gets a score from 1 to 5 that sets how much of it Ike writes himself. Higher scores go to work that is most marketable for AI engineering and backend roles.

# Hands-on scale

TDD applies at every level. The score sets who writes the tests and who writes the code.[^scale]

| Score | Name | Tests are written by | Code is written by | Claude's role |
|---|---|---|---|---|
| **5** | You build it | Ike | Ike, until he hands off | Explains the concepts first, answers questions, reviews. Writes nothing until the handoff |
| **4** | You implement | Claude; Ike agrees they describe the right behavior first | Ike, until he hands off | Writes the failing tests, gives hints, reviews |
| **3** | Pair | Claude | Split: Ike writes the core functions Claude marks; Claude writes the surrounding plumbing | Scaffolds, marks Ike's parts, reviews |
| **2** | You study it | Claude | Claude | Walks through every line; Ike must be able to explain it back |
| **1** | Claude handles it | Claude | Claude | Writes it and gives a short summary |

## Learn, then hand off (scores 4 and 5)

Ike doesn't write everything at 4 or 5, because that would slow development too much.[^handoff]

1. Ike writes the **core** of the task (and its tests, at a 5) until he understands the pattern.
2. Ike says **"take over"**.
3. Claude finishes the rest of the task in the same style, then walks through what it added (as at level 2).

## Ike understands all the code

Every piece of code Claude writes, at every level, comes with an explanation sized to its score: a short summary at 1, a line-by-line walkthrough at 2 or above.

## How scores are chosen

1. How marketable the skill is for AI engineering and backend roles.
2. How often it comes up in interviews.
3. Learning value compared with time spent. Boilerplate scores low even when it's backend work.

The slice score sets the overall emphasis, and each task's score is what applies in practice. Harness, retrieval, tracing and eval work scores 4 or 5. React UI, Docker, deployment and config score 1 or 2. Ike can override any score.

# In OpenSpec

Decided at the start of slice 0: the rules live as `context` and per-artifact `rules` in `openspec/config.yaml`, so every proposal and task list states its scores, puts a failing-test task before each code task and marks the hand-off at 4 and 5.[^openspec]

[^ike-2026-11-22]: Ike: "I prefer to divide the app into vertical slices... before the vertical slices can be written, [I] prefer to do a contract-first approach... it's also important that we leverage TDD for all code written... each slice and task within the slice will get a score from 1-5... the goal being to actually have me develop code for tasks that are very marketable for AI engineering/BE roles."
[^scale]: Ike accepted the proposed 1 to 5 scale ("sure, this works for me").
[^handoff]: Ike: "i don't want to write most of the code... i don't want to have to write everything for scores of 4 or 5 even... maybe i can start by writing the code for all 4s and 5s, but once i've gotten a hang of it, i can delegate AI to write the rest of it for that task."
[^openspec]: Ike chose config.yaml rules over a custom OpenSpec schema or no encoding (2026-11-22).
