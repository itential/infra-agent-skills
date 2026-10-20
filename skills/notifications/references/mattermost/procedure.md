# Mattermost — Create a Post Procedure

Posts a new message into a Mattermost channel, or as a reply within an existing thread, using the
REST API's create-post operation. Covers creating a new post only — not ephemeral posts (visible to
one user only), not editing, patching, or deleting a post already sent, not file upload, and not
channel/user lookup (this procedure assumes the caller already has a valid channel ID).

Sources: Mattermost's own API v4 definition (the `posts.yaml` and `introduction.yaml` OpenAPI source
files in the official `mattermost/mattermost` repository, `api/v4/source/`, retrieved 2026-10-19) and
Mattermost's incoming webhooks developer page
(https://developers.mattermost.com/integrate/webhooks/incoming/, retrieved 2026-10-19).

## Operational procedure

1. **Resolve the destination.** The create-post call takes a `channel_id` — an ID, not a channel
   name or display name. If only a name was given, resolving it is a separate lookup that is not part
   of this procedure. To reply in a thread, also have the ID of the thread's root post.
2. **Choose the path.** Use the REST create-post call (this procedure) when the sender is a
   Mattermost user, bot account, or OAuth app with the `create_post` permission on the target
   channel. Use an incoming webhook instead when the integration only needs to post and a webhook URL
   has already been configured by an administrator (see Patterns); a webhook URL is a secret.
3. **Compose the body.** `message` is required and may use Markdown. Add `root_id` to post as a
   comment on an existing post. Use `props` only for extra metadata; several keys inside `props` are
   documented as reserved and server-controlled, so do not rely on setting them from the REST call.
   Attach files only by first uploading them and passing the resulting `file_ids` (maximum 5 per
   post — send additional posts for more files).
4. **Decide whether it should notify.** The `silent` query parameter, when true, delivers the post
   with no desktop, push or email notifications and no unread/mention count changes. Only bot
   accounts, OAuth apps, incoming webhooks and plugins may set it; any other sender gets HTTP 403.
   Treat `@channel`/`@here` mentions in `message` as a deliberate choice rather than a default.
5. **Submit the call.** See `endpoints.md` for the literal request shape.
6. **Confirm creation from the response.** Success is HTTP 201 with the created post object; keep
   its post `id` as the handle for later threading. On failure, surface the literal HTTP status and
   the error body's `id` and `message` fields (the API's documented error shape) rather than a
   generic failure.
7. **Handle rate limiting explicitly.** The API reports its rate limit state in `X-Ratelimit-Limit`,
   `X-Ratelimit-Remaining` and `X-Ratelimit-Reset` response headers, and an exceeded limit returns
   HTTP 429. Wait until the reset indicated by `X-Ratelimit-Reset` before retrying rather than
   retrying on a fixed short interval.

## Patterns

- **The REST path needs credentials; the webhook path needs only a URL.** A session token or
  personal access token is sent as `Authorization: Bearer`. Session tokens expire; personal access
  tokens live until revoked. An incoming webhook endpoint has a default channel set
  when it was created, and its payload may override the channel by name (not display name) — and
  Mattermost's own page says anyone holding the endpoint can post, so never log it.
- **Webhook posts are labelled as bot posts in Mattermost clients.** Mattermost documents a BOT
  indicator on them, so do not expect them to look like a person's message.
- **Reuse a resolved channel ID** rather than re-deriving it on every send.

## Known limitations

- Covers only creating a new post or thread reply. Ephemeral posts, editing/patching/deleting a post,
  file upload, and channel or user lookup are separate capabilities not covered here.
- Identity overrides (username, icon) on the webhook path only take effect when the matching
  Mattermost server configuration settings are enabled — confirm with the administrator before
  promising a custom sender name.
- Mattermost's documentation describes `X-Ratelimit-Reset` as the remaining seconds before the limit
  resets; it does not document a `Retry-After` header. The documented numeric limits are examples in
  the API introduction, so do not assume a fixed ceiling for a given server.
- Accepted (HTTP 201) means the server stored the post, not that a person has read it.
- Not verified against a live Mattermost server; everything above is from the vendor's published
  definitions.

## Tools

| Operation | Description | Category |
|---|---|---|
| `CreatePost` | Create a post in a channel, optionally as a thread reply | Messaging |

## Verification checklist

- [ ] Destination was a channel ID, not a display name
- [ ] `message` populated; `root_id` set only when replying to an existing post
- [ ] If `silent` was used, the sender is a bot, OAuth app, webhook or plugin
- [ ] Response was HTTP 201 and the post `id` was kept
- [ ] On failure, the HTTP status and the error body's `id`/`message` were reported
- [ ] On HTTP 429, the `X-Ratelimit-Reset` value was honored before any retry
- [ ] No webhook URL or token appeared in any log or message
