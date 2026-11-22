# Spec Delta

## Purpose

Defines the HTTP contract the client uses to find out whether Observation Mode produced an observation for a newly saved entry, and to rate that observation thumbs up or down.

## ADDED Requirements

### Requirement: Poll for an entry's observation
`GET /api/v1/entries/{id}/observation` SHALL report the state of Observation Mode for one of the authenticated user's entries: `202` while it is still running, `200` with the observation when one was produced, and `204` when there is none (silence). Each entry SHALL have at most one observation.

#### Scenario: Still running
- **WHEN** a user polls an entry's observation shortly after saving it
- **THEN** the API responds `202` with `{"status": "pending"}` and a `Retry-After` header of 1 second

#### Scenario: Observation produced
- **WHEN** Observation Mode met the confidence threshold for the entry
- **THEN** the API responds `200` with the observation's `id`, `entry_id`, `content`, `citations` (each with `entry_id`, `title` and `written_at` of a cited past entry), `created_at` and `feedback` (null until rated)

#### Scenario: Silence
- **WHEN** Observation Mode did not meet the confidence threshold for the entry
- **THEN** the API responds `204` with no body

#### Scenario: Unknown entry
- **WHEN** a user polls the observation of an entry that does not exist or is not theirs
- **THEN** the API responds `404` with `code` `not_found`

### Requirement: Pending ends within the latency budget
The API SHALL stop reporting `pending` for an entry no later than 8 seconds after the entry was saved. If no observation is ready by then, or generation failed, or the monthly spend limit is reached, the API SHALL respond with silence (`204`).

#### Scenario: Budget exceeded
- **WHEN** a user polls an entry's observation more than 8 seconds after saving it and no observation was produced
- **THEN** the API responds `204`

#### Scenario: Spend limit reached
- **WHEN** an entry is saved after the monthly spend limit has been reached
- **THEN** polling its observation responds `204` and the entry itself is saved normally

### Requirement: Rate an observation
`PUT /api/v1/observations/{id}/feedback` SHALL set the authenticated user's thumbs up or thumbs down on one of their observations from `{"rating": "up" | "down"}`, replacing any earlier rating, and respond `200` with the updated observation.

#### Scenario: Thumbs up
- **WHEN** a user sends `{"rating": "up"}` for their observation
- **THEN** the API responds `200` and the observation's `feedback` is `up`

#### Scenario: Change of mind
- **WHEN** a user who rated an observation `up` sends `{"rating": "down"}`
- **THEN** the observation's `feedback` is `down`

#### Scenario: Invalid rating
- **WHEN** a user sends `{"rating": "meh"}`
- **THEN** the API responds `422` with `code` `validation_error`
