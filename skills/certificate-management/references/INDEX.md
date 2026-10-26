# Certificate Management — Vendor/Protocol Index

One row per supported platform or protocol. Each directory holds its own `procedure.md` (the full
step-by-step), plus wire-level `endpoints.md`.

| Platform / Protocol | Directory | Scope | Notes |
|---|---|---|---|
| ACME protocol (RFC 8555) — e.g. Let's Encrypt | `acme/` | Issue, renew (as reissue), read, revoke, against any RFC 8555-compliant CA | CA-agnostic protocol coverage; no CA-specific rate limits/policy captured — confirm those against the specific CA in use. |
| HashiCorp Vault — PKI secrets engine | `vault-pki/` | Issue (Vault-generated key), sign (caller CSR), read, revoke, against an already-configured mount/role (`vault-pki-procedure.md`). CA and role setup: generate a self-signed root, generate an intermediate CSR and import its signed certificate, set the default issuer, create/patch/replace/delete roles (`vault-pki-ca-configuration-procedure.md`) | Does not cover enabling the mount, importing a CA with its private key, cross-signing, or URL/CRL/tidy configuration. No dedicated renew call — renewal is a fresh issue/sign. A role write replaces the whole role; omitted settings revert to defaults. Intermediate signing happens outside Vault. |
| AWS Certificate Manager (ACM) | `aws-acm/` | Request (issue), read, renew (managed + explicit), import, delete | Distinct from AWS Private CA's own direct issuance API. Two different renewal mechanisms with different eligibility — see `procedure.md`. |
| DigiCert ONE — Trust Lifecycle Manager | `digicert/` | Issue, read, renew, revoke (by serial number), against a REST-enabled certificate profile | REST. Revocation is permanent except the private-certificate hold reason, which is reversible per a secondary source (unverified). Field-level detail is flagged unverified in `digicert-procedure.md`. Does not cover profile/seat administration or discovery. |
| Sectigo Certificate Manager (SCM) | `sectigo/` | Enroll, collect, check status, DCV recheck, renew, replace (Sectigo Public CA only), revoke | REST, OAuth client credentials. Enroll/renew/replace are asynchronous and return a new certificate ID. Field-level detail is flagged unverified in `sectigo-procedure.md`. Does not cover SCM administration or ACME/EST. |

**Correction to shared concepts:** DigiCert's private-certificate hold is reportedly a reversible suspension (secondary source, unverified), so revocation may not be uniformly permanent, and its optional key escrow may mean a server-generated private key is not always one-time (retrieval after issuance unconfirmed). `SKILL.md` Universal concepts are hedged accordingly.
