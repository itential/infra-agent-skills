# DigiCert ONE Trust Lifecycle Manager — Certificate Lifecycle Procedure

Issues, reads, renews, and revokes certificates through the REST API of DigiCert ONE's Trust Lifecycle
Manager service, for certificate profiles that allow direct API enrollment. Assumes an API token for a
service user in the target DigiCert ONE account is already available. See `digicert-endpoints.md` for
the literal routes and field tables behind every operation named below.

**Source confidence.** The existence of the issue, renew, and revoke routes and the
one-certificate-per-call revocation limit are documented by DigiCert (Trust Lifecycle API page and
the "Revoke certificates" page in the Trust Lifecycle Manager docs, retrieved 2026-10-19).
DigiCert's per-endpoint reference pages are not available as a source here, so every field-level
detail, eligibility rule, and status value below that is marked *(unverified)* comes from a
third-party packaged OpenAPI definition of this API, a secondary source. Confirm those details
against DigiCert's current API reference before relying on them.

## Common Sequences

- **Issue and collect:** Issue certificate → (if only a request identifier came back) Read certificate.
- **Renew:** Read certificate (confirm it is inside its renewal window) → Renew certificate.
- **Revoke:** Read certificate → Revoke certificate (operator confirmation required).

## Operational procedure

### Issue a certificate

Submit an issuance request naming the certificate profile to use and the seat to apply, plus the
subject and SAN values the profile requires, and a CSR unless the profile has DigiCert-side key escrow
enabled (then DigiCert generates the key and no CSR is sent). Issuance through this API works only for
profiles configured for REST API enrollment with third-party-app authentication *(unverified)*. Every
subject/SAN field the profile sources from the REST request and marks required must be supplied in the
request *(unverified)*.

Success: HTTP 201 with the certificate in the requested delivery format and its serial number. For
certificates from a Microsoft CA template the response carries only a request identifier, and the
certificate is collected afterward through a separate pickup call *(unverified)*. A PKCS#12 delivery
returns a generated password in the response — capture it at that moment.

Errors: 429 means the call was rate limited; back off and retry, honoring any `Retry-After` header
(limits themselves are not documented in the sources used). A missing required profile field or an
ineligible profile is a request error; correct the request rather than retrying unchanged.

### Read a certificate

Fetch a certificate's details by its serial number. If more than one certificate in the account shares
the serial number, the call fails with a collision error; repeat it with the SHA-256 thumbprint added
as a filter. Additional delivery formats of an issued certificate are retrievable through a separate
read call keyed on the same serial number.

### Renew a certificate

Request renewal by serial number, optionally supplying a CSR (new or existing public key), validity,
delivery format, and a renewal comment. Eligibility *(unverified)*: only certificates from profiles
configured for REST API enrollment with third-party-app authentication, and only inside the profile's
renewal period (a 30-day default is stated). With key escrow enabled no CSR is required.

Success: HTTP 200 with the renewed certificate's record. Whether the renewed certificate keeps the
original serial number was not confirmed — read the response and treat the returned record, not the
old serial number, as the identity of the renewed certificate.

### Revoke a certificate

**Stop and confirm with the operator before proceeding.** Revocation of a public or ACME-based
certificate is treated as permanent: no reversal operation is documented for it in the sources used.
Revocation processes one certificate per call; revoking many means calling once per serial number.
Before revoking, the service must have access to the issuing CA, which for non-DigiCert private CAs
means an active CA connector must exist (confirmed in DigiCert's revoke-certificates page).

Supply a revocation reason *(unverified)*: public/ACME certificates accept key compromise,
affiliation changed, superseded, or cessation of operation; private certificates additionally accept
unspecified, privilege withdrawn, CA compromise, and certificate hold. Success: HTTP 204, no body.
If the serial number collides, retry with the SHA-256 thumbprint filter.

**Certificate hold is the exception to permanence** *(unverified)*: for a private certificate, the hold
reason suspends it by listing it temporarily on the CRL until it expires or a separate resume-suspended
operation removes it. Treat hold as reversible and every other reason as irreversible.

## Patterns

- **Issuance is profile-gated.** A certificate enrolled through another path (enrollment codes,
  protocols) may not be renewable through this API. Check the profile before assuming renewal works.
- **Serial numbers are not guaranteed unique per account**; keep the thumbprint available for
  read and revoke calls.
- **Key handling depends on the profile.** With key escrow DigiCert generates the key; without it the
  caller's CSR is the only key input. Whether and how an escrowed key can be retrieved later was not
  confirmed.

## Known limitations

- Covers issue, read, renew, and revoke by serial number only. Does not cover enrollment workflows,
  profile/seat/business-unit/owner administration, certificate search, discovery, or import.
- Bulk revocation by deleting seat records exists per DigiCert's docs but is outside this procedure.
- Rate limits, the full revocation-reason vocabulary per CA type, and renewal-period rules were not
  confirmed against primary reference pages (see Source confidence).
- Revocation (other than hold) is irreversible.

## Tools

| Operation | Description | Category |
|---|---|---|
| Issue certificate | Issue a certificate from a REST-enabled profile | Issuance |
| Get certificate | Read a certificate by serial number | Read |
| Renew certificate | Renew an eligible certificate by serial number | Renewal |
| Revoke certificate | Revoke one certificate by serial number | Revocation |

## Verification checklist

- [ ] The certificate's profile was confirmed REST-enrollment-enabled before issue or renew
- [ ] Issue success was confirmed by a 201 response carrying the certificate or a request identifier
- [ ] Renewal eligibility (profile type and renewal window) was checked before calling renew
- [ ] The renewed certificate was identified from the renew response, not assumed to keep its serial
- [ ] Revocation was preceded by explicit operator confirmation and, for non-DigiCert private CAs, a
      working CA connector; success was a 204 response
- [ ] For a hold, the operator understood it as reversible; for any other reason, as permanent
