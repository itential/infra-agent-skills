# Endpoint Wiring — Sectigo Certificate Manager (SCM) REST Enrollment API

Literal REST calls behind each operation named in `sectigo-procedure.md`. Instance host patterns and
the auth host are confirmed by Sectigo's "Understanding REST endpoints" documentation
(https://docs.sectigo.com/scm/scm-administrator/understanding-rest-endpoints, retrieved 2026-10-19).
Everything else is *(unverified)*: it comes from the API's OpenAPI definition as packaged by a third party, a
secondary source, because Sectigo's per-endpoint reference is not available as a
source here.

**Host.** Per-customer enrollment host: `https://<customer>.enroll.enterprise.sectigo.com` (Prod),
`https://<customer>.enroll.hard.sectigo.com` (Hard), or a `<customer>.rest.eu.sectigo.com` host (EU).
Outbound TCP 443 is required. The OpenAPI definition uses the `enroll.<instance>` pattern for all
instances *(unverified for EU)*.

**Auth.** OAuth 2.0 client-credentials grant against Sectigo's SSO token endpoint under
`auth.sso.sectigo.com` *(the full token path is unverified)*; the access token is sent as a bearer
token. Each enrollment endpoint has its own account tied to an organization and department.

## Enroll certificate

`POST /api/v1/certificates` — body shapes vary by certificate type. SSL-style: `csr` (required),
`customFields`, `subjAltNames`, `comments`, `externalRequester`. Other shapes add `email`, `firstName`,
`lastName`, `commonName`, `optionalFields`, and device/HSM fields (`hsmType`, `attestation`).
Response `200`: `certId`. Errors: `400` and `401`, body `code` + `description`.

## Collect certificate

`GET /api/v1/certificates/{certId}` — `200` with the certificate. `404` while issuance is pending with
`code` -103 or -109; other `404` codes mean not found. Also `400`, `401`.

## Check certificate status

`GET /api/v1/certificates/{certId}/status` — `200` with `status` and `dcvInfo`. Also `400`, `401`, `404`.

## Initiate DCV recheck

`POST /api/v1/certificates/{certId}/dcv-recheck` — `202` accepted. Also `400`, `401`, `404`.

## Renew certificate

`POST /api/v1/certificates/{certId}/renew` — body: `profileId` (optional when the endpoint has a
single profile), `csr`, `subjAltNames`, `email`, `term` (days), `comments`, `dcvMode` (`EMAIL` |
`CNAME` | `HTTP` | `HTTPS`), `dcvEmail` (for email mode), `externalRequester`, `customFields`
(mandatory custom fields must be present). Response `200`: `certId` (new ID). Also `400`, `404`.

## Replace certificate

`POST /api/v1/certificates/{certId}/replace` — body: `csr` (required), `subjAltNames`, `comments`.
Response `200`: `certId` (new ID). Also `400`, `404`.

## Revoke certificate

`DELETE /api/v1/certificates/{certId}` with a JSON body: `message` (required, audit text) and
`reasonCode` (integer, RFC 5280 codes; 0 default = unspecified, 1 = key compromise; not all accepted).
Response `200`; also `400`, `401`, `404`. This route revokes; it does not merely remove an SCM entry.
