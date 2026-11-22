---
type: Decision
title: Authentication - Auth0
description: Login is handled by Auth0, a hosted auth service, chosen for its ease and resume recognition. Its free tier (about 25K MAU) far exceeds v1's needs.
tags: [decision, auth, security]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T19:45:00Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
  - id: comparison-agentdeals
    resource: https://agentdeals.dev/auth-comparison-2026
    title: "Auth & Identity Comparison 2026 (secondary source)"
  - id: comparison-highcircl
    resource: https://www.highcircl.com/en/blog/auth0-alternatives
    title: "Auth0 alternatives in 2026 (secondary source)"
---

# Decision

Authentication uses **Auth0**, a hosted auth service.[^auth0]

# Why

* It's easier than building or running auth ourselves.
* Auth0 is widely recognized, so it's more marketable on a resume than lesser-known providers.
* Its free tier, reported at about **25,000 MAU**,[^comparison] is far more than v1 needs (Ike plus a few users).

# Alternatives considered

Picking the largest free tier was considered first. That would have meant WorkOS AuthKit (about 1M MAU free). Ike chose Auth0 instead for name recognition. Supabase Auth, Clerk (about 50K) and Stytch (about 10K) were also compared.

# Privacy

Auth0 sees user emails and login events. It never sees journal entries. The FastAPI backend verifies Auth0's tokens and scopes every query to the user (see [Tenancy](tenancy.md)).

# Open

* Confirm the free-tier limits on Auth0's official pricing page before integrating. The figures above come from comparison sites.
* Which login methods to offer (email + password, magic link, Google), and how the frontend and backend handle sessions.

[^auth0]: Ike: "lets use auth0... i've heard of it and it's probably more marketable on a resume."
[^comparison]: Figures come from secondary comparison sites; see `sources`.
