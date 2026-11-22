# Spec Delta

## Purpose

Defines the HTTP contract for a user's journal entries: writing an entry, listing and reading entries, and deleting an entry along with everything derived from it.

## ADDED Requirements

### Requirement: Create an entry
`POST /api/v1/entries` SHALL create an entry owned by the authenticated user from `content` (Markdown, 1 to 100,000 characters, required), `title` (up to 200 characters, optional), `mood` (up to 32 characters, optional) and `written_at` (optional, defaults to the time of saving). It SHALL respond `201` with the entry.

#### Scenario: Minimal entry
- **WHEN** an authenticated user posts `{"content": "Today I..."}`
- **THEN** the API responds `201` with an entry that has an `id`, the content, `title` null, `mood` null, `written_at` equal to the save time and `created_at`

#### Scenario: Backdated entry
- **WHEN** an authenticated user posts an entry with `written_at` set to last Tuesday
- **THEN** the saved entry's `written_at` is last Tuesday and its `created_at` is the save time

#### Scenario: Timestamp in the future
- **WHEN** a user posts an entry with `written_at` later than the current time
- **THEN** the API responds `422` with `code` `validation_error`

#### Scenario: Empty content
- **WHEN** a user posts an entry with empty or missing `content`
- **THEN** the API responds `422` with `code` `validation_error`

### Requirement: Entries are immutable
An entry SHALL NOT be changed after it is saved, including its `written_at`. The API SHALL NOT offer any operation that edits an entry.

#### Scenario: Attempt to edit
- **WHEN** a client sends `PUT` or `PATCH` to `/api/v1/entries/{id}`
- **THEN** the API responds `405` with `code` `method_not_allowed`

### Requirement: List entries
`GET /api/v1/entries` SHALL return the authenticated user's entries, newest `written_at` first, as an offset-paginated list. Each item SHALL include `id`, `title`, `mood`, `written_at` and a `preview` of at most the first 200 characters of `content`.

#### Scenario: Newest first
- **WHEN** a user with entries written on Monday and Wednesday lists entries
- **THEN** Wednesday's entry comes before Monday's

#### Scenario: Only the user's own entries
- **WHEN** user A lists entries
- **THEN** no entry owned by any other user appears and `total` counts only user A's entries

### Requirement: Read an entry
`GET /api/v1/entries/{id}` SHALL return one of the authenticated user's entries with its full `content` and the Collaborative Reflections attached to it.

#### Scenario: Entry with a reflection
- **WHEN** a user reads an entry whose conversation was closed with a reflection
- **THEN** the response includes the entry and a `reflections` list containing that reflection

#### Scenario: Unknown entry
- **WHEN** a user reads an entry ID that does not exist or is not theirs
- **THEN** the API responds `404` with `code` `not_found`

### Requirement: Delete an entry
`DELETE /api/v1/entries/{id}` SHALL permanently delete one of the authenticated user's entries and respond `204`.

#### Scenario: Delete then read
- **WHEN** a user deletes an entry and then reads it
- **THEN** the delete responds `204` and the read responds `404`

#### Scenario: Delete twice
- **WHEN** a user deletes an entry that was already deleted
- **THEN** the API responds `404` with `code` `not_found`

### Requirement: Deletion cascades through the API
After an entry is deleted, no API response SHALL contain it or anything derived from it: its chunks, its reflections, reflections on other entries that cite it, observations that cited it, and conversations whose transcripts retrieved it.

#### Scenario: Gone from search
- **WHEN** a user deletes an entry and then searches for words from it
- **THEN** no search result refers to the deleted entry

#### Scenario: Citing reflection removed
- **WHEN** a user deletes entry Y and a reflection on entry X cites Y
- **THEN** reading entry X no longer includes that reflection

#### Scenario: Citing observation removed
- **WHEN** a user deletes entry Y and an observation on entry X cited Y
- **THEN** polling entry X's observation responds as silence (`204`)

#### Scenario: Conversation that retrieved it removed
- **WHEN** a user deletes an entry that a conversation's transcript retrieved
- **THEN** reading that conversation responds `404` with `code` `not_found`
