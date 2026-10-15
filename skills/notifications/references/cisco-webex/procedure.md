# Cisco Webex — Send a Message Procedure

Posts a new message into a Webex space (room) or directly to a person, using the Webex REST API's
Messages resource. Covers creating a new message only — not editing a message already sent
(a separate update call), not deleting a message, and not room/person lookup itself (this procedure
assumes the caller already has, or can resolve, a valid room or person identifier).

Sources: Cisco's own Webex for Developers documentation — the Messages API overview
(https://developer.webex.com/docs/api/v1/messages, retrieved 2026-09-29), the Create a Message
reference (https://developer.webex.com/docs/api/v1/messages/create-a-message, retrieved 2026-09-29),
and Cisco's own Webex Developers blog post on rate limiting
(https://developer.webex.com/blog/rate-limiting-and-the-webex-api, retrieved 2026-09-29).

## Operational procedure

1. **Resolve the destination — a room, or a specific person.** Webex messages address a destination
   one of three ways, and exactly one should be supplied per call: a `roomId` (post into a space),
   a `toPersonId` (send a 1:1 message to a known person by their Webex identifier), or a
   `toPersonEmail` (send a 1:1 message to a person identified by email address, useful when only
   the email is known). Resolving a room name or a person's identifier from other information is a
   separate lookup capability, not part of this procedure.
2. **Decide plain text vs. formatted content.** Supply `text` for a plain-text body. If richer
   formatting is needed, supply `markdown` instead (or in addition) — Cisco's own reference
   describes `markdown` as the formatted alternative to `text`, letting the message render with
   bold/links/mentions rather than literal characters. Both fields share the same documented maximum
   message length.
3. **Attach a file or a card, if the message needs one.** `files` takes a publicly reachable URL to
   a single file to include (only one file per message is supported); `attachments` carries a
   structured card payload (e.g. an Adaptive Card object) for interactive content beyond plain
   text/markdown. These are independent of each other — use whichever the caller's content actually
   requires, not both by default.
4. **Decide whether this is a new message or a threaded reply.** To reply within an existing
   conversation thread in a room, set `parentId` to the identifier of the message being replied to.
   Omit it for a new, top-level message.
5. **Submit the call** with a Bearer token authorized for the target Webex org/user. See
   `endpoints.md` for the literal request shape.
6. **Confirm delivery from the HTTP status and response body.** A successful create returns the full
   message object, including the server-assigned message `id` — treat receipt of that object as
   confirmation the message was accepted. Webex's documented error responses use standard HTTP
   status codes with a JSON error body; report the actual status and body content on failure rather
   than assuming a specific cause.
7. **Handle rate limiting explicitly.** On an HTTP 429 response, read the `Retry-After` header —
   Cisco's own documentation states this header gives the number of seconds to wait before the next
   request — and wait at least that long before retrying. Cisco's own guidance notes most REST
   endpoints are limited to roughly 300 requests per minute, with the Messages/People resources
   given a separate, dynamically-adjusted allowance rather than sharing that same flat number — so
   don't assume the general 300/minute figure is the exact ceiling for message posting specifically.

## Patterns

- **Exactly one destination field per call.** `roomId`, `toPersonId`, and `toPersonEmail` each
  address a different kind of destination (a space vs. a direct 1:1 conversation) — supplying more
  than one in the same call isn't a documented combined-destination behavior; pick the one that
  matches the caller's actual target.
- **`markdown` supersedes `text` for rendering when both are present** — Cisco's own reference
  treats `text` as the fallback for clients that can't render markdown, similar in spirit to how
  other chat platforms pair a plain-text fallback with a richer body.
- **One file per message.** Unlike some platforms that accept a batch of attachments, Webex's
  `files` field is documented as carrying a single file URL per message.

## Known limitations

- Covers only creating a new message or threaded reply via the Messages API's create operation.
  Editing (`PUT` on an existing message), deleting a message, listing message history, and
  room/person lookup or creation are separate capabilities not covered here.
- The maximum message length for `text`/`markdown` is a fixed byte limit Cisco documents on the
  Create a Message reference — content exceeding it must be trimmed or split by the caller before
  this procedure's call step, since there's no documented server-side truncation behavior to rely
  on.
- The Messages/People resource's exact per-minute cap is not a fixed published number — Cisco's own
  guidance describes it as dynamically adjusted, separate from the general ~300 requests/minute
  figure that applies to most other endpoints. Don't hardcode a specific request-per-minute value
  for messages; rely on the `Retry-After` header when a 429 actually occurs instead.
- This procedure does not cover confirming a human has read the message — a successful create
  response means Webex accepted and stored the message, not that a recipient has seen it.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create a Message | Post a new message (or threaded reply) to a room, or directly to a person | Messaging |

## Verification checklist

- [ ] Exactly one destination field (`roomId`, `toPersonId`, or `toPersonEmail`) was set, matching
      the caller's intended target
- [ ] `text` and/or `markdown` populated with content within the documented length limit
- [ ] If replying within a thread: `parentId` references the correct existing message
- [ ] Response status and returned message object (including its `id`) checked to confirm creation,
      not just that the call didn't error at the transport level
- [ ] On HTTP 429, the `Retry-After` header value was honored before any retry
