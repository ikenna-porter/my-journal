---
type: Decision
title: Multi-tenant from day one, few users at first
description: v1 serves Ike and a few other people, but every table and query is scoped by user so the app can grow to many tenants.
tags: [decision, product, data, security]
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

* For now the users are Ike and possibly a few other people.[^ike-2026-11-22]
* The app is designed to support many tenants later. Every entry, chunk, embedding, observation, reflection, transcript and trace belongs to a user, and **every retrieval query is filtered by user**. One user's data must never show up in another user's results.
* The PRD's "multi-user scale infrastructure" exclusion ([PRD section 6](../product/prd.md)) is about infrastructure for high load, not about whether the app has multiple users.

[^ike-2026-11-22]: Ike: "the plan is to support multi-tenancy in time... for now it's just going to be me and maybe a few other people until the app is ready."
