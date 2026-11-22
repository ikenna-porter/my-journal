# Spec Delta

## Purpose

Defines the HTTP contract for Conversation Mode: starting an Observation Reply or Direct Conversation about an entry, sending messages, receiving streamed replies, and resuming a conversation while its transcript exists.

## ADDED Requirements

### Requirement: Start a conversation
`POST /api/v1/conversations` SHALL start a conversation about one of the authenticated user's entries from `entry_id` and an optional `observation_id`. With `observation_id` it SHALL be an Observation Reply; without it, a Direct Conversation. It SHALL respond `201` with the conversation and SHALL NOT call the LLM.

#### Scenario: Direct Conversation
- **WHEN** a user posts `{"entry_id": "<id>"}`
- **THEN** the API responds `201` with the conversation's `id`, `entry_id`, `kind` `direct_conversation`, `observation_id` null, `created_at` and `expires_at` 30 days later

#### Scenario: Observation Reply
- **WHEN** a user posts an `entry_id` and the `observation_id` of that entry's observation
- **THEN** the API responds `201` with `kind` `observation_reply` and that `observation_id`

#### Scenario: Observation from a different entry
- **WHEN** a user posts an `observation_id` that does not belong to the given `entry_id`
- **THEN** the API responds `422` with `code` `validation_error`

#### Scenario: Unknown entry
- **WHEN** a user posts an `entry_id` that does not exist or is not theirs
- **THEN** the API responds `404` with `code` `not_found`

### Requirement: Send a message and stream the reply
`POST /api/v1/conversations/{id}/messages` SHALL take an optional `content` (1 to 10,000 characters) and respond `200` with `text/event-stream`, streaming the AI's reply as server-sent events.

#### Scenario: Direct Conversation opens with the AI
- **WHEN** the first message of a Direct Conversation is sent with no `content`
- **THEN** the stream carries the AI's opening reply, which summarizes related past entries and cites them

#### Scenario: Observation Reply opens with the user's response
- **WHEN** the first message of an Observation Reply is sent without `content`
- **THEN** the API responds `422` with `code` `validation_error`

#### Scenario: Later turns need content
- **WHEN** a message after the first turn is sent without `content`
- **THEN** the API responds `422` with `code` `validation_error`

#### Scenario: One reply at a time
- **WHEN** a message is sent while the previous reply in the same conversation is still streaming
- **THEN** the API responds `409` with `code` `conflict`

### Requirement: Stream event types
The reply stream SHALL use these named events, each with a JSON `data` payload described in the contract: `message.delta` (`text`), `tool.started` (`name`), `message.completed` (`message_id`, full `content`, `citations`), and `error` (a problem object). Every stream SHALL end with exactly one `message.completed` or one `error`.

#### Scenario: Successful reply
- **WHEN** the AI replies without failure
- **THEN** the client receives zero or more `message.delta` and `tool.started` events followed by one `message.completed` whose `content` equals the concatenated deltas

#### Scenario: Failure mid-stream
- **WHEN** the reply fails after streaming has started
- **THEN** the stream ends with one `error` event and no `message.completed`

### Requirement: Spend limit blocks AI replies
When the monthly spend limit has been reached, sending a message SHALL respond `503` with `code` `spend_limit_reached` before any stream starts. Starting and reading conversations SHALL keep working.

#### Scenario: Limit reached
- **WHEN** a user sends a message after the monthly spend limit is reached
- **THEN** the API responds `503` problem+json with `code` `spend_limit_reached` and no event stream

### Requirement: Read and resume a conversation
`GET /api/v1/conversations/{id}` SHALL return one of the authenticated user's conversations with its transcript (`messages`, each with `id`, `role` `user` or `assistant`, `content`, `citations` and `created_at`). `GET /api/v1/conversations` SHALL list the user's unexpired conversations, offset-paginated and optionally filtered by `entry_id`.

#### Scenario: Resume within 30 days
- **WHEN** a user reads a conversation before its `expires_at`
- **THEN** the API responds `200` with every message so far, and the user can send another message

#### Scenario: Filter by entry
- **WHEN** a user lists conversations with `entry_id` set
- **THEN** only that entry's unexpired conversations owned by the user are returned

### Requirement: Transcripts expire after 30 days
After a conversation's `expires_at`, reading it or sending it a message SHALL respond `410` with `code` `conversation_expired`, and it SHALL no longer appear in the list.

#### Scenario: Expired conversation
- **WHEN** a user reads a conversation 31 days after it started
- **THEN** the API responds `410` with `code` `conversation_expired` and no transcript

### Requirement: Transcripts stay out of the journal
Conversation transcripts SHALL be returned only by the conversation endpoints, never by entry or search endpoints.

#### Scenario: Entry read after a conversation
- **WHEN** a user reads an entry that has had a conversation
- **THEN** the response contains no transcript messages, only any Collaborative Reflection saved for it
