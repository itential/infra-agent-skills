# Endpoints — SendGrid v3 Mail Send

Literal wiring layer. `procedure.md` steps reference these by name. Source: Twilio SendGrid's Mail Send
reference (https://www.twilio.com/docs/sendgrid/api-reference/mail-send/mail-send, retrieved
2026-10-19) and rate-limit page
(https://www.twilio.com/docs/sendgrid/api-reference/how-to-use-the-sendgrid-v3-api/rate-limits,
retrieved 2026-10-19). The `itential/assets` spec is a secondary source and was not relied on.

## Send mail

```
POST https://api.sendgrid.com/v3/mail/send
```

Regional (EU) subusers use `https://api.eu.sendgrid.com/v3/mail/send`.

**Authentication:** `Authorization: Bearer <API key>`.

**Body fields (JSON):**

| Field | Required | Notes |
|---|---|---|
| `personalizations` | Yes | Array, up to 1,000 entries; each needs at least one `to` address. Cc/bcc up to 1,000 each per entry. |
| `from` | Yes | Object with an email address; must be a verified sender. |
| `subject` | Yes | At message or personalization level; at least 1 character. |
| `content` | Yes | Array with at least one entry whose type is plain text or HTML. |
| `attachments` | No | Base64 encoded content. |
| `categories` | No | Up to 10 unique categories. |
| `send_at` | No | Scheduled send; cannot be more than 72 hours ahead. Out of scope here. |

Assumption: element names inside `to`, `from` and `content` entries (`email`, `type`, `value`) were
not on the page retrieved; verify against the reference before use.

**Success:** HTTP 202 (accepted for processing; not a delivery guarantee).

**Errors:** 400 invalid request format, 401 missing or invalid authorization, 403 forbidden, 413
payload too large, 500 server error.

**Rate limiting:** responses include a limit header, a remaining header and a reset header (Unix
timestamp). HTTP 429 with remaining at 0 means wait for the reset time. Mail Send-specific limits
and a `Retry-After` header are not documented.
