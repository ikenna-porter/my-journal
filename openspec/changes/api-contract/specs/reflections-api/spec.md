# Spec Delta

## Purpose

Defines the HTTP contract for closing a conversation with an optional Collaborative Reflection, written by the user or drafted by the AI and approved by the user, which is saved permanently on the entry.

## ADDED Requirements

### Requirement: Draft a reflection with the AI
`POST /api/v1/conversations/{id}/reflection/draft` SHALL return an AI-drafted reflection of one of the authenticated user's conversations as `{"content": ...}` with `200`. The draft SHALL NOT be saved.

#### Scenario: Draft is not saved
- **WHEN** a user requests a draft and then reads the conversation's entry
- **THEN** the entry's `reflections` list does not contain the draft

#### Scenario: Nothing to reflect on
- **WHEN** a user requests a draft for a conversation that has no messages
- **THEN** the API responds `409` with `code` `conflict`

#### Scenario: Spend limit reached
- **WHEN** a user requests a draft after the monthly spend limit is reached
- **THEN** the API responds `503` with `code` `spend_limit_reached`

### Requirement: Save a reflection
`PUT /api/v1/conversations/{id}/reflection` SHALL save the conversation's Collaborative Reflection from `content` (1 to 5,000 characters) and `source` (`user` or `ai_draft`), responding `201` the first time and `200` when it replaces an earlier one. A conversation SHALL have at most one reflection.

#### Scenario: User-written reflection
- **WHEN** a user saves a reflection with `source` `user`
- **THEN** the API responds `201` with the reflection's `id`, `conversation_id`, `entry_id`, `content`, `ai_assisted` false, `cited_entry_ids` and `created_at`

#### Scenario: Approved AI draft
- **WHEN** a user saves a reflection with `source` `ai_draft`, edited or not
- **THEN** the saved reflection has `ai_assisted` true

#### Scenario: Rewrite while the transcript exists
- **WHEN** a user saves a second reflection for the same conversation before it expires
- **THEN** the API responds `200` and the conversation's entry shows only the new reflection

### Requirement: The server decides provenance
The server SHALL set `ai_assisted` from `source` and SHALL set `cited_entry_ids` from the entries the conversation cited. The request SHALL NOT be able to set either field.

#### Scenario: Client tries to set provenance
- **WHEN** a request body includes `ai_assisted` or `cited_entry_ids`
- **THEN** the API responds `422` with `code` `validation_error`

### Requirement: Reflections are permanent and optional
A saved reflection SHALL remain attached to its entry after the conversation's transcript expires, until the entry or a cited entry is deleted. Leaving a conversation without a reflection SHALL save nothing.

#### Scenario: Transcript expired
- **WHEN** a user reads an entry 31 days after a conversation that ended with a reflection
- **THEN** the reflection is still in the entry's `reflections` list

#### Scenario: Rewrite after expiry
- **WHEN** a user saves a reflection for a conversation past its `expires_at`
- **THEN** the API responds `410` with `code` `conversation_expired`

#### Scenario: No reflection
- **WHEN** a user leaves a conversation without saving a reflection
- **THEN** the entry's `reflections` list is unchanged
