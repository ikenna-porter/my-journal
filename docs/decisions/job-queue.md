---
type: Decision
title: Job queue - Celery with RabbitMQ
description: Background jobs such as entry ingestion run as Celery tasks, with RabbitMQ as the broker. It runs on the VPS and can move to its own machine later.
tags: [decision, infrastructure, queue, ingestion]
status: stable
generated:
  by: claude-code/claude-opus-5-5
  at: "2026-11-22T19:20:00Z"
sources:
  - id: ike-2026-11-22
    resource: process:planning-session
    author: human:ike
    title: Planning conversation with Ike, 2026-11-22
---

# Decision

* **Worker library: Celery.** Ike writes the job functions, such as `ingest_entry` (chunk, embed, store). Celery runs the worker processes, pulls jobs, acknowledges or retries them, and handles timeouts and periodic jobs.[^ike-2026-11-22]
* **Broker: RabbitMQ.** It holds and delivers jobs. Durable queues and acknowledgements mean a job isn't lost if a worker crashes.
* **Retries:** failed jobs retry up to 3 times with backoff, then fail gracefully, as the [PRD](../product/prd.md) requires (section 4.1).
* **Deployment:** RabbitMQ runs as a container on the VPS. Workers and the broker are reached through addresses set in config, so either can move to another machine later (see [Hosting](hosting.md)).

# Why

* Celery is the most widely used Python task queue and RabbitMQ is a standard dedicated broker, so both are marketable.
* The worker library is plumbing, so per [Build vs library](build-vs-library.md) it comes from a library. The job logic is hand-written.
* Redis as a broker was rejected because it can lose queued jobs in a crash unless its disk persistence is configured. A Postgres-based queue was the other option considered.

# Open

* **Saving an entry and queuing its job happen in two systems.** If the entry saves to Postgres but enqueueing to RabbitMQ fails, the entry is never embedded. Options include a periodic sweep that re-queues entries with no chunks, or an outbox table. Decide when designing ingestion.[^gap]

[^ike-2026-11-22]: Ike: "yes celery and rabbitmq."
[^gap]: Ike: "leave this as an open question that we'll address when we get to that particular feature."
