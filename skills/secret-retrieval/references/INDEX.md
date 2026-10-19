# Secret Retrieval — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full
step-by-step) plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| HashiCorp Vault | `hashicorp-vault/` | Read/write a secret in the KV v1 or KV v2 secrets engine; delete/undelete/destroy a KV v2 version | Token-based auth (`X-Vault-Token`); KV v2 is versioned and soft-delete capable, KV v1 is not |
| 1Password (Connect API) | `1password/` | Read/create/update/delete a vault item and its field values | Requires a self-hosted 1Password Connect server plus a scoped Connect access token; items hold multiple typed fields, not one bare value |
| CyberArk Conjur | `cyberark-conjur/` | Retrieve/set the value of a `variable` resource (a "secret") | Two-step auth (login for API key, then authenticate for a short-lived access token); the variable resource itself must already exist via policy before a value can be set |
| CyberArk Privilege Cloud | `cyberark-privilege-cloud/` | Retrieve/change a privileged account's credential value; trigger verify/reconcile | Session-token auth via Logon; "accounts" are the addressable unit, not bare key/value secrets; retrieval is documented as intended for human/interactive use, not high-volume automation |
| AWS Secrets Manager | `aws-secrets-manager/` | Get/put a secret value; rotate a secret; describe secret metadata | SigV4-signed calls; versioned via staging labels (`AWSCURRENT`/`AWSPENDING`/`AWSPREVIOUS`), not sequential version numbers |
| Azure Key Vault | `azure-key-vault/` | Get/set/delete/list a secret in a Key Vault instance | OAuth2 bearer token (Azure AD) scoped to `https://vault.azure.net/.default`; every Set creates a new version automatically, versions are immutable |
| Delinea Secret Server | `delinea-secret-server/` | Read a secret (whole, or one field by slug) by numeric ID; overwrite a field value | Native REST API with an OAuth2 password-grant token; secrets addressed by numeric ID, values held in a slug-keyed items list. Secrets may require check-out, approval or a comment, which can block API reads (no documented bypass). Delinea Platform-mediated calls (different base path and token source), check-out calls and search are not covered. The field-level read call and domain parameter are unverified (secondary source) |

**Not in scope for this skill:** PKI certificate issuance/renewal (see the separate
`certificate-management` skill — HashiCorp Vault PKI and AWS Certificate Manager are covered there,
not here), and secrets-engine/vault/mount configuration (enabling a KV engine, creating a Key Vault
resource, authoring a Conjur policy that defines a variable) — this skill assumes that setup is
already done and a specific secret/path/item/account already exists to read or write.

Correction recorded when Delinea Secret Server was added: the universal claims that every platform redacts secret values from its audit log and generates an access record were hedged to "where a platform documents it", because Delinea's sources reviewed state neither.
