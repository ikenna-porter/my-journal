# Spec Delta

## Purpose

Defines the HTTP contract for searching a user's own entries by meaning, so the user can find relevant entries without remembering the exact words they used.

## ADDED Requirements

### Requirement: Search by meaning
`POST /api/v1/search` SHALL accept `query` (1 to 1,000 characters), `limit` (1 to 50, default 10) and optional filters `written_from`, `written_to` and `mood`. It SHALL respond `200` with a `results` list ranked most relevant first, drawn only from the authenticated user's entries.

#### Scenario: Results link to entries
- **WHEN** an authenticated user searches for "feeling stuck at work"
- **THEN** each result includes `entry_id`, the entry's `title` and `written_at`, a `snippet` from the matching chunk and a relevance `score`, ordered by descending relevance

#### Scenario: Only the user's own entries
- **WHEN** user A searches
- **THEN** no result comes from an entry owned by another user

#### Scenario: Date filter
- **WHEN** a user searches with `written_from` and `written_to` set to last spring
- **THEN** every result's `written_at` falls within that range

#### Scenario: Nothing relevant
- **WHEN** a user searches and nothing in their journal matches
- **THEN** the API responds `200` with an empty `results` list

### Requirement: Query text stays out of URLs
Search SHALL take its query in the request body, never in the URL, so query text does not appear in access logs.

#### Scenario: Query as a URL parameter
- **WHEN** a client sends `GET /api/v1/search?q=...`
- **THEN** the API responds `405` with `code` `method_not_allowed`

### Requirement: Search results do not paginate
Search SHALL return only the top `limit` results and SHALL NOT accept `offset`.

#### Scenario: Limit respected
- **WHEN** a user searches with `limit` 5 and more than 5 chunks match
- **THEN** exactly 5 results are returned

#### Scenario: Limit out of range
- **WHEN** a user searches with `limit` 0 or 51
- **THEN** the API responds `422` with `code` `validation_error`
