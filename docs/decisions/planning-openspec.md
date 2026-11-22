---
type: Decision
title: "Planning workflow: OpenSpec"
description: Features are planned as OpenSpec changes (proposal, design, specs, tasks) before implementation.
tags: [decision, planning, openspec]
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

The application is planned with **OpenSpec**.[^ike-2026-11-22] Each piece of work starts as an OpenSpec change made up of `proposal.md`, `design.md`, specs and `tasks.md`, and implementation begins only after that.

# Relationship to docs/

* OpenSpec artifacts live in `openspec/`, the tool's own directory, and follow OpenSpec's format.
* `docs/` holds long-lived knowledge: architecture, decisions and brainstorms. When an OpenSpec change settles a decision, record it here as a `Decision` doc.

# Setup status

Set up on 2026-11-22:

* The `openspec` CLI v2.1.1 is installed globally with npm (`@fission-ai/openspec`).
* The skills are installed globally (`--scope global`) in `~/.agents/skills/` and symlinked into `~/.claude/skills/`, so every project on the machine can use them: `openspec-propose`, `openspec-explore`, `openspec-apply-change`, `openspec-update-change`, `openspec-sync-specs` and `openspec-archive-change`.
* This repo was initialized with `openspec init --tools claude --scope global`, which created `openspec/config.yaml` (schema: `spec-driven`), `openspec/specs/` and `openspec/changes/`.

[^ike-2026-11-22]: Ike: "we will be using them to help us plan out this application."
