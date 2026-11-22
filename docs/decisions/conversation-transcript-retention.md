---
type: Decision
title: Conversation transcripts are kept separately for 30 days
description: Conversation transcripts are stored apart from the journal, never shown in it or retrieved, and deleted after 30 days. Langfuse traces follow the same retention. Reflections are kept permanently.
tags: [decision, product, privacy, observability]
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

This refines [PRD section 3.3](../product/prd.md), which said "the raw conversation transcript is not persisted."[^ike-2026-11-22]

* The **Collaborative Reflection** is the permanent record of a conversation.
* **Transcripts are stored separately** from the journal. They're never shown in the journal and never indexed for retrieval.
* Transcripts are **deleted automatically 30 days** after the conversation, or right away if their entry is deleted (see [Entry deletion](entry-immutability-and-deletion.md)).
* **Langfuse traces follow the same 30-day retention**, because traces contain the conversation text.

# Why

* The PRD's goal is to keep conversation noise out of the journal and keep only the meaning of each conversation. That goal concerns what the journal shows and what retrieval searches, not whether transcripts are stored at all.
* Deleting transcripts immediately would also make the Langfuse traces useless for seeing what the agent did. A 30-day window keeps that ability while the conversation is recent, and still keeps how long sensitive text is held bounded.
* While transcripts exist, a conversation can be resumed or its reflection rewritten.

[^ike-2026-11-22]: Ike chose option 3 (store, then expire) and accepted the 30-day limit.
