# Certificate Management — Vendor/Protocol Index

One row per supported platform or protocol. Each directory holds its own `procedure.md` (the full
step-by-step), plus wire-level `endpoints.md`.

| Platform / Protocol | Directory | Scope | Notes |
|---|---|---|---|
| ACME protocol (RFC 8555) — e.g. Let's Encrypt | `acme/` | Issue, renew (as reissue), read, revoke, against any RFC 8555-compliant CA | CA-agnostic protocol coverage; no CA-specific rate limits/policy captured — confirm those against the specific CA in use. |
| HashiCorp Vault — PKI secrets engine | `vault-pki/` | Issue (Vault-generated key), sign (caller CSR), read, revoke, against an already-configured mount/role | Does not cover engine enablement, CA generation, or role configuration. No dedicated renew call — renewal is a fresh issue/sign. |
| AWS Certificate Manager (ACM) | `aws-acm/` | Request (issue), read, renew (managed + explicit), import, delete | Distinct from AWS Private CA's own direct issuance API. Two different renewal mechanisms with different eligibility — see `procedure.md`. |
