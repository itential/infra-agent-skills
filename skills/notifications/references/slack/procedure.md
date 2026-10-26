# Slack — Send a Message Procedure

Posts a new message into a Slack channel, private group, direct message, or as a reply within an
existing thread, using the Web API's `chat.postMessage` method. Covers creating a new message only —
not `chat.postEphemeral` (a message visible to a single member only), not editing or deleting a
message already sent, and not channel/user lookup itself (this procedure assumes the caller already
has, or can resolve, a valid destination identifier).

Sources: Slack's own Web API reference for `chat.postMessage`
(https://docs.slack.dev/reference/methods/chat.postMessage, redirected from the legacy
`api.slack.com/methods/chat.postMessage` path — retrieved 2026-09-29) and Slack's own Web API rate
limits page (https://docs.slack.dev/apis/web-api/rate-limits, retrieved 2026-09-29).

## Operational procedure

1. **Resolve the destination.** `chat.postMessage` takes a single `channel` value that can be a
   public channel, private channel, or a user ID for a direct message — Slack accepts either the
   channel's ID or, for some destinations, its name, but an ID is the more reliable form to pass
   once resolved. To post into a user's own App Home surface instead of a normal
   channel/DM, pass that user's ID as `channel`. If the target destination hasn't been resolved
   yet (e.g. only a human-readable channel name was given), that lookup is a separate capability,
   not part of this procedure.
2. **Decide plain text vs. structured content.** Always populate `text` — it's the fallback shown in
   notifications and to clients that can't render richer content, and Slack's own guidance treats it
   as the primary body whenever `blocks` isn't used. If richer formatting (buttons, sections, images
   laid out beyond inline markdown) is needed, build a Block Kit `blocks` array in addition to `text`
   — don't substitute `blocks` for `text` entirely.
3. **Decide whether this is a new message or a thread reply.** To reply within an existing thread,
   include `thread_ts` set to the parent message's own timestamp value (not the timestamp of another
   reply in that thread). Set `reply_broadcast` to true only if the reply should also surface in the
   main channel view, not just the thread — this is a visibility choice worth confirming with the
   caller's intent rather than defaulting it on.
4. **Only override the sending identity if the integration is meant to look like a specific bot
   persona for that one message.** `username`, `icon_emoji`, and `icon_url` only take effect for a
   token/app with the `chat:write.customize` scope in addition to `chat:write` — a standard bot
   token without that scope will have these fields silently ignored, so don't rely on them to
   confirm identity-override behavior actually worked without checking the app's granted scopes
   first.
5. **Stop and confirm with the operator before proceeding** — confirm the resolved destination and
   the message content; the message reaches its audience as soon as it is posted.
6. **Submit the call** against `chat.postMessage` with an authenticated token carrying `chat:write`
   (plus `chat:write.customize` if step 4 applies). See `endpoints.md` for the literal request shape.
7. **Confirm delivery using the `ok` field, not just a 2xx HTTP status.** A response can be HTTP 200
   and still carry `"ok": false` with an `error` string — treat that as the authoritative pass/fail
   signal. On failure, report the literal `error` value (e.g. `channel_not_found`, `not_in_channel`,
   `no_permission`, `invalid_blocks`, `too_many_attachments`, `no_text`) rather than a generic
   failure message, since the caller needs that string to decide how to react.
8. **Handle rate limiting explicitly.** If the response is HTTP 429 (or `ok:false` with
   `error: "rate_limited"`), read the `Retry-After` header — Slack's own documentation states this
   header carries the number of seconds to wait before the next attempt on that same method — and
   wait at least that long before retrying. Don't retry on a fixed short interval regardless of what
   `Retry-After` says.

## Patterns

- **`chat.postMessage` sits in Slack's own "Special" rate-limit tier**, separate from the general
  Tier 1–4 buckets that cover most other Web API methods: Slack's guidance describes roughly one
  message per second per channel as the sustained ceiling, with limited burst tolerance — pace
  repeated sends to the same channel accordingly, and don't assume a Tier 1–4 number applies here.
- **`text` and `blocks` are complementary, not either/or** — always set `text` even when sending
  `blocks`, since it's what shows in previews, push notifications, and any client that can't render
  Block Kit.
- **A destination identifier resolved once should be reused, not re-derived per call** — if the
  caller already resolved a channel name to an ID earlier in a workflow, reuse that ID rather than
  passing the name again on every subsequent send.

## Known limitations

- Covers only sending a new message or thread reply via `chat.postMessage`. Ephemeral messages
  (`chat.postEphemeral`), editing a previously sent message, deleting a message, and destination
  lookup/creation (resolving a channel name to an ID, opening a new DM conversation) are separate
  capabilities not covered here.
- Identity-override fields (`username`, `icon_emoji`, `icon_url`) depend on the calling app/token
  having `chat:write.customize` — confirm the token's granted scopes before promising this will take
  effect (see step 4).
- The rate-limit guidance above is what Slack documents publicly; actual throughput can be lower in
  practice for a given workspace/app combination — always honor `Retry-After` over an assumed fixed
  rate.
- This procedure does not cover repeated sending to guarantee eventual human read — `ok: true` means
  Slack accepted and queued the message for delivery to the destination, not that a person has seen
  it.

## Tools

| Operation | Description | Category |
|---|---|---|
| `chat.postMessage` | Post a new message (or thread reply) to a channel, group, or DM | Messaging |

## Verification checklist

- [ ] Destination (`channel`) resolved to a valid channel/group/user ID before the call, not left as
      an unresolved display name
- [ ] Operator confirmed the destination and content before the call
- [ ] `text` was populated even when `blocks` was also sent
- [ ] If replying in a thread: `thread_ts` references the thread's original parent message, not
      another reply
- [ ] Response's `ok` field checked, not just the HTTP status code
- [ ] On failure, the literal `error` string from the response was surfaced to the caller
- [ ] On HTTP 429 / `rate_limited`, the `Retry-After` header value was honored before any retry
