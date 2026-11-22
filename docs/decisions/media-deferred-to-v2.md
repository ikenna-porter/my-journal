---
type: Decision
title: Voice notes and photos move to v2
description: v1 is text-only. Voice notes (Whisper transcription) and photo attachments move to v2, so v1 focuses on writing, observations and conversations.
tags: [decision, product, scope, media]
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

**v1 entries are text only (Markdown).** Voice notes and photo attachments move to **v2**.[^ike-2026-11-22]

| Feature | Was | Now |
|---|---|---|
| Voice notes + self-hosted Whisper transcription | v1 | v2 |
| Photo attachments (upload, store, display) | v1 | v2 |
| AI vision / photo understanding | v2 | v2 (unchanged) |
| Video | out of scope | out of scope (unchanged) |

# Why

Recording in the browser, file storage, running Whisper on a CPU-only VPS, and uploading and displaying photos add a lot of work that doesn't touch the AI layer. Transcription would also add delay before chunking, which competes with the observation latency budget (see [Observation Mode](observation-mode.md)).

# Consequences

* v1 has no file storage, so the PRD's VPS storage and Cloudflare R2 plan isn't needed until v2.
* The existing `media` table in the old Prisma schema isn't needed in v1.
* v1 should not rule out media later. The v2 design will have voice transcripts flow through the same chunking pipeline as text.

[^ike-2026-11-22]: Ike: "let's move voice and photos to v2."
