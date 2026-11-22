# Spec Delta

## Purpose

Defines the rules every my-journal HTTP endpoint follows (base path, authentication, user scoping, error format, pagination, unbuilt-endpoint behavior) and the contract artifacts the React client and the backend share.

## ADDED Requirements

### Requirement: Versioned base path
Every application endpoint SHALL be served under the `/api/v1` path prefix. The only endpoint outside authentication is `GET /api/v1/health`.

#### Scenario: Health check without a token
- **WHEN** a client sends `GET /api/v1/health` with no `Authorization` header
- **THEN** the API responds `200` with body `{"status": "ok"}`

### Requirement: Bearer authentication on every other endpoint
Every endpoint other than health SHALL require an `Authorization: Bearer <token>` header carrying an Auth0 access token, and SHALL be declared with a bearer security scheme in the contract.

#### Scenario: Missing token
- **WHEN** a client calls any endpoint other than health without an `Authorization` header
- **THEN** the API responds `401` with a problem response whose `code` is `unauthenticated`

#### Scenario: Invalid token
- **WHEN** a client calls an authenticated endpoint with a token that fails verification
- **THEN** the API responds `401` with a problem response whose `code` is `unauthenticated`

### Requirement: Current user
The API SHALL expose `GET /api/v1/me`, returning the authenticated user's `id` and `email`. The first authenticated request from a new Auth0 identity SHALL create that user's record.

#### Scenario: Read the current user
- **WHEN** an authenticated user calls `GET /api/v1/me`
- **THEN** the API responds `200` with that user's `id` and `email`, and no other user's data

### Requirement: Resources are scoped to the authenticated user
Every endpoint that reads or changes an entry, observation, conversation or Collaborative Reflection SHALL act only on resources owned by the authenticated user. A resource owned by another user SHALL be reported exactly as if it did not exist.

#### Scenario: Another user's entry
- **WHEN** user A requests an entry, observation, conversation or reflection that belongs to user B
- **THEN** the API responds `404` with a problem response whose `code` is `not_found`, identical to the response for an ID that does not exist

### Requirement: Problem details error format
Every error response SHALL use RFC 9457 with media type `application/problem+json` and the fields `type`, `title`, `status`, `detail` and a stable machine-readable `code`. Validation errors SHALL also include an `errors` list with each field's location and message.

#### Scenario: Validation error
- **WHEN** a client sends a request body that fails validation
- **THEN** the API responds `422` with `code` `validation_error` and an `errors` list naming each invalid field

#### Scenario: Codes are part of the contract
- **WHEN** the contract is generated
- **THEN** it lists every allowed `code` value as an enumeration, including at least `unauthenticated`, `not_found`, `validation_error`, `method_not_allowed`, `conflict`, `conversation_expired`, `spend_limit_reached` and `not_implemented`

### Requirement: Offset pagination for lists
List endpoints SHALL accept `limit` (1 to 100, default 20) and `offset` (0 or more, default 0) query parameters and SHALL return `{items, total, limit, offset}`.

#### Scenario: Second page
- **WHEN** a user with 45 entries requests `limit=20&offset=20`
- **THEN** the response contains 20 items, `total` 45, `limit` 20 and `offset` 20

#### Scenario: Limit out of range
- **WHEN** a client sends `limit=500`
- **THEN** the API responds `422` with `code` `validation_error`

### Requirement: Unbuilt endpoints
Until the slice that builds an endpoint is complete, that endpoint SHALL still authenticate and validate requests exactly as the contract describes, and then SHALL respond `501` with `code` `not_implemented`.

#### Scenario: Valid request to an unbuilt endpoint
- **WHEN** an authenticated client sends a valid request to an endpoint whose slice is not built
- **THEN** the API responds `501` with a problem response whose `code` is `not_implemented`

#### Scenario: Invalid request to an unbuilt endpoint
- **WHEN** an authenticated client sends an invalid body to an endpoint whose slice is not built
- **THEN** the API responds `422` with `code` `validation_error`, not `501`

### Requirement: Committed OpenAPI contract
The repository SHALL contain the generated OpenAPI 3.1 document for the API at `contract/openapi.json`, and an automated check SHALL fail whenever the API's generated document differs from the committed one.

#### Scenario: Endpoint changed without regenerating
- **WHEN** a request or response model changes and `contract/openapi.json` is not regenerated
- **THEN** the contract drift check fails in CI

### Requirement: Generated client types
The React client SHALL use TypeScript types generated from `contract/openapi.json`, and an automated check SHALL fail when the committed types differ from what the committed contract generates.

#### Scenario: Stale client types
- **WHEN** `contract/openapi.json` changes and the client types are not regenerated
- **THEN** the client type drift check fails in CI
