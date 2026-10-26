# HashiCorp Vault PKI — CA Generation and Role Configuration Procedure

Creates a certificate authority inside an already-enabled Vault PKI mount (a self-signed root, or an
intermediate signed elsewhere) and defines or changes the issuance roles that day-to-day issuing
depends on. Assumes an authenticated Vault client whose policy covers the mount's issuer, key, config
and role paths, and a mount that is already enabled (enabling the mount is not covered). Literal
requests and fields are in `vault-pki-ca-configuration-endpoints.md`. Day-to-day issue, sign, read and
revoke are in `vault-pki-procedure.md`. Source: HashiCorp Vault PKI secrets engine API reference
(developer.hashicorp.com/vault/api-docs/secret/pki), Vault 1.11+ multi-issuer model, retrieved
2026-10-26.

## Common Sequences

- **Inspect a mount:** Read issuers, then Read roles.
- **Stand up a self-signed root and a role:** Read issuers, Generate root, Read issuer, Set default
  issuer (only if it is meant to be the default), Create or replace role, Read role.
- **Stand up an intermediate:** Read issuers, Generate intermediate CSR, (CSR is signed by an
  external CA outside this procedure), Import signed intermediate, Read issuer, Set default issuer
  (only if it is meant to be the default), Create or replace role, Read role.
- **Retire a role:** Read role, Delete role, Read roles.
- **Adjust an existing role:** Read role, Patch role, Read role.

## Read issuers

List the mount's issuers (identifier plus operator-assigned name) and read the one of interest to see
its certificate, chain, key identifier and usage settings; read the mount's default-issuer setting too.
Listing issuers needs no token. Success is a list matching what the operator expects to exist. A
read-back warning on an issuer means its private key was exported at some point; report it as a
security finding. A 404 on a list can mean an empty mount or a hidden path; do not treat it as
permission to create a replacement.

## Generate root

Create a new self-signed root. The operator supplies the common name, validity, key type and size,
and a unique issuer name (it must be unique within the mount and cannot be `default`).

**Stop and confirm with the operator before proceeding** — this creates a new signing authority on a
live mount. Also confirm the key handling: with internal key handling the private key is never
returned and can never be fetched afterwards; with exported key handling the private key comes back
once in the response and must be stored by the operator immediately (a hard-to-undo exposure — do not
request it unless the operator explicitly asks for it).

Success: the response carries the certificate, serial number, issuer identifier and key identifier.
Generating a root never replaces an existing issuer. The new issuer becomes the default only when the
mount had no default yet (unless the mount's default-follows-latest setting is on); otherwise the
existing default is unchanged. Read the new issuer by identifier afterward. If the call times out,
list issuers before any retry; a repeat can create a second authority.

## Generate intermediate CSR

Request a signing request for an intermediate, optionally creating a fresh key. This call creates no
issuer. **Stop and confirm with the operator before proceeding** (it can create key material on the
live mount). Success is a returned CSR (plus a private key only if exported handling was chosen).
The CSR must be signed by an external CA; that signing step is outside this procedure and the
signing CA's own parameters govern the final certificate.

## Import signed intermediate

Submit the signed certificate (and its chain, concatenated as PEM) to the same mount that produced
the CSR, so it pairs with the key already held there. **Stop and confirm with the operator before
proceeding.** Success: the response names the newly imported issuer and the key it maps to. A
certificate without a matching key in the mount becomes a key-less issuer, which cannot issue
certificates or sign CRLs. Only certificates asserting CA status are accepted.

## Set default issuer

Choose which issuer serves requests that do not name one (including roles whose issuer reference is
`default`). **Stop and confirm with the operator before proceeding**: this changes which authority
signs for every role and path that relies on the default, and some mount functions do not work with
no default configured. Success: reading the default-issuer setting returns the chosen issuer.

## Read roles

List role names and read the selected role to see its full definition. A not-found result can mean
the role is absent or the caller lacks permission to see it; the response does not distinguish them.

## Create or replace role

The operator supplies the complete definition: issuer reference, permitted names (domains and the
matching modes that apply to them), SAN permissions, validity (default and maximum), key type and
size, usage flags, and whether certificates are stored. This procedure derives none of those values.

**Stop and confirm with the operator before proceeding.** A write to an existing role replaces it
entirely, and any property left out reverts to its default, which can widen what the role allows.
Read the current role first and send every property that should survive. Success: reading the role
back shows exactly the approved values. A rejected value is corrected and re-confirmed, not
retried blindly; after a timeout, read the role before writing again.

## Patch role

Change only specific properties of an existing role. **Stop and confirm with the operator before
proceeding**, showing the before and after values for each property. Success: the read-back shows
the requested changes and every untouched property unchanged.

## Delete role

**Stop and confirm with the operator before proceeding.** Removing a role stops further issuance
under that name but does not revoke certificates it already issued; revoke those separately via the
issue/sign/revoke procedure if needed. Success: the role no longer appears in the role list.

## Patterns

- **Name-matching options add up rather than narrow.** The domain-matching switches, the any-name
  switch and the usage flags each widen what is allowed; the allowed-domains list is ignored entirely
  when any-name is on. Review the role as the union of what its options permit.
- **A role stores its issuer reference exactly as given.** A name is not converted to an identifier,
  so deleting or renaming that issuer can make issuance fail or fall through to a different issuer.
  Reference by identifier when the intent is a specific authority; after any issuer rename or
  delete, re-read every role that points at it.
- **Per-issuer issue/sign paths can bypass a role's issuer reference.** Restrict access to those
  paths in Vault policy if the role's issuer must be the only one used; the role setting alone is
  not an access control.
- **A role with the "any" key type can sign CSRs but cannot generate key pairs.**
- **Skipping storage has consequences.** Certificates from a role that does not store them cannot be
  listed or revoked by serial number (only revoked by presenting the certificate).
- **A created CA is trusted only inside Vault.** Distributing the CA certificate to relying systems is
  a separate action.

## Known limitations

- Covers CA generation (self-signed root, intermediate CSR and import), setting the default issuer,
  and role create, read, patch, replace and delete. Does not cover enabling or disabling the
  mount, importing a CA together with its private key, key or issuer deletion, cross-signing, managed
  (KMS-backed) keys, root rotation shortcuts, URL/CRL/OCSP configuration, tidy settings, or Enterprise
  external-policy features.
- Unverified: whether the patch operation requires a specific content type. The docs describe the
  patch format only by reference to the KV v2 engine's format. Assumption: it takes the merge-patch
  content type; if rejected, fall back to reading and replacing the full role.
- Not documented: rate limits and quotas. On HTTP 429, back off and honor any `Retry-After`.
- Irreversible: a root's internal private key cannot be recovered, and an exported one cannot be
  un-exported.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read issuers | List issuers, read one issuer, read default-issuer setting | Read |
| Generate root | Create a self-signed root issuer and key | Authority write |
| Generate intermediate CSR | Produce a CSR for external signing | Authority write |
| Import signed intermediate | Attach the signed certificate to the mount | Authority write |
| Set default issuer | Choose the default issuer | Configuration write |
| Read roles | List roles, read one role | Read |
| Create or replace role | Write a complete role definition | Policy write |
| Patch role | Change selected role properties | Policy write |
| Delete role | Remove a role | Policy write |

## Verification checklist

- [ ] Operator confirmation obtained before every write above
- [ ] Reading the new issuer shows the intended subject, validity and key handling (no private key
      returned unless explicitly requested), with any exported-key warning surfaced
- [ ] Default-issuer setting is what the operator intended
- [ ] Read-back of each role matches the approved definition, with its issuer reference resolving to
      an existing issuer
- [ ] Authority creation was not reported as trust distribution to clients
