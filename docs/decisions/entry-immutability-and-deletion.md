---
type: Decision
title: Entries are immutable, and deletion cascades to everything derived from them
description: Entries can't be edited, only deleted. Deleting an entry removes its chunks and embeddings plus every reflection, observation, transcript and trace that references it.
tags: [decision, product, privacy, data]
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

**Entries can't be edited.** Like a paper journal, you don't go back and change what you wrote. A user can **delete** an entry.[^immutable]

**The timestamp is set automatically, and the user can change it only while writing**, for example to backdate an entry about last Tuesday. Once the entry is saved, the timestamp is fixed like the rest of the entry. Date filters such as "last spring" use this timestamp, so it should reflect when things happened.[^timestamp]

**Deletion cascades** to everything derived from the entry:[^cascade]

```
  delete Entry Y
     |
     +--> Y's chunks and embeddings
     +--> reflections attached to Y
     +--> reflections on OTHER entries that cite Y
     +--> observations that cited Y
     +--> conversation transcripts that retrieved Y
     +--> Langfuse traces that retrieved Y
```

# Why

Journals hold sensitive information. If a user deletes something, we have to trust they have a reason. Keeping its content inside reflections, observations, transcripts or traces would break that trust. Reflections on other entries that mention Y are deleted even though this loses the user's thoughts about those other entries.

# Requirements this creates

* Every reflection, observation, conversation transcript and Langfuse trace must record the IDs of the entries it used or cites, so a delete can find all of them.
* Deletion of Langfuse traces goes through Langfuse's API.

# Not affected

* Nothing can take back an observation the user has already seen. The rule is that nothing **new** is generated from a deleted entry's text, and that every stored derivative is removed.

[^immutable]: Ike: "entries cannot be edited. a user can choose to delete an entry if they wish... the important part is that new observations are not based on text that has been deleted."
[^cascade]: Ike: "we should cascade the delete to include all reflections that reference the deleted entry", then agreed to extend this to observations, transcripts and traces.
[^timestamp]: Ike chose option 1 (editable only while writing) over never editable or editable after saving.
