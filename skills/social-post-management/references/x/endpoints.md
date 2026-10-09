# X APIv2 post bindings

Base: `https://api.x.com`. Read operations support the documented bearer or user authentication; writes require user-context OAuth2 (`tweet.read`,`users.read`,`tweet.write`) or supported OAuth1 user credentials. Read OAuth2 scopes are `tweet.read`,`users.read`.

| Operation | Binding | Input / output |
|---|---|---|
| Mentions | `GET /2/users/{id}/mentions` | `max_results`5–100, optional `pagination_token`,`since_id`,`until_id`,`start_time`,`end_time`; `data`, `meta`, possible `errors` |
| Lookup | `GET /2/tweets/{id}` | selected fields; `data`, possible `errors` |
| Recent search | `GET /2/tweets/search/recent` | required `query`, `max_results`10–100; optional bounds and `next_token` or `pagination_token`, never both; `data`,`meta`,`errors` |
| Create | `POST /2/tweets` | `{"text":"<approved-text>"}`;201 with `data.id`,`data.text` |
| Reply | `POST /2/tweets` | text plus `reply:{in_reply_to_tweet_id:<parent-post-id>}`;201 with `data.id` |
| Delete | `DELETE /2/tweets/{id}` |200 with `data.deleted:true` |

The retrieved current reference names the field-selector parameter `post.fields`, including `conversation_id` and `created_at`; this binding does not silently substitute older `tweet.fields` examples. Recent search forbids combining `start_time` with `since_id`, or `end_time` with `until_id`. Start is within the last seven days. Result continuation uses the returned metadata token with unchanged query filters.

Already-uploaded media may be attached using `media:{media_ids:[<id>]}`. The current create schema allows up to 4 IDs but media-kind restrictions still apply (up to 4 photos, one GIF or one video). `text` is sent explicitly, including an empty string for media-only content. Quote posting requires a different entitlement and is out of scope.

## Problem responses

The default failure may be `{code,message}` or an RFC-style problem with `type`,`title`,`detail`,`status`; successful envelopes may also contain `errors`. Documented problem families include resource-not-found, invalid-request, not-authorized-for-resource, not-authorized-for-field, field-unauthorized, field-hydration-failure, resource-unavailable, disallowed-resource, recipient-not-messageable, internal-error, duplicate-rules and invalid-rules. The last two are generic schema members, not permission to create stream rules through this capability. Correct invalid input, stop on access restrictions, retain partial fields on hydration errors, and report unavailable/internal failures; unclassified transport/rate errors remain explicit failures and follow returned provider guidance. No undocumented retry interval is supplied.

Sources: the method references linked in [procedure](procedure.md), API schema2.170 as retrieved 2026-10-09.
