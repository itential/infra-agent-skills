# HashiCorp Vault PKI Secrets Engine — Certificate Lifecycle Procedure

Issues, reads, and revokes X.509 certificates from a HashiCorp Vault PKI secrets engine mount, acting
as an internal or intermediate certificate authority under Vault's own management. Assumes an
authenticated Vault client (a token or other auth method with policy access to the target PKI mount's
paths) and a PKI secrets engine already enabled and configured with at least one issuer (root or
intermediate CA) and at least one role are already in place — this procedure does not cover enabling
the engine; generating CA material and configuring roles is in `vault-pki-ca-configuration-procedure.md`. See `vault-pki-endpoints.md` for the
literal request paths and fields behind every operation below. Citation: HashiCorp Vault API
documentation, "PKI Secrets Engine (API)," retrieved 2026-09-17, spot-checked again 2026-09-29
(https://developer.hashicorp.com/vault/api-docs/secret/pki).

## Operational procedure

### Issue a certificate (Vault generates the key pair)

Request a new certificate against a specific role, supplying the common name and any additional
Subject Alternative Names (additional DNS names, IP addresses, or URIs) the certificate should
cover, plus how long the certificate should be valid for. Vault generates a fresh private key,
signs a certificate for it under the mount's issuer, and returns the certificate, its private key,
the issuing CA's certificate, and the full chain in the response.

**Capture the private key from this response immediately — Vault does not retain it.** Once this
response has been received and not saved, the private key is not recoverable from Vault; the only
remedy is requesting a new certificate. This is a deliberate design choice by Vault, not an error
condition to troubleshoot.

The role a certificate is issued against constrains what the request is allowed to specify — the
role determines which domains are permitted, whether names outside the role's allowed set are
rejected outright, whether IP or URI SANs are permitted at all, the maximum lifetime any request
against it can obtain, and the key type/size used. A request naming a domain or SAN type the role
doesn't permit is expected to be rejected, not silently narrowed.

### Sign a certificate from a caller-supplied CSR (Vault never sees the private key)

When the private key must never leave the requesting system, submit a PEM-encoded certificate
signing request against a role instead of requesting a Vault-generated key pair. Vault validates the
request against the same role constraints described above, signs the public key from the CSR, and
returns the certificate, issuing CA, and chain — with no private key in the response, since Vault
never held one.

### Read a certificate

Fetch a previously issued certificate by its serial number to retrieve it again in isolation from the
original issuance response — useful when the original response wasn't retained or when auditing what
a mount has issued. A list operation returns the serial numbers of every certificate this mount has
on record. Note that if a role was configured to skip storing issued certificates, a certificate
issued under it will not appear in either the by-serial read or the list — storage of issued material
is a per-role/per-mount setting, not a guarantee that applies universally.

The mount's own CA certificate, and its full trust chain, can also be read directly — useful for
distributing the mount's CA certificate to trusting systems without needing to go through an
issued-leaf-certificate lookup.

### Revoke a certificate

**Stop and confirm with the operator before proceeding — revocation is expected to be permanent** and
immediately affects any relying party that checks Vault's CRL or OCSP responder for this mount.
Submit either the certificate's serial number or the certificate itself (exactly one of the two, not
both) to revoke it; Vault records a revocation time and the certificate's serial is added to the
mount's revocation data, which feeds its CRL.

A separate revocation path exists for the case where the caller holds the certificate's private key
but doesn't otherwise have permission to call the standard revoke operation — supplying the private
key alongside the certificate/serial as proof of possession is accepted as sufficient authorization
for that path specifically, independent of the caller's normal Vault ACL policy for revocation.

### Adjacent maintenance (not part of core issue/read/revoke, but relevant to their correctness)

Vault periodically needs its expired-certificate and stale-revocation bookkeeping cleaned up (a
"tidy" operation) and its CRL rebuilt on demand — these are mount-maintenance actions an operator runs
separately from any single certificate's lifecycle, not steps this procedure's issue/read/revoke flow
triggers automatically.

## Patterns

- **There is no dedicated renewal call in this engine — renewing is issuing a new certificate under
  the same role.** Vault's PKI secrets engine reference does not describe a "renew" operation that
  preserves a serial number or otherwise differs mechanically from a fresh issue call; treat renewal
  as "issue again before the old one expires," the same role constraints applying each time.
- **A role is the authorization boundary, not the issue call's parameters.** The role decides what
  names/SAN types/lifetimes are acceptable before the issue or sign call is ever evaluated against a
  specific request; don't assume a broader request will be narrowed down to what's allowed — expect
  outright rejection instead.
- **"No private key stored" is a security property to plan around, not a transient state.** Every
  Vault-generated-key issuance is a one-time opportunity to capture the private key; there is no
  later retrieval call for it.
- **Revocation has two authorization paths** — the caller's normal Vault policy permissions, or proof
  of possession of the certificate's own private key — either is sufficient, which matters when
  deciding who is allowed to revoke a given certificate under the operator confirmation gate above.

## Known limitations

- Covers issuing (Vault-generated key), signing (caller-supplied CSR), reading, and revoking
  certificates against an already-configured PKI mount and role. Does not cover enabling the PKI
  secrets engine or the intermediate-CA cross-signing operations (sign-intermediate, sign-verbatim)
  the engine also exposes. CA generation and role configuration are in
  `vault-pki-ca-configuration-procedure.md`.
- The exact live per-certificate revocation-status check (OCSP) is known to exist on this engine, but
  its precise request/response shape is not confirmed — treat
  "Vault can serve OCSP responses for this mount" as true, but confirm the literal call shape against
  Vault's own documentation before wiring an OCSP check into automation.
- Default lifetimes, default key type/size, and other role-level defaults are configured per role
  (and can inherit mount-level defaults) — this procedure does not assume any specific default values;
  confirm the target role's actual configuration before assuming a request without an explicit TTL or
  key-type value will behave a particular way.
- Tidy scheduling and CRL rebuild cadence are operator/administrator configuration on the target Vault
  installation, not something this procedure can assume a fixed value for.

## Tools

| Operation | Description | Category |
|---|---|---|
| Issue (Vault-generated key) | Request a new certificate and key pair under a role | Issuance |
| Sign (caller CSR) | Sign a caller-supplied CSR under a role, no key generated by Vault | Issuance |
| Read certificate by serial | Retrieve a previously issued certificate | Read |
| List certificates | List serial numbers this mount has issued | Read |
| Read CA/chain | Retrieve the mount's own CA certificate and trust chain | Read |
| Revoke | Revoke a certificate by serial number or certificate body | Revocation |
| Revoke with key | Revoke using private-key possession as proof of authorization | Revocation |

## Verification checklist

- [ ] A Vault-generated private key from an issue response was captured immediately — not assumed
      retrievable later
- [ ] The target role's allowed domains/SAN types/max lifetime were checked before assuming a request
      would succeed with the values being requested
- [ ] Renewal was treated as a fresh issue/sign call under the same role, not assumed to reuse the
      prior certificate's serial number
- [ ] Revocation was preceded by explicit operator confirmation, and used either standard policy
      permission or private-key proof-of-possession as its authorization path
- [ ] If a certificate wasn't found on a by-serial read or list, whether the issuing role was
      configured to skip storage was checked before assuming the certificate doesn't exist
