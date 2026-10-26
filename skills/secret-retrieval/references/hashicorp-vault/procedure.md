# HashiCorp Vault — Secret Retrieval Procedure

Reads or writes a secret's value in Vault's Key/Value secrets engine, covering both the older KV
version 1 (unversioned) and the current KV version 2 (versioned) mount types. Assumes an
authenticated Vault client already holding a valid client token — obtaining that token via a Vault
auth method (userpass, AppRole, cloud auth, etc.) is out of scope here.

Source: HashiCorp's own Vault API documentation for the KV v2 secrets engine and the KV v1
secrets engine (developer.hashicorp.com/vault/api-docs/secret/kv/kv-v1, retrieved 2026-09-29,
and .../kv-v2, retrieved 2026-10-26).

## Operational procedure

### 1. Determine the KV engine version in use

**KV v1 and v2 are not interchangeable — the request shape and the URL path differ.** If the caller
doesn't already know which version the target mount uses, this must be established first (e.g. by
checking how the mount was enabled, or by attempting a v2-style metadata read and treating a
not-found/format mismatch as a signal to fall back to v1 semantics). Never assume v2 just because
it's the newer default — plenty of long-lived mounts are still v1.

- **KV v1**: every request path is `/{mount}/{path}` directly — no `data`/`metadata` segment, no
  version concept.
- **KV v2**: the actual secret data lives under `/{mount}/data/{path}`; a separate
  `/{mount}/metadata/{path}` space holds version history and configuration. Treat these as two
  different logical resources sharing one secret name.

See `endpoints.md` for the exact paths of each.

### 2. Read a secret

- **KV v1**: issue a read against the mount+path directly. The response body's `data` map is the
  secret's full contents (whatever keys were written) — there is no separate `version` in the
  payload, since v1 has none.
- **KV v2**: issue a read against the `data` sub-path. To read a specific historical version rather
  than the latest, supply the `version` query parameter — omitting it returns the latest version,
  whatever that version's state. No skip to an earlier version is documented when the latest
  version is deleted or destroyed. The response separates the secret's own key/value map (under `data.data`)
  from Vault-managed version metadata (under `data.metadata`: `created_time`, `version`,
  `destroyed`, and deletion state).
- If the read returns nothing where a value was expected, check whether the requested (or latest)
  KV v2 version was soft-deleted or destroyed (see step 4) before concluding the secret doesn't
  exist — such a version still shows up in metadata history but yields no secret data. Unverified:
  the exact status code and body of a read against a deleted or destroyed version; report the read
  as failed and read the secret's metadata resource (see `endpoints.md`), whose per-version entries
  carry `deletion_time` and `destroyed`, to tell the states apart.
- Vault documents no fallback to an earlier version when the requested or latest version is deleted
  or destroyed, so do not expect an older version's value from such a read. Reading a
  named earlier version is a separate, explicit read.

### 3. Create or overwrite a secret's value

- **Before overwriting an existing secret's value, stop and confirm with the operator** — this is a
  destructive, hard-to-reverse-without-history action on KV v1 (no version history exists to recover
  the prior value), and a version-creating action with real operational impact on KV v2 (the prior
  version becomes non-current, though it's still recoverable unless later destroyed).
- **KV v1**: write the full desired key/value map to the mount+path. This is a full replace, not a
  merge — any key not included in the write is dropped from the stored secret.
- **KV v2**: write the desired key/value map inside a `data` wrapper to the `data` sub-path. Like v1,
  this replaces the entire contents at that path (it is not a per-key patch). Optionally include an
  `options.cas` (check-and-set) value to make the write conditional on the secret's current version
  number — pass `0` to require the secret not already exist, or the exact current version number to
  require no intervening write happened. Use `cas` whenever there's a real risk of a concurrent
  writer, since Vault's own semantics make this the documented way to detect that race rather than
  silently clobbering another writer's version.
- On success, KV v2 returns the new version's number and creation time; KV v1 returns no body
  (success is signaled by the response status alone).

### 4. Delete, undelete, or destroy a KV v2 version (KV v1 has no equivalent — see below)

KV v2 draws a real distinction between three levels of removal; KV v1 has only one (permanent
delete, since it has no version history to soft-delete from):

- **Soft delete** (a version's data becomes unreadable but recoverable) — targets either the latest
  version (delete against the `data` path) or a specific list of version numbers (`delete` sub-path
  with a `versions` array in the body). **Confirm with the operator before this step** even though
  it's recoverable, since a caller depending on that secret loses access immediately.
- **Undelete** (reverse a soft delete) — same `versions` array shape, against the `undelete`
  sub-path. Restores read access to those specific versions. **Always stop and confirm with the
  operator before submission** — it makes secret data readable again.
- **Destroy** (irreversible; the underlying data is actually removed) — same `versions` array shape,
  against the `destroy` sub-path. A destroyed version cannot be brought back with undelete.
  **This step always needs explicit operator confirmation before submission** — Vault documents
  this as not recoverable, unlike a soft delete.
- **KV v1 delete**: removes the value at the path outright, with no soft-delete/undelete tier at
  all. Treat every KV v1 delete as equivalent in severity to a KV v2 destroy, and gate it the same
  way.

### 5. Handle documented conditions

- A `cas` mismatch on a KV v2 write (the secret's current version doesn't match what was supplied)
  is a concurrency signal, not a generic failure — re-read the current version and let the operator
  decide whether to retry with the fresh version number or abandon the write.
- A read against a path that was never written, or that belongs to a mount that doesn't exist,
  returns a not-found condition — don't interpret this as "the secret has an empty value," they are
  different states.
- Every request requires the `X-Vault-Token` header; a missing or expired token is an authentication
  failure the caller must resolve (re-authenticate via whatever Vault auth method issued the
  original token) before retrying — this skill does not manage that token lifecycle itself.

## Patterns

- **KV v2's `data`/`metadata` split is the single most important structural fact to get right.**
  Reading and writing secret content always goes through `data`; version history, soft-delete
  state, and per-secret configuration (like max version count) always goes through `metadata`.
  Confusing the two produces a request that looks superficially correct but targets the wrong
  resource.
- **A version number is only meaningful on KV v2.** Don't ask a KV v1 mount for "version 3 of this
  secret" — the concept doesn't exist there; the only state is "whatever was last written."

## Known limitations

- Covers the KV v1 and v2 secrets engines only — Vault's other secret-producing engines (database
  dynamic credentials, cloud provider dynamic credentials, Transit encryption keys) are a
  structurally different kind of "secret" (generated on demand, often leased/expiring) and are out
  of scope for this skill.
- Does not cover Vault PKI (certificate issuance) — see `certificate-management`.
- Does not cover enabling a new KV mount or configuring engine-level settings (max versions,
  cas-required enforcement) — this skill assumes the mount already exists with whatever
  configuration the operator has set.

## Tools

Every operation maps to the Vault HTTP API — see `endpoints.md` for literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| KV v1 read | Read a secret's current (only) value | Secret Read |
| KV v2 read | Read a secret's latest or a specific version's value plus metadata | Secret Read |
| KV v1 write | Fully replace a secret's stored key/value map | Secret Write |
| KV v2 write | Create a new version with a fully replaced key/value map | Secret Write |
| KV v1 delete | Permanently remove the secret | Secret Delete |
| KV v2 soft delete | Mark version(s) deleted, recoverable | Secret Delete |
| KV v2 undelete | Restore soft-deleted version(s) | Secret Delete |
| KV v2 destroy | Permanently remove version(s) | Secret Delete |

## Verification checklist

- [ ] KV engine version (v1 vs v2) for the target mount was confirmed, not assumed
- [ ] For KV v2 reads, whether a specific version or the latest was intended was made explicit
- [ ] Any overwrite, delete, undelete, or destroy of an existing value was confirmed with the operator first
- [ ] A `cas` value was used on KV v2 writes where a concurrent writer was a realistic risk
- [ ] The retrieved secret value was not written into any log, report, or status message
