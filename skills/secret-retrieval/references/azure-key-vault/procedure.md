# Azure Key Vault — Secret Retrieval Procedure

Reads, writes, deletes, or lists secrets in an Azure Key Vault instance. Assumes the caller already
holds a valid Azure AD (Microsoft Entra ID) OAuth2 access token scoped to
`https://vault.azure.net/.default` and has been granted the relevant Key Vault access policy or RBAC
role (`secrets/get`, `secrets/set`, `secrets/delete`, `secrets/list`, as applicable); provisioning
that token or the access grant itself is out of scope here.

Source: Microsoft's own REST API reference for Azure Key Vault secrets operations
(learn.microsoft.com/en-us/rest/api/keyvault/secrets/ — Get Secret, Set Secret, Delete Secret, Get
Secrets pages, API version `2025-07-01`), retrieved 2026-09-29.

## Operational procedure

### 1. Confirm the vault's base URL and API version

Every call targets a specific vault instance by its own DNS name
(`https://<vault-name>.vault.azure.net`), not a shared Azure management endpoint, and every request
requires an explicit `api-version` query parameter — Microsoft version-pins this API and does not
default to "latest" if the parameter is omitted. Confirm both before proceeding rather than assuming
a prior call's vault/version still applies.

### 2. Read a secret's value

Call get-secret with the secret's name and, optionally, a specific version identifier in the path.
Omitting the version returns the latest enabled version. The response bundles the value together
with its identity and management attributes in one object: `value` (the actual secret content),
`id` (a URL that embeds both the secret name and its version — useful for pinning a later read to
exactly this version), `contentType` (a caller-supplied hint about what the value represents, not
enforced by the vault), and `attributes` (`enabled`, `created`, `updated`, `exp`/`nbf` validity
window if set, `recoveryLevel`).

### 3. List secrets in a vault (metadata only, no values)

Call get-secrets (no name in the path — vault-scoped) to enumerate what secrets exist. This
returns only base identifiers and attributes per secret, explicitly not values — a separate
get-secret call per name is required to see any actual content. Supports pagination via a returned
`nextLink` when the vault holds more than the page size.

### 4. Create or update a secret's value

**Confirm with the operator before setting a value for a secret name that already exists** — Key
Vault's own documented behavior is that this always creates a brand-new, immutable version rather
than modifying anything in place; the previous version remains retrievable by its own version
identifier (from step 2) unless separately purged, but every consumer doing an unversioned "get
latest" read will start seeing the new value immediately.

Call set-secret with the secret name in the path and, in the body, the new `value`, plus optionally
`contentType` and `attributes` (e.g. to set an expiry). There is no way to update just the
attributes of the existing latest version without also supplying a value in this same call — this
is a create-new-version operation, not a metadata patch.

### 5. Delete a secret

**This is a hard-to-reverse action needing explicit operator confirmation before submission.**
Delete applies to the entire secret (all versions), not to one version individually — Microsoft's
own documentation is explicit that delete cannot target an individual version. Depending on the
vault's configured `recoveryLevel` (visible in the secret's `attributes`), a deleted secret may
remain recoverable for a retention window (7–90 days) before being eligible for permanent purge, or
it may be purged immediately if the vault has no soft-delete protection configured — check
`recoveryLevel` before assuming a delete is recoverable.

### 6. Handle documented errors

- Every operation shares one error envelope (`KeyVaultError`, wrapping an `Error` with `code`,
  `message`, and an optional nested `innererror`) rather than distinct per-operation error types —
  read the `code`/`message` pair to determine the actual cause rather than branching on HTTP status
  alone.
- A `secrets/get`, `secrets/set`, `secrets/delete`, or `secrets/list` permission gap on the calling
  identity's access policy/RBAC role produces an authorization failure — this needs an operator to
  grant the missing permission, not a retry with the same token.

## Patterns

- **Every write is a new, immutable version — there is no in-place update of an existing version's
  value.** This mirrors Vault KV v2 and AWS Secrets Manager's versioning model more than it mirrors
  1Password or Conjur; when reasoning about "did this call change the existing value or create a
  new one," the answer for Key Vault is always "created a new one."
- **`id` doubles as a version pointer.** The `id` returned on a read or write embeds the specific
  version — capturing it is the documented way to pin a later read to exactly this version rather
  than whatever happens to be latest at that time.

## Known limitations

- Does not cover Key Vault instance creation, access policy/RBAC role assignment, or network
  ACL/firewall configuration on the vault itself — this skill assumes the vault exists and the
  caller's identity is already permissioned against it.
- Does not cover Key Vault's key or certificate object types (`keys/*`, `certificates/*` REST
  surfaces) — see `certificate-management` for certificate handling; only the `secrets/*` surface is
  in scope here.
- Does not cover soft-delete recovery or purge as an explicit workflow beyond noting that
  `recoveryLevel` governs whether it's possible — recovering or purging a soft-deleted secret is a
  distinct set of calls (`recover`, `purge`) not detailed in `endpoints.md`.

## Tools

Every operation maps to the Azure Key Vault REST API (`secrets` surface) — see `endpoints.md` for
literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| Get Secret | Read a secret's latest or a specific version's value plus attributes | Secret Read |
| Get Secrets | List secrets in a vault (metadata only, no values) | Secret Read |
| Set Secret | Create a new version with a new value | Secret Write |
| Delete Secret | Remove a secret (all versions), subject to the vault's soft-delete configuration | Secret Delete |

## Verification checklist

- [ ] The correct vault base URL and an explicit `api-version` were used, not assumed from a prior
      call
- [ ] Whether a specific version or "latest" was intended was made explicit before reading
- [ ] Any Set against an existing secret name was confirmed with the operator, understanding it
      creates a new version rather than editing in place
- [ ] Delete was confirmed with the operator, and the vault's `recoveryLevel` was checked to know
      whether the deletion is recoverable within a retention window or immediate
- [ ] The retrieved secret value was not written into any log, report, or status message
