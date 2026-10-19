# SendGrid — Send an Email Procedure

Sends one email message (optionally personalized per recipient group) through SendGrid's v3 Mail Send
API. Covers sending only — not template authoring, contact or list management, suppression handling,
delivery analytics, or sender verification setup.

Sources: Twilio SendGrid's own Mail Send reference
(https://www.twilio.com/docs/sendgrid/api-reference/mail-send/mail-send, retrieved 2026-10-19) and its
v3 rate-limit page
(https://www.twilio.com/docs/sendgrid/api-reference/how-to-use-the-sendgrid-v3-api/rate-limits,
retrieved 2026-10-19). The SendGrid spec in `itential/assets` was used only to choose the operation; it
is a secondary source and no fact here rests on it alone.

## Operational procedure

1. **Resolve the destination.** Recipients are email addresses, supplied as one or more personalization
   entries, each with at least one `to` address (optionally cc and bcc). There is no channel or thread
   concept. A single request may carry up to 1,000 personalization entries, and up to 1,000 cc and
   1,000 bcc recipients per entry.
2. **Choose the sender.** The `from` address must be a sender verified in the account. Setting up that
   verification is out of scope.
3. **Provide the subject and content.** A subject is required (at message or personalization level).
   Content needs at least one MIME type entry: plain text, HTML, or both. HTML is the richer format;
   its rendering depends on the recipient's mail client, not on SendGrid.
4. **Respect the documented limits.** Attachments are base64 encoded; the oversized-payload case returns
   HTTP 413. A scheduled send cannot be more than 72 hours ahead (scheduling is otherwise out of
   scope). Custom arguments and substitutions are limited to 10,000 bytes per personalization.
5. **Submit the send call** with an API key. See `endpoints.md`.
6. **Treat HTTP 202 as "accepted for processing", not delivered.** The source states 202 means queued
   for processing and delivery is not guaranteed. This procedure has no delivery confirmation; delivery
   events come from SendGrid's separate event reporting, which is out of scope.
7. **Report failures by status.** Documented: 400 (invalid request format), 401 (missing or invalid
   authorization), 403 (forbidden), 413 (payload too large), 500 (server error). Surface the response
   body to the caller.
8. **Handle rate limiting.** Every v3 response carries three rate-limit headers (limit, remaining,
   reset time as a Unix timestamp). Exceeding an endpoint's limit returns HTTP 429 with remaining at 0,
   and no further requests to that endpoint succeed until the reset time. The source does not state a
   Mail Send-specific limit — consult SendGrid support or platform-specific guidance — and does not
   document a `Retry-After` header; wait until the reset timestamp instead.

## Patterns

- **Batch recipients into one request** with multiple personalizations rather than many calls, within
  the 1,000-entry limit, to stay clear of rate limits.
- **Check the remaining-requests header proactively** instead of waiting for a 429.

## Known limitations

- Email only; no channel, thread, or chat destination.
- No delivery confirmation in this procedure; 202 is acceptance only.
- Mail Send-specific rate limits and the regional (EU) account selection rules beyond the base URL are
  not stated in the sources.
- Does not cover templates, contacts, suppressions, analytics, or sender verification.
- An email, once accepted for sending, cannot be recalled by this procedure.

## Tools

| Operation | Description | Category |
|---|---|---|
| Send mail | Queue one email request with one or more personalizations | Messaging |

## Verification checklist

- [ ] Every personalization has at least one `to` address, and the request is within the 1,000-entry
      limit
- [ ] `from` is a verified sender and a subject and at least one content entry were supplied
- [ ] HTTP 202 was reported as accepted, not delivered
- [ ] On failure, the status code and response body were surfaced
- [ ] On HTTP 429, the caller waited until the reset time from the rate-limit headers
