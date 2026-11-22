---
type: Decision
title: "Documentation format: Open Knowledge Format"
description: All docs in this directory follow Google's Open Knowledge Format (OKF) v0.3.
tags: [decision, docs, okf]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T17:33:14Z"
sources:
  - id: okf-spec
    resource: https://raw.githubusercontent.com/open-knowledge-format/open-knowledge-format/main/SPEC.md
    title: Open Knowledge Format specification, v0.3
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# Decision

`docs/` is an OKF v0.3 bundle.[^ike-2026-11-22][^okf-spec]

# Rules for this repo

* Each doc is a Markdown file whose YAML frontmatter has at least a `type`. This repo also sets `title`, `description`, `tags`, `status` and `generated`.
* `type` values used so far: `PRD`, `Architecture Overview`, `Sequence Diagram`, `Decision`, `Brainstorm`. Diagrams are stored as Mermaid code blocks inside `.md` docs, not as separate `.mmd` files.
* Use `status: draft` for anything that isn't settled. Every brainstorming doc is a draft.
* For a retired doc, keep the file, set `status: deprecated` and add `superseded_by` with the path of the replacement.
* Actors: AI-written content uses `generated.by: claude-code/<model>`. When Ike reviews a doc, add `verified: [{by: "human:ike", at: "<timestamp>"}]`. This gives the doc the "human-reviewed" trust tier.
* Timestamps are quoted ISO 8601, either a date-time with an offset (`"2026-11-22T17:33:14Z"`) or a date (`"2026-11-22"`).
* Link with ordinary relative Markdown links. `[[wikilinks]]` are not links in OKF.
* Claims are cited with footnotes whose labels match a `sources[].id`.
* `index.md` and `log.md` are reserved names. Add every new doc to `index.md` and add a dated entry to `log.md`, with the newest entry first.

# Why

OKF is a vendor-neutral Markdown format that both people and AI agents can read. That fits a project whose purpose is learning agentic development.

[^okf-spec]: OKF v0.3, sections 3 to 9.
[^ike-2026-11-22]: Ike: "all docs should follow the open knowledge format by google."
