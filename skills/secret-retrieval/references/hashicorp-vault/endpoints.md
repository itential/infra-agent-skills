# Endpoint Wiring — HashiCorp Vault Secret Retrieval

Literal API calls behind each capability named in `procedure.md`. All calls are Vault's HTTP API,
JSON request/response bodies, authenticated with an `X-Vault-Token` header carrying a valid client
token. `{mount}` is the path a KV engine was enabled at (commonly `secret`, but caller-defined);
`{path}` is the secret's location under that mount.

Source: developer.hashicorp.com/vault/api-docs/secret/kv/kv-v1 and .../kv-v2, retrieved 2026-09-29; destroy method and version-omitted read re-checked 2026-10-26.

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

`version` is optional; omitted, returns the latest version. No fallback to an earlier version is
documented when the requested or latest version is deleted or destroyed, and none should be
performed by the caller.

Response: `data.data` — the secret's key/value map. `data.metadata` — `created_time`, `version`
(integer), `destroyed` (boolean), and `deletion_time`.

Unverified: the HTTP status and body returned when the targeted version is soft-deleted or
destroyed are not stated in the API reference. Treat any response lacking `data.data` as a failed
read.

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

`POST /{mount}/metadata/{path}` — updates per-secret configuration (e.g. max versions retained).

`DELETE /{mount}/metadata/{path}` — deletes the metadata entry and **all** versions of the secret
permanently; treat as equivalent in severity to a destroy-all-versions action.

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
call behind explicit operator confirmation (see `procedure.md` step 4).

## Authentication header (all calls above)

`X-Vault-Token: <client token>` — obtained separately via whatever Vault auth method the caller's
environment uses; this skill does not perform that login step.
