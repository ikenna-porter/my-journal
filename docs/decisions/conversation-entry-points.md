---
type: Decision
title: Conversation Mode entry points - Observation Reply and Direct Conversation
description: Conversation Mode has two entry points, and both are about the entry just written. In an Observation Reply the user responds to an observation; in a Direct Conversation the user starts one without an observation.
tags: [decision, product, conversation-mode, vocabulary]
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

The PRD originally called the two entry points "Path A" and "Path B". These replace them:[^names]

| Name | Was | How it starts | Opening context |
|---|---|---|---|
| **Observation Reply** | Path A | The user responds to an observation | The observation, the user's response and the new entry |
| **Direct Conversation** | Path B | The user starts a conversation without an observation | The new entry |

**Both are about the entry the user just wrote.**[^entry] The PRD's phrase "fresh conversation" meant only that no observation starts it. In both cases, the agent retrieves chunks related to the new entry, then summarizes them with links to the entries they came from, so the user can see how their thinking has changed, stagnated or improved over time.

The canonical vocabulary is in the [Glossary](../product/glossary.md).

# Out of scope

* Open-ended conversations that aren't tied to an entry, such as "how have I felt about my career this year?"

[^names]: Ike asked for a name other than "Path B" and for consistent terms with no duplicates. Claude chose these names.
[^entry]: Ike: "path B should be related to the entry the user just wrote."
