# Vault PKI authority configuration bindings

Sources: [PKI API](https://developer.hashicorp.com/vault/api-docs/secret/pki), [HTTP API](https://developer.hashicorp.com/vault/api-docs), retrieved 2026-10-09.

Base: authorized Vault address plus `/v1`; token header `X-Vault-Token`, namespace header `X-Vault-Namespace` where required. `{mount}` is the existing PKI mount.

| Operation | Method/path | Fields/result |
|---|---|---|
| List issuers | `LIST /{mount}/issuers` | `data.keys`, `data.key_info`; publisher permits this discovery unauthenticated |
| Read issuer | `GET /{mount}/issuer/{issuer_ref}` | Certificate, chain, issuer/key IDs, usage and warnings |
| Generate internal root | `POST /{mount}/issuers/generate/root/internal` | Required `common_name`; requested `issuer_name`, `ttl`, `key_type`, `key_bits`; result includes `certificate`, `serial_number`, `issuer_id`, `key_id` |
| List roles | `LIST /{mount}/roles` | `data.keys` |
| Read role | `GET /{mount}/roles/{name}` | Current role definition |
| Create/replace role | `POST /{mount}/roles/{name}` | Complete approved definition; omitted properties default |
| Patch role | `PATCH /{mount}/roles/{name}` | `Content-Type: application/merge-patch+json`; requested changes only |

Role fields within scope: `issuer_ref`, `allowed_domains`, `allow_bare_domains`, `allow_subdomains`, `allow_glob_domains`, `allow_any_name`, `allow_ip_sans`, `allowed_uri_sans`, `ttl`, `max_ttl`, `key_type`, `key_bits`, `server_flag`, `client_flag`, `no_store`. Their values are supplied by the approved policy, not derived by this skill. A role with `key_type: any` can sign CSRs but cannot generate key pairs.

Common errors: 400 invalid request; 403 credentials/policy; 404 unavailable or hidden path (also empty LIST); 405 wrong method; 412 Enterprise consistency; 429 quota pressure; 500 internal error; 501 uninitialized; 502 external dependency error; 503 sealed/maintenance/overload. Preserve `errors` and `warnings`; accept 200 or 204 on documented successful writes. Do not interpret timeout as a safe-to-repeat creation.
