# Endpoint Wiring — HashiCorp Vault Secret Retrieval

Literal API calls behind each capability named in `procedure.md`. All calls are Vault's HTTP API,
JSON request/response bodies, authenticated with an `X-Vault-Token` header carrying a valid client
token. `{mount}` is the path a KV engine was enabled at (commonly `secret`, but caller-defined);
`{path}` is the secret's location under that mount.

Sources: [KV v1](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v1), [KV v2](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2), [HTTP API](https://developer.hashicorp.com/vault/api-docs), retrieved 2026-10-09. All paths below are relative to `/v1` at the authorized Vault base address.

## KV v1 — Read a Secret

`GET /{mount}/{path}`

Response: `data` — a map of whatever keys were last written at that path.

No versioning: there is no `version` field in the response and no way to request a prior value.

## KV v1 — Create or Replace a Secret

`POST /{mount}/{path}`

Body: a flat JSON object of key/value pairs — this becomes the entire stored secret content,
replacing anything previously stored at that path.

Response: no body on success; success is the HTTP status alone.

## KV v1 — Delete a Secret

`DELETE /{mount}/{path}`

Permanent removal — no soft-delete tier exists at this engine version.

## KV v2 — Read a Secret Version

`GET /{mount}/data/{path}?version={version}`

`version` is optional; omitted, selects the latest version; deletion or destruction does not make this a search for an older readable version.

Response: `data.data` — the secret's key/value map. `data.metadata` — `created_time`, `version`
(integer), `destroyed` (boolean), plus deletion-time fields if the version was soft-deleted.

## KV v2 — Create or Update a Secret

`POST /{mount}/data/{path}`

Body:
```
{
  "data": { "<key>": "<value>", ... },
  "options": { "cas": <integer, optional> }
}
```
`data` replaces the entire key/value map for the new version (not a per-key merge). `options.cas`,
if supplied, makes the write conditional: `0` requires the secret not already exist; a positive
integer requires the secret's current version to exactly equal that number.

Response: `data` — `version` (the new version's number), `created_time`, `custom_metadata`,
`deletion_time`, `destroyed`.

## KV v2 — List Version/Config Metadata

`GET /{mount}/metadata/{path}` — returns per-secret metadata and version history (not the secret
values themselves).

## KV v2 — Soft-Delete Specific Versions

`POST /{mount}/delete/{path}`

Body: `{ "versions": [<integer>, ...] }`

Marks the listed versions deleted (recoverable) without touching other versions of the same secret.

Note: `DELETE /{mount}/data/{path}` (no body) is the shorthand for soft-deleting only the current
latest version.

## KV v2 — Undelete Specific Versions

`POST /{mount}/undelete/{path}`

Body: `{ "versions": [<integer>, ...] }`

Restores read access to the listed soft-deleted versions.

## KV v2 — Destroy Specific Versions

`PUT /{mount}/destroy/{path}`

Body: `{ "versions": [<integer>, ...] }`

Permanently removes the underlying data for the listed versions — not recoverable. Always gate this
call behind explicit operator confirmation (see the Remove/restore step in `procedure.md`).

## Authentication header (all calls above)

`X-Vault-Token: <client token>` — obtained separately via whatever Vault auth method the caller's
environment uses; this skill does not perform that login step.

## Mount version and directory listing

`GET /sys/mounts/{mount}` identifies engine `type` and KV `options.version`.

`LIST /{mount}/{directory}` lists KV v1 names. `LIST /{mount}/metadata/{directory}` lists KV v2 names; optional `exclude_deleted` filters deleted entries. Both return `data.keys`; `GET` with `list=true` is an alternative to the `LIST` method.

## Common error statuses

Errors use an `errors` array. 400: invalid input, including a failed write condition; 403: authentication/policy; 404: absent/inaccessible path or empty LIST; 405: wrong method; 412: Enterprise eventual-consistency precondition; 429: quota pressure (health endpoints also use it for standby); 500: internal error; 501: uninitialized; 502: upstream error; 503: sealed, maintenance, or overload. Health endpoints additionally use 472/473 for replication and performance standby states. Successful responses can be 200 or 204; warnings can produce a body where an empty response was expected.
