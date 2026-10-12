# Endpoints — Cisco Webex Messages API

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever HTTP
client/adapter is assumed available. Sources: Cisco's Webex for Developers Messages API overview
(https://developer.webex.com/docs/api/v1/messages, retrieved 2026-09-29), the Create a Message
reference (https://developer.webex.com/docs/api/v1/messages/create-a-message, retrieved 2026-09-29),
and the base API path confirmed against Cisco's own REST API Basics documentation
(https://developer.webex.com/docs/rest-api-basics, retrieved 2026-09-29 via search, page itself did
not render fully for direct extraction — cross-checked against the vendor's published OpenAPI
description for the Messages resource, which also targets this same base path).

## Create a Message

**Method/URL:**

```
POST https://webexapis.com/v1/messages
```

**Authentication:** `Authorization: Bearer <access_token>` header.

**Content type:** `application/json`.

**Body fields:**

| Field | Required | Notes |
|---|---|---|
| `roomId` | One of `roomId`/`toPersonId`/`toPersonEmail` | Destination space (room) identifier. |
| `toPersonId` | One of the three above | Destination person's Webex identifier, for a direct 1:1 message. |
| `toPersonEmail` | One of the three above | Destination person's email address, for a direct 1:1 message. |
| `text` | Conditionally | Plain-text message body. |
| `markdown` | Conditionally | Markdown-formatted message body; takes rendering precedence over `text` when both present. |
| `files` | No | Array containing a single publicly reachable file URL to attach. |
| `attachments` | No | Array of structured card content (e.g. an Adaptive Card object) for interactive messages. |
| `parentId` | No | Identifier of the message being replied to, for a threaded reply. |

**Success response:** HTTP 200 with a JSON body containing the created message object, including a
server-assigned `id`, the resolved `roomId`/`roomType`, `personId`/`personEmail` of the sender, the
`created` timestamp, and (if applicable) `mentionedPeople`/`mentionedGroups` and `attachments`.

**Documented error status codes** (per Cisco's Create a Message reference): `400`, `401`, `403`,
`404`, `405`, `409`, `410`, `415`, `423`, `428`, `429`, `500`, `502`, `503`, `504` — each returns a
JSON error body; Cisco's reference does not enumerate a fixed set of application-level error code
strings for this endpoint the way some other Webex resources document, so surface the actual status
and body content rather than assuming a specific cause.

**Rate limiting (429):** response includes a `Retry-After` header giving the number of seconds to
wait, per Cisco's own developer blog post on rate limiting. Example:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 3600
```

Cisco's guidance describes most REST endpoints as limited to roughly 300 requests per minute, while
noting the Messages and People resources are given a separate, dynamically-adjusted allowance rather
than sharing that flat figure exactly.
