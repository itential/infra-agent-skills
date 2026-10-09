# Secret Retrieval — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full
step-by-step) plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| HashiCorp Vault | `hashicorp_vault/` | Read/write/list a secret in KV v1 or KV v2; inspect KV v2 version metadata; delete/undelete/destroy a KV v2 version | Token-based auth (`X-Vault-Token`); KV v2 is versioned and soft-delete capable, KV v1 is not |
| 1Password (Connect API) | `1password/` | Read/create/update/delete a vault item and its field values | Requires a self-hosted 1Password Connect server plus a scoped Connect access token; items hold multiple typed fields, not one bare value |
| CyberArk Conjur | `cyberark_conjur/` | Retrieve/set the value of a `variable` resource (a "secret") | Two-step auth (login for API key, then authenticate for a short-lived access token); the variable resource itself must already exist via policy before a value can be set |
| CyberArk Privilege Cloud | `cyberark_privilege_cloud/` | Retrieve/change a privileged account's credential value; trigger verify/reconcile | Session-token auth via Logon; "accounts" are the addressable unit, not bare key/value secrets; retrieval is documented as intended for human/interactive use, not high-volume automation |
| AWS Secrets Manager | `aws_secrets_manager/` | Get/put a secret value; rotate a secret; describe secret metadata | SigV4-signed calls; versioned via staging labels (`AWSCURRENT`/`AWSPENDING`/`AWSPREVIOUS`), not sequential version numbers |
| Azure Key Vault | `azure_key_vault/` | Get/set/delete/list a secret in a Key Vault instance | OAuth2 bearer token (Azure AD) scoped to `https://vault.azure.net/.default`; every Set creates a new version automatically, versions are immutable |

**Not in scope for this skill:** PKI certificate issuance/renewal (see the separate
`certificate_management` skill — HashiCorp Vault PKI and AWS Certificate Manager are covered there,
not here), and secrets-engine/vault/mount configuration (enabling a KV engine, creating a Key Vault
resource, authoring a Conjur policy that defines a variable) — this skill assumes that setup is
already done and a specific secret/path/item/account already exists to read or write.

## Adding a new vendor

1. Create `references/<vendor>/procedure.md` following the shape of an existing vendor file
   (Operational procedure → Patterns → Known limitations → Tools → Verification checklist).
2. Add `endpoints.md` (wire-level calls) alongside it.
3. Add one row to the table above.
4. Do NOT add vendor-specific procedure content to the top-level `SKILL.md` — see that file's own
   contribution note.
5. Re-check `SKILL.md`'s "Universal concepts" section against the new vendor's actual behavior
   before merging — if the new vendor contradicts a claim there (e.g. a platform with no
   authenticated-identity model, or one that doesn't generate any access record), that's a bug in
   `SKILL.md` to fix, not a footnote to add here.
