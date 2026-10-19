# Twilio — Send an SMS/MMS Message Procedure

Sends one outbound text message (SMS, or MMS when media is attached) to a single phone number through
Twilio's Programmable Messaging API. Covers creating a message only — not reading message history,
cancelling a scheduled message, receiving inbound messages, WhatsApp/other channel setup, or
provisioning and registering sender numbers.

Sources: Twilio's own Message resource reference
(https://www.twilio.com/docs/messaging/api/message-resource, retrieved 2026-10-19) and Twilio's own
error reference for 20429 (https://www.twilio.com/docs/api/errors/20429, retrieved 2026-10-19). The
OpenAPI spec for Twilio in `itential/assets` was used only to choose which operation to cover; it is a
secondary source and no fact here rests on it alone.

## Operational procedure

1. **Resolve the destination.** The only destination type is a single recipient addressed by phone
   number in E.164 form. There is no channel or thread concept for SMS/MMS. Resolving a person or team
   to a phone number is a separate capability, not part of this procedure. A trial account can message
   only verified recipient numbers.
2. **Choose the sender.** Provide exactly one of: a sender address owned by the account (a Twilio phone
   number or an alphanumeric sender ID where permitted), or a Messaging Service identifier that lets
   Twilio pick the sender. Which sender types are allowed for a given destination country is not stated
   in the sources — consult platform-specific guidance.
3. **Choose the content.** Provide a text body (documented limit 1,600 characters), or media
   attachments (up to 10 files; images are documented as limited to 5 MB each), or a content-template
   identifier. SMS has no rich formatting: the body is plain text and nothing is rendered as markup.
4. **Optionally set delivery controls.** A status-callback URL receives each status change. The
   validity period (1–36000 seconds, default 36000) is the longest a message may wait in Twilio's
   outgoing queue before it is dropped unsent — shorten it for time-sensitive alerts so a stale alert
   is not delivered hours late. A message-intent label may be set; documented values include
   `notifications`. Scheduling a future send is possible but is out of scope here.
5. **Submit the create-message call** with the account's credentials. See `endpoints.md`.
6. **Treat HTTP 201 as "accepted and queued", not delivered.** The initial status is `queued` (or
   `accepted` when a Messaging Service is used). Record the returned message identifier.
7. **Follow the status to a terminal state when delivery matters.** Documented outbound progression:
   queued, sending, sent (nearest upstream carrier accepted it), delivered (carrier or handset
   confirmed). Terminal failures are `undelivered` (a delivery receipt said it was not delivered) and
   `failed` (it could not be sent, e.g. queue overflow, suspended account, media error). Failed and
   undelivered messages carry an error code and message; report them verbatim. Status updates arrive
   through the status callback or by reading the message resource.
8. **Handle rate limiting.** Messages beyond the account's sending capacity are queued by Twilio rather
   than rejected. Separately, exceeding the account's concurrent REST request limit returns HTTP 429
   with error code 20429; Twilio documents that such responses are safe to retry with exponential
   backoff and that the `Twilio-Concurrent-Requests` response header shows current load. The sources
   do not document a `Retry-After` header for 20429, so do not rely on one. Reduce concurrency or queue
   requests on the caller side.

## Patterns

- **`delivered` is the only status that confirms handset or carrier confirmation**, and it is not
  guaranteed to be available for every destination ("where available" in the source). `sent` means only
  that the upstream carrier accepted it.
- **Queue time is a hidden cost for alerts.** Because over-capacity messages wait in a queue up to the
  validity period, a burst of alerts can be delivered late rather than refused; lower the validity
  period if a late message is worse than none.
- **Use a Messaging Service for large volumes**, which Twilio recommends for high-volume sending.

## Known limitations

- Single recipient per call; no channel, thread, or group destination.
- No rich formatting; MMS media support varies by destination (not stated in the sources — consult
  platform-specific guidance).
- Which error code applies to an invalid destination number is not stated in the sources.
- Does not cover scheduling, cancelling, inbound messages, sender registration, or other channels.
- Sending is billed and reaches a real person's phone; there is no recall once a message is
  delivered.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create message | Queue one outbound SMS/MMS to a phone number | Messaging |
| Fetch message | Read a message's current status and error code | Messaging |

## Verification checklist

- [ ] Destination is an E.164 phone number, and the account is allowed to message it (trial accounts:
      verified numbers only)
- [ ] Exactly one sender source and at least one content source were supplied
- [ ] Validity period was shortened where a late message would be harmful
- [ ] HTTP 201 was not reported as delivery; the status (`queued`/`accepted`) was reported as such
- [ ] When delivery matters, status was followed to `delivered`, `undelivered`, or `failed`, and any
      error code and message were surfaced
- [ ] On HTTP 429 / 20429, the caller backed off exponentially and reduced concurrency
