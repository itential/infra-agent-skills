# HashiCorp Vault PKI — CA Generation and Role Configuration Bindings

Wire-level calls behind `vault-pki-ca-configuration-procedure.md`. Source: HashiCorp Vault PKI
secrets engine API reference (developer.hashicorp.com/vault/api-docs/secret/pki), Vault 1.11+
multi-issuer paths, retrieved 2026-10-26. Base: the Vault address plus `/v1`; `{mount}` is the
existing PKI mount (the docs' examples use `pki`). Auth: `X-Vault-Token`; `X-Vault-Namespace` where
namespaces are used (the namespace header comes from Vault's general HTTP API, not the PKI page).

| Operation | Method and path | Fields and result |
|---|---|---|
| List issuers | `LIST /{mount}/issuers` | No token needed. `data.keys` (IDs), `data.key_info` (ID to `issuer_name`) |
| Read issuer | `GET /{mount}/issuer/{issuer_ref}` | `issuer_ref` is an ID, a name, or `default`. Returns `certificate`, `ca_chain`, `issuer_id`, `issuer_name`, `key_id`, `usage`, `leaf_not_after_behavior`, `manual_chain`; `warnings` notes a previously exported key |
| Read default issuer | `GET /{mount}/config/issuers` | `default`, `default_follows_latest_issuer` |
| Generate root | `POST /{mount}/issuers/generate/root/{type}` | `type` is `internal` (key never returned), `exported` (key returned once), `existing` (reuse `key_ref`) or `kms`. Body: `common_name` (required), `issuer_name`, `key_name`, `ttl` or `not_after`, `key_type` (`rsa` default, `ec`, `ed25519`, `ml-dsa`), `key_bits`, `max_path_length`, `permitted_dns_domains` and sibling name-constraint fields, subject fields. Result: `certificate`, `issuing_ca`, `serial_number`, `issuer_id`, `issuer_name`, `key_id`, `key_name`; `private_key` only for `exported`. The legacy path `/{mount}/root/generate/{type}` does the same |
| Generate intermediate CSR | `POST /{mount}/issuers/generate/intermediate/{type}` | Same `type` values and similar body (`common_name` required). Result: `csr`, plus `private_key` and `private_key_type` for `exported`. Creates no issuer. Legacy: `/{mount}/intermediate/generate/{type}` |
| Import signed intermediate | `POST /{mount}/intermediate/set-signed` | Body: `certificate` (PEM, chain concatenated). Result: `imported_issuers`, `imported_keys`, `mapping`, `existing_issuers`, `existing_keys` |
| Set default issuer | `POST /{mount}/config/issuers` | Body: `default` (name or ID), optional `default_follows_latest_issuer` (bool, default false). Result: `data.default` |
| List roles | `LIST /{mount}/roles` | `data.keys` |
| Read role | `GET /{mount}/roles/{name}` | Current definition |
| Create or replace role | `POST /{mount}/roles/{name}` | Overwrites; omitted fields take defaults. Fields below |
| Patch role | `PATCH /{mount}/roles/{name}` | Changed fields only. Assumption: header `Content-Type: application/merge-patch+json` (docs only reference the KV v2 patch format) |
| Delete role | `DELETE /{mount}/roles/{name}` | Existing certificates are not revoked |

Role fields (defaults from the docs): `issuer_ref` (`default`; stored verbatim), `ttl` (empty: system
default or `max_ttl`, whichever is shorter), `max_ttl` (empty: system max), `allowed_domains` (empty
list), `allow_bare_domains` (false), `allow_subdomains` (false), `allow_glob_domains` (false),
`allow_wildcard_certificates` (true), `allow_any_name` (false), `allow_localhost` (true),
`enforce_hostnames` (true), `allow_ip_sans` (true), `allowed_uri_sans` (empty), `server_flag` (true),
`client_flag` (true), `code_signing_flag` (false), `email_protection_flag` (false), `key_type`
(`rsa`; `any` is signing-only), `key_bits` (0 meaning the type's default), `require_cn` (true),
`no_store` (false), `generate_lease` (false), `not_before_duration` (30s). Values come from the
operator's approved policy, not from these defaults.

Documented outcomes: Generate root, intermediate CSR, set default issuer and role reads return a
JSON body; the role-write response shape and status (200 versus 204) are not stated on the docs
page, so accept either. Unverified here: exact error strings for rejected role fields, so
preserve the returned `errors` array verbatim. Standard Vault HTTP statuses apply: 400 invalid
request, 403 token or policy, 404 absent or hidden path, 405 wrong method, 429 request limiting,
500/502/503 server-side.
