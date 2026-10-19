# Endpoints — Twilio Create Message

Literal wiring layer. `procedure.md` steps reference these by name. Source: Twilio's Message resource
reference (https://www.twilio.com/docs/messaging/api/message-resource, retrieved 2026-10-19) and the
20429 error page (https://www.twilio.com/docs/api/errors/20429, retrieved 2026-10-19). The OpenAPI spec
in `itential/assets` is a secondary source and was not relied on for any field below.

## Create message

```
POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json
```

**Authentication:** HTTP Basic, with the Account SID and Auth Token, or an API key SID and secret.

**Body fields (form-encoded):**

| Field | Required | Notes |
|---|---|---|
| `To` | Yes | Recipient phone number in E.164 form (or a channel address for other channels — out of scope). |
| `From` | One of `From` / `MessagingServiceSid` | Sender number, alphanumeric sender ID, or channel address. |
| `MessagingServiceSid` | One of `From` / `MessagingServiceSid` | Lets Twilio select the sender. |
| `Body` | One of `Body` / `MediaUrl` / `ContentSid` | Text, up to 1,600 characters. |
| `MediaUrl` | One of the content fields | Up to 10 media URLs; images documented at 5 MB each. |
| `ContentSid` | One of the content fields | Content template identifier. |
| `StatusCallback` | No | URL that receives a POST on each status change (`MessageStatus`, `ErrorCode`). |
| `ValidityPeriod` | No | 1–36000 seconds; default 36000. |
| `MessageIntent` | No | Documented values include `notifications`. |

**Success:** HTTP 201 with the message resource, including its identifier and initial status
(`queued`, or `accepted` with a Messaging Service). Assumption: the identifier field is named `sid`
(not stated on the page retrieved).

**Statuses:** `accepted`, `queued`, `sending`, `sent`, `delivered`, `undelivered`, `failed`
(plus `scheduled`, `receiving`, `received`, which are out of scope here).

**Rate limiting:** HTTP 429 with error code `20429` means the concurrent request limit was exceeded.
Documented remedy: retry with exponential backoff. The `Twilio-Concurrent-Requests` response header
reports current load. No `Retry-After` header is documented.

## Fetch message

```
GET https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages/{Sid}.json
```

Reading a message back by its identifier returns its current status and error fields. Authentication
is the same as for create.
