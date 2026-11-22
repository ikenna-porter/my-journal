---
type: Agent Instructions
title: Instructions for Claude sessions in my-journal
description: How every Claude session should work in this repo, at any stage.
---

# Working in my-journal

my-journal is a journaling app with an AI layer: Observation Mode, Conversation Mode and Collaborative Reflection, all built on hand-built retrieval over the user's own entries. Its main purpose is to build Ike's **AI engineering** skills (loop engineering, observability, evals) for the job search. Design choices put those skills first.

## Read first

1. `docs/index.md` lists every doc.
2. `docs/product/roadmap.md` gives the build order (slice 0, the API contract, then five vertical slices). Find the slice you're working on.
3. `docs/decisions/development-methodology.md` explains how every task is built.
4. `docs/product/glossary.md` defines the terms you must use.

Before surveying the repo, run `git fetch`. Local copies have been stale before.

## Which doc wins

* **Decision docs in `docs/decisions/` override the PRD** (`docs/product/prd.md`). The PRD is kept in sync with them.
* `docs/brainstorming/` is never authoritative.
* When a decision changes a feature, update the PRD in the same change and link the decision from it.

## Vocabulary

Use the glossary's terms exactly, in docs, specs, UI labels and code. Say **conversation**, never "chat". Say **Observation Reply** and **Direct Conversation**, never "Path A/B". Say **Collaborative Reflection** (or **reflection**), never "summary". Add new terms to the glossary first.

## How work is done

* **Contract first.** The API contract (slice 0) is designed before the slices are built.
* **Vertical slices.** Each slice is one OpenSpec change. Plan it with the `openspec-propose` skill and build it with `openspec-apply-change`. Don't start the next slice until the current one passes its end-to-end tests.
* **TDD always.** A failing test comes before the code that makes it pass.
* **Hands-on scores (1 to 5)** on every slice and task decide who writes the tests and code. At **4 and 5**, Ike writes the core until he has the pattern, then says "take over", and Claude finishes in the same style. Never write code Ike is meant to write before he hands off.
* **Explain all code you write**, sized to its score: a short summary at 1, a line-by-line walkthrough at 2 or above.
* **High-level design decisions are Ike's**: technology, data model, API design, the shape of the harness, what goes into context. Lay out the options, the trade-offs and a recommendation, one decision at a time. Code-level details are Claude's call; say what was chosen and why in a line or two.
* **Record every key decision** in `docs/decisions/` as its own doc, add it to `docs/index.md`, and add a dated entry at the top of `docs/log.md`.

## Docs format: OKF v0.3

Every doc in `docs/` is Markdown with YAML frontmatter that has at least a `type`, plus `title`, `description`, `status` and `generated` (see `docs/decisions/documentation-okf.md`). Cite sources with footnotes. Diagrams go in Mermaid code blocks or ASCII, inside `.md` files.

## Current state

The repo still has the original Express + Prisma backend (TypeScript). It's being **replaced** by Python + FastAPI + SQLAlchemy/Alembic, starting in slice 1. Don't build on the Express code. The frontend is React + TypeScript (Vite).

## Privacy

* Never commit real journal entries, database dumps or `.env` files. Evals use a **synthetic** journal only.
* Never log raw entry text to stdout or general logs. Entry text goes only to the LLM provider and to self-hosted Langfuse traces.

## Git and GitHub

* Remote: `git@github.com:ikenna-porter/my-journal.git` (public). Push over **SSH** with `git push origin <branch>`.
* Commit or push only when Ike asks.
* Don't change the repo's git author config.
