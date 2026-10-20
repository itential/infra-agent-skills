# Endpoints — Mattermost Create Post

Literal wiring layer. `procedure.md` steps reference these by name. Source: Mattermost's API v4
definition (`api/v4/source/posts.yaml` and `introduction.yaml` in the official `mattermost/mattermost`
repository, retrieved 2026-10-19) and the incoming webhooks developer page
(https://developers.mattermost.com/integrate/webhooks/incoming/, retrieved 2026-10-19).

## Create a Post

```
POST https://<mattermost-host>/api/v4/posts
```

**Authentication:** `Authorization: Bearer <token>` (session token from `POST /api/v4/users/login`
via its response `Token` header, or a personal access token). Requires the `create_post` permission
on the target channel.

**Query parameters:** `set_online` (boolean, optional); `silent` (boolean, optional — bot accounts,
OAuth apps, incoming webhooks and plugins only, otherwise HTTP 403).

**Body fields (JSON):**

| Field | Required | Notes |
|---|---|---|
| `channel_id` | Yes | ID of the channel to post in. |
| `message` | Yes | Message contents; Markdown allowed. |
| `root_id` | No | ID of the post to comment on (thread reply). |
| `file_ids` | No | IDs of previously uploaded files; maximum 5 per post. |
| `props` | No | JSON property bag; several keys are documented as reserved and server-controlled. |
| `metadata.priority` | No | Object with `priority` (empty, `important`, or `urgent`) and `requested_ack` (boolean). |

**Responses:** `201` with the created post object; `400`, `401`, `403` documented as error responses.
Error body shape: `id`, `message`, `request_id`, `status_code`, `is_oauth`.

**Rate limiting:** response headers `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`,
`X-Ratelimit-Reset`; exceeded limit returns `429`.

## Incoming Webhook (alternate path)

```
POST https://<mattermost-host>/hooks/<generated-key>
Content-Type: application/json
```

No `Authorization` header; the URL itself is the credential. Body fields include `text` (required
unless `attachments` is set), `channel` (channel name, or `@username` for a direct message),
`username`, `icon_url`, `icon_emoji`, `attachments`, `type`, `props`, `priority`, `silent`. A
successful call returns HTTP 200 with the plain-text body `ok`. If no `Content-Type` header is set,
the body must be prefixed with `payload=` (Slack compatibility, per Mattermost's page).
