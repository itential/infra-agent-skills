# Endpoint Wiring — HashiCorp Vault PKI Secrets Engine

Literal API calls behind each capability named in `vault-pki-procedure.md`. Paths below assume the
engine is mounted at its conventional default path `pki` — an operator can mount it elsewhere, in
which case substitute that mount path. Citation: HashiCorp Vault API documentation, "PKI Secrets
Engine (API)," retrieved 2026-09-17, spot-checked and corrected 2026-09-29 against the same source
(https://developer.hashicorp.com/vault/api-docs/secret/pki) — the CRL-rotate and issuer-scoped
CRL-read paths below were wrong in the 2026-09-17 pass and are now verified directly against the
docs' own method/path tables.

## Issue a certificate (Vault-generated key pair)

Tool hint: `POST /pki/issue/:role_name` (uses the mount's default issuer), or
`POST /pki/issuer/:issuer_ref/issue/:role_name` (names a specific issuer explicitly, on a mount
configured with more than one).

Body fields: `common_name` (required if the role's `require_cn` is true), `alt_names`
(comma-separated additional DNS names), `ip_sans` (comma-separated IP SANs), `uri_sans`
(comma-separated URI SANs), `ttl` (requested lifetime — capped by the role's configured `max_ttl`),
`not_after` (an absolute UTC expiration timestamp, `YYYY-MM-DDTHH:MM:SSZ`, as an alternative to
`ttl`), `format` (`pem` | `der` | `pem_bundle` | `pkcs12_bundle` | `jks_bundle`),
`exclude_cn_from_sans` (boolean — omit the common name from the certificate's DNS/email SAN list).

Response fields: `certificate`, `private_key`, `issuing_ca`, `ca_chain` (array), `serial_number`
(colon-separated hex), `expiration` (Unix timestamp).

## Sign a caller-supplied CSR

Tool hint: `POST /pki/sign/:role_name`, or `POST /pki/issuer/:issuer_ref/sign/:role_name`.

Body fields: `csr` (required, PEM-encoded), `common_name` (required), plus the same `alt_names`,
`ip_sans`, `uri_sans`, `ttl`, `not_after`, `format`, `exclude_cn_from_sans` fields as the issue call.

Response: identical shape to the issue response, minus `private_key` (Vault never generated one).

## Read a certificate by serial number

Tool hint: `GET /pki/cert/:serial` (unauthenticated per the engine's own access model — this mirrors
that certificates are public material once issued).

## List certificates

Tool hint: `LIST /pki/certs` — returns the serial numbers this mount has record of.

## Read the mount's own CA certificate / chain

Tool hint (unauthenticated): `GET /pki/cert/ca` (JSON), `GET /pki/ca` (DER), `GET /pki/ca/pem` (PEM)
for the mount's default issuer; `GET /pki/issuer/:issuer_ref/{json|der|pem}` for a specific issuer on
a multi-issuer mount. Full chain: `GET /pki/ca_chain` (PEM) or `GET /pki/cert/ca_chain` (JSON).

## Read CRL

Tool hint (unauthenticated): for the mount's default issuer, `GET /pki/crl` (DER) or `GET
/pki/crl/pem` (PEM) for the full CRL, `GET /pki/crl/delta` (DER) or `GET /pki/crl/delta/pem` (PEM)
for the delta CRL. For a specific issuer on a multi-issuer mount, substitute
`GET /pki/issuer/:issuer_ref/crl` (JSON), `.../crl/der`, or `.../crl/pem` for the full CRL, and the
equivalent `.../crl/delta`, `.../crl/delta/der`, `.../crl/delta/pem` paths for the delta CRL — there
is no combined `/pki/crl/:issuer_ref` path.

## Revoke a certificate

Tool hint: `POST /pki/revoke`.

Body: exactly one of `serial_number` (colon- or hyphen-separated hex) or `certificate` (PEM) —
supplying both is not a valid combination per the engine's own documented constraint.

Response: `{"data": {"revocation_time": <unix timestamp>}}`.

## Revoke using private-key possession as authorization

Tool hint: `POST /pki/revoke-with-key`.

Body: `serial_number` or `certificate` (as above), plus `private_key` (PEM) as proof of possession.
This path is documented as not requiring the normal ACL-level revoke permission specifically because
supplying the matching private key is itself treated as sufficient proof of authority to revoke —
the endpoint remains authenticated (a valid Vault token is still required) to prevent abuse, it is
just not gated by the same policy check as the plain revoke path.

## List revoked / pending-revocation certificates

Tool hint: `LIST /pki/certs/revoked` (serials revoked at this cluster); `LIST
/pki/certs/revocation-queue` (serials with cross-cluster revocation requests pending, relevant to
Vault installations using performance replication across clusters).

## Roles (read-only reference here; creating and changing roles is in `vault-pki-ca-configuration-endpoints.md`)

Tool hint: `LIST /pki/roles`, `GET /pki/roles/:name`. A role response includes (among other fields)
`allow_any_name`, `allowed_domains`, `allow_bare_domains`, `allow_subdomains`, `allow_glob_domains`,
`allow_ip_sans`, `key_type`, `key_bits`, `ttl`, `max_ttl`, `require_cn` — these are the fields that
determine whether a given issue/sign request against that role will be accepted.

## Maintenance (adjacent, not part of core issue/read/revoke)

Tool hint: `POST /pki/tidy` (clean up expired/stale data), `GET /pki/crl/rotate` (force-rebuild the
CRL on demand — a GET despite being state-changing, per the engine's own documented call shape),
`GET /pki/tidy-status` (progress of an in-flight tidy operation).

## Formats and defaults worth noting

`format` accepts `pem`, `der`, `pem_bundle`, `pkcs12_bundle`, `jks_bundle`. When a PKCS#12 or JKS
bundle is requested, `pkcs12_password`/`jks_password` default to the literal string `"changeit"` if
not supplied by the caller — treat this as a value to override explicitly for anything beyond local
testing, not a value safe to leave at its default in a shared environment.
