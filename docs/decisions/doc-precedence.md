---
type: Decision
title: Doc precedence
description: Decision docs override the PRD, and the PRD is kept in sync with them. Brainstorms are never authoritative.
tags: [decision, docs, process]
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

When documents disagree:[^first][^second]

| Rank | Source | Covers |
|---|---|---|
| 1 | Decision docs in this folder, made in planning sessions | Anything they decide, both features and tech |
| 2 | [PRD v1](../product/prd.md) | Features and user flows, plus any technical details no decision doc has replaced |
| 3 | [Glossary](../product/glossary.md) | The vocabulary every other doc must use |
| -- | [brainstorming/](../brainstorming/) | Never authoritative. Ideas only |

# Keeping them in sync

When a decision changes a feature, update the PRD in the same change so the PRD always describes the current product. Each affected PRD section links to its decision doc.

[^first]: Ike: "What the PRD says takes precedent over everything when it comes to functionality/features. the tech stack/decisions make in this chat should take precedent over what the PRD says."
[^second]: Ike, later the same day: "decisions made in our conversation now override the PRD."
