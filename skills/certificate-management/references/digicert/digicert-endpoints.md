# Endpoint Wiring — DigiCert ONE Trust Lifecycle Manager

Literal REST calls behind each operation named in `digicert-procedure.md`. Route existence for issue,
renew, and revoke is confirmed by DigiCert's Trust Lifecycle API documentation
(https://dev.digicert.com/trust-lifecycle-api.html, retrieved 2026-10-19). All other details are
*(unverified)*: they come from the API's OpenAPI definition as packaged by a third party, a
secondary source, because DigiCert's per-endpoint reference pages were not fetchable.

**Host and auth.** Requests go to the account's DigiCert ONE host (`https://<host>`; `one.digicert.com`
is the default in the OpenAPI definition *(unverified)*). Authentication is a service-user API token
sent in the `X-API-Key` header *(unverified)*; the token is created in the account's Account Manager
under service users.

## Issue certificate

`POST /mpki/api/v1/certificate`

Body: `profile` (profile ID), `seat` (seat ID), `csr` (omit only with key escrow), `validity`,
`delivery_format` (`x509` | `pkcs7` | `pkcs12` | `pkcs12_pem`), `include_ca_chain`, `attributes` (the
subject/SAN values the profile requires), `tags`; a second documented body shape adds `cert_owner_ids`,
`ca_attributes`, `custom_attributes`.

Response: `201`. Fields of note: `serial_number`, `certificate`, `delivery_format`, `pkcs12_password`,
`request_id`, `dv_details`. For Microsoft CA templates only `request_id` is returned; pickup is
`GET /mpki/api/v1/certificate-pickup/{request_id}` *(this pickup route is named only in the OpenAPI
description and is not in the path list of the packaged definition; treat as unverified)*.
Documented error: `429`.

## Get certificate

`GET /mpki/api/v1/certificate/{serial_number}` — optional query `thumbprint_sha256`. Response `200`
with certificate details. Additional formats: `GET /mpki/api/v1/certificate/{serial_number}/additional-formats`.

Collision error text: `Collision occurred! Please specify additional parameter: thumbprint_sha256`.

## Renew certificate

`POST /mpki/api/v1/certificate/{serial_number}/renew` — optional query `thumbprint_sha256`,
`account_id`. Body (all optional): `csr`, `validity`, `delivery_format`, `include_ca_chain`,
`renewal_comment`. Response `200` with the renewed certificate record (fields include `id`,
`common_name`, `days_till_renewal`, `key_type`, `key_length`, `auto_renew_status`).

## Revoke certificate

`PUT /mpki/api/v1/certificate/{serial_number}/revoke` — optional query `thumbprint_sha256`.
Body: `revocation_reason` (required). Values: `unspecified`, `key_compromise`, `affiliation_changed`,
`superseded`, `cessation_of_operation`, `privilege_withdrawn`, `ca_compromise`, `certificate_hold`;
public/ACME certificates accept only `key_compromise`, `affiliation_changed`, `superseded`,
`cessation_of_operation`. (The packaged enum omits `ca_compromise` while the description lists it —
a defect in the secondary source; confirm against DigiCert's reference.) Response `204`, no body.

Resume a suspended private certificate: the OpenAPI description points to a delete operation on the
same revoke route; the method is *(unverified)* and not in the packaged path list — consult DigiCert's
API reference before use.
