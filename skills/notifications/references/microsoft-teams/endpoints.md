# Endpoints — Microsoft Teams Message Sending

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever HTTP
client/adapter is assumed available. Sources: Microsoft's own "Create an Incoming Webhook"
documentation
(https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook,
retrieved 2026-09-29) and the Microsoft Graph API reference "Send chatMessage in a channel"
(https://learn.microsoft.com/en-us/graph/api/channel-post-messages, retrieved 2026-09-29).

## Primary path: Workflows webhook trigger

**Method/URL:** `POST` to the workflow-specific URL generated when the "When a Teams webhook request
is received" trigger was configured (copied from the Workflows app after creating the flow — there is
no fixed, documented path pattern the way there is for a conventional REST API, since the URL is
generated per flow).

**Headers:** `Content-Type: application/json`.

**Body — simple text case** (per Microsoft's own worked example):

```json
{
  "text": "Hello from a webhook workflow!"
}
```

**Body — Adaptive Card case** (per Microsoft's own worked example, sent as the full envelope
including the Bot Framework `type`/`attachments` wrapper for this integration path — note this
differs from other Teams integration surfaces where a bare `AdaptiveCard` object is expected instead;
confirm which shape the specific configured flow's action actually expects):

```json
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
          { "type": "TextBlock", "text": "Message Text" }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
      }
    }
  ]
}
```

**Success:** an HTTP success response from the trigger indicates the request was accepted; it does
not by itself confirm the flow's downstream "post message" action completed (see `procedure.md`
step 6).

**Size limit:** 28 KB per request (documented by Microsoft); exceeding it produces an error.

**Rate limiting:** more than four requests per second to the same webhook triggers throttling until
the rate window resets; Microsoft's own guidance recommends retry with exponential backoff and
references handling HTTP 429 responses for this case.

## Alternate path: Microsoft Graph — Send chatMessage in a channel

**Method/URL:**

```
POST https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}/messages
```

**Headers:** `Authorization: Bearer <token>` (required), `Content-Type: application/json` (required).

**Permissions:** delegated `ChannelMessage.Send` (work or school account) is the least-privileged
option Microsoft documents for ordinary sending; personal Microsoft accounts are not supported for
this operation. Application-only permission (`Teamwork.Migrate.All`) is documented as scoped to
message-migration scenarios only, not general notification sending.

**Body — minimal example** (per Microsoft's own reference):

```json
{
  "body": {
    "content": "Hello World"
  }
}
```

Only `body` is mandatory; `body.contentType` can be set to distinguish plain text from HTML content.

**Success:** HTTP `201 Created`, with the response body containing the created `chatMessage` object
(including its server-assigned `id`, `createdDateTime`, `from`, and the echoed `body`).
