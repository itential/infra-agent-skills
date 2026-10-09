# Slack external upload bindings

Base: `https://slack.com/api`; bearer token with `files:write`.

| Operation | Binding | Request / success |
|---|---|---|
| Prepare | `POST /files.getUploadURLExternal` | `filename`, integer `length` in bytes; optional `alt_txt`,`snippet_type`; `ok:true`,`upload_url`,`file_id` |
| Transfer | `POST <returned-upload_url>` | Raw bytes or multipart file data; HTTP 200 |
| Complete | `POST /files.completeUploadExternal` | `files:[{id:<file-id>,title:<optional-title>}]`; optional `channel_id`,`thread_ts`,`initial_comment`; `ok:true` and file objects |

Without `channel_id`, completion retains a private file. `thread_ts` refers to the parent. Completion supports `blocks` as a JSON-encoded string but ignores it if `initial_comment` is present. This scope uses one explicit `channel_id`, not the alternate multi-destination `channels` parameter. Identity customization is not used.

## Error handling

The following literal error codes come from the method references. At each procedure step: authentication/token/account/two-factor failures require an authorized session; scope, membership, visibility, network or policy denials stop that lookup; invalid/missing inputs and cursors require correction; missing channels/users/threads remain missing for that request; migration or service failures preserve an incomplete result; rate limiting honors `Retry-After`. Deprecation requires a supported replacement method. Unrecognized codes remain failures rather than empty data.


Upload-specific codes: .

Source: Slack method references linked in [procedure](procedure.md), retrieved 2026-10-09.
