# Slack context bindings

Base: `https://slack.com/api`; `Authorization: Bearer <token>`.

| Operation | Binding | Inputs/results | Scope |
|---|---|---|---|
| User information | [GET /users.info](https://docs.slack.dev/reference/methods/users.info/) | `user; optional include_locale` | `users:read` |
| Profile | [GET /users.profile.get](https://docs.slack.dev/reference/methods/users.profile.get/) | `user; optional include_labels (strongly rate-limited)` | `users.profile:read` |
| Presence | [GET /users.getPresence](https://docs.slack.dev/reference/methods/users.getPresence/) | `user; active or away for another user` | `users:read` |
| DND | [GET /dnd.info](https://docs.slack.dev/reference/methods/dnd.info/) | `user; team_id for org-token scope` | `dnd:read` |
| Conversations | [GET /conversations.list](https://docs.slack.dev/reference/methods/conversations.list/) | `types,team_id,exclude_archived,cursor,limit; channels` | `channels:read/groups:read/im:read/mpim:read by type` |
| History | [GET /conversations.history](https://docs.slack.dev/reference/methods/conversations.history/) | `channel,oldest,latest,inclusive,cursor,limit; messages` | `relevant conversation-type :history scope` |
| Thread | [GET /conversations.replies](https://docs.slack.dev/reference/methods/conversations.replies/) | `channel,ts,oldest,latest,inclusive,cursor,limit; messages` | `relevant conversation-type :history scope` |
| Search | [GET /search.messages](https://docs.slack.dev/reference/methods/search.messages/) | `query,count,page,sort,sort_dir; messages.matches and paging` | `user token with search:read` |

Success uses `ok:true`. Cursors appear in `response_metadata.next_cursor`. Standard conversation-list limit is an integer below1000; history/reply methods have special commercial-distribution limits documented on their own pages, including15 objects and one request per minute for the stated newer non-Marketplace installations. No universal rate is assumed. Search uses `count<=100`, `page<=100`; results beyond this paging scope require a narrower query or a separately supported method. `users:read.email` is additional to basic user access; it does not override workspace email-display settings.

## Error handling

The following literal error codes come from the method references. At each procedure step: authentication/token/account/two-factor failures require an authorized session; scope, membership, visibility, network or policy denials stop that lookup; invalid/missing inputs and cursors require correction; missing channels/users/threads remain missing for that request; migration or service failures preserve an incomplete result; rate limiting honors `Retry-After`. Deprecation requires a supported replacement method. Unrecognized codes remain failures rather than empty data.


Read-method error codes: .

Sources: method links above, retrieved 2026-10-09.
