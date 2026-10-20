# Sectigo Certificate Manager — Certificate Lifecycle Procedure

Enrolls, collects, checks, renews, replaces, and revokes certificates through the Sectigo Certificate
Manager (SCM) REST enrollment API. Assumes OAuth client credentials for an SCM enrollment endpoint
account are already available. See `sectigo-endpoints.md` for the literal routes and field tables
behind every operation named below.

**Sourcing note.** Lifecycle concepts (statuses, renew vs. replace, permanence of revocation, the
separation of deleting an entry from revoking) were confirmed against Sectigo's own documentation
(Sectigo Certificate Manager Documentation: "Understanding SSL certificates", "Managing SSL
certificates", and "Understanding REST endpoints" at https://docs.sectigo.com/scm/, retrieved
2026-10-19). Sectigo's per-endpoint REST reference was not fetchable in this research pass, so all
request/response detail marked *(unverified)* comes from a third-party packaged OpenAPI definition of this API, a
secondary source. Confirm those details against Sectigo's current
REST API reference before relying on them.

## Common Sequences

- **Enroll and collect:** Enroll certificate → Check certificate status (repeat until issued) →
  Collect certificate.
- **Renew:** Check certificate status → Renew certificate → Check status → Collect certificate.
- **Revoke:** Check certificate status → Revoke certificate (operator confirmation required).

## Operational procedure

### Enroll a certificate

Submit an enrollment request containing a CSR (single-line Base64 PKCS#10) and the custom fields the
enrollment endpoint's profile requires; SAN values, comments, and requester details are optional or
profile-dependent *(unverified)*. The set of accepted fields differs by certificate type (SSL, client,
device, code signing) and by profile, so the field list the endpoint accepts must match the account's
profile.

Success: the response contains a certificate ID. Issuance is not always immediate; the ID is used to
collect the certificate later. A 400 response carries a code and description naming what was wrong with
the request — correct it rather than retrying unchanged. A 401 means the access token is missing or
expired.

### Check certificate status and domain validation

Read the status of a certificate by its ID. The response gives its status and, where relevant, domain
control validation (DCV) information. Documented statuses cover the request pipeline (requested,
approved, applied), the active state (issued), end states (expired, revoked), and failures (declined,
invalid, rejected). If DCV has stalled after the validation record or approval has been completed, a
recheck can be triggered, which asks the CA to re-evaluate the domain *(unverified: DCV modes are
CNAME, EMAIL, HTTP, HTTPS; the DCV recheck call returns 202 and is asynchronous)*.

### Collect a certificate

Download the issued certificate by its ID. While issuance is pending, the call returns 404 with a
response code of -103 or -109 *(unverified)*; this means "not ready yet", not "does not exist" — check
status and retry later. A 404 with any other code should be treated as an unknown or wrong ID.

### Renew a certificate

Request renewal by the existing certificate's ID. Renewal extends the validity of an active
certificate; depending on the profile, a new key pair is required or the existing key pair and details
may be reused (confirmed). The renew call may need the profile ID, requested term in days, SANs,
requester email, DCV mode, and custom fields *(unverified)*. Success: the response contains a
certificate ID to collect from. This is a **new certificate ID**, so the renewed certificate is a
separate object from the one it renews — record the new ID.

Renewing a certificate deployed to Apache or Apache Tomcat requires restarting that endpoint after the
new certificate is deployed (confirmed); this procedure does not perform deployment.

### Replace a certificate

Replacement issues a new certificate in place of an existing one, for example to change key
parameters or the SAN list. It is available only for certificates issued by the Sectigo Public CA
(confirmed). Supply a CSR; SAN list and comments are optional *(unverified)*. Success returns a
certificate ID to collect from.

**Stop and confirm with the operator before proceeding.** What happens to the original certificate
after a replace (whether it is revoked, left valid, or expires on its own) was not confirmed; consult
platform-specific guidance, and do not assume the original stays usable.

### Revoke a certificate

**Stop and confirm with the operator before proceeding — revocation is permanent**; no reversal
exists in the documentation. Supply a human-readable message (required, recorded for audit and
notification purposes) and optionally an RFC 5280 reason code (default 0, unspecified; not every code
is accepted *(unverified)*). Success is a 200 response. Deleting a certificate's entry in SCM is a
different action that does not revoke the certificate (confirmed) — never use it as a substitute.

## Patterns

- **Enrollment is asynchronous.** Enroll, renew, and replace each return an ID rather than a
  certificate; always follow with status check and collect.
- **Renew and replace both yield a new certificate ID**; the old certificate is not changed in place.
- **A 404 on collect can mean "pending".** Distinguish by the response code before treating it as a
  failure.
- **Base URL and token are per instance and per customer**, and the instance (enterprise, hard, EU)
  changes the host.

## Known limitations

- Covers SSL-style certificate enrollment, collection, status, DCV recheck, renew, replace, and revoke
  through the enrollment API. Does not cover SCM administrator functions (organizations, departments,
  profiles, approvals), ACME/EST enrollment, or certificate deployment.
- Field lists differ by certificate type and profile and were not confirmed against primary reference
  pages (see sourcing note); revocation reason-code acceptance is likewise unconfirmed.
- Revocation is irreversible.

## Tools

| Operation | Description | Category |
|---|---|---|
| Enroll certificate | Submit a CSR-based enrollment request | Issuance |
| Check certificate status | Read status and DCV information | Read |
| Initiate DCV recheck | Ask the CA to re-check domain validation | Validation |
| Collect certificate | Download an issued certificate | Read |
| Renew certificate | Request renewal of an existing certificate | Renewal |
| Replace certificate | Issue a replacement (Sectigo Public CA only) | Issuance |
| Revoke certificate | Revoke a certificate by ID | Revocation |

## Verification checklist

- [ ] The enrollment endpoint's profile and certificate type were matched to the fields submitted
- [ ] Status was read from the status call before collecting, not inferred from a collect failure
- [ ] A collect 404 with code -103 or -109 was treated as pending rather than failed
- [ ] The new certificate ID from a renew or replace was recorded as a separate certificate
- [ ] Replace was used only for Sectigo Public CA certificates, after explicit operator confirmation
- [ ] Revocation was preceded by explicit operator confirmation and not replaced by an entry delete
