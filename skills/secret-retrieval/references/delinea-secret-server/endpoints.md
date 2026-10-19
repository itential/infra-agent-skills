# Endpoint Wiring — Delinea Secret Server Secret Retrieval

Literal calls behind each operation named in `procedure.md`. `{base}` is the Secret Server instance
URL (self-hosted or the Cloud tenant URL). All paths are the native Secret Server API, not the
Delinea Platform-mediated API.

Sources: Delinea Secret Server 11.6.x online help, "Script Authentication Using Tokens" and "REST
API Python Scripts", retrieved 2026-10-19. Items marked (unverified) are not stated in those pages.

## Get Token

`POST {base}/oauth2/token`

Body (form-encoded): `grant_type=password`, `username`, `password`. Optional `domain` for a
non-default domain (unverified). Optional header `OTP` carrying the one-time password when two-factor
authentication is enabled.

Response: JSON containing `access_token`.

Usage on later calls: `Authorization: Bearer <access_token>` (shown in the REST examples; the
authentication page itself does not state the header format).

## Get Secret

`GET {base}/api/v1/secrets/{secretId}`

Response (200): JSON with `id`, `name`, `active` and `items`; each item has `itemId`, `slug`,
`itemValue`.

## Get Secret Field (unverified)

`GET {base}/api/v1/secrets/{secretId}/fields/{fieldSlug}`

Response (200): the field value as a JSON-encoded string literal (quotes included).

## Update Secret

`PUT {base}/api/v1/secrets/{secretId}`

Body: the secret JSON structure with the target item's `itemValue` changed. Whether a partial body is
accepted is not stated; send the full structure.

Response (200): the updated secret JSON.

## Error handling

The source documents only success statuses (200, and 304 for conditional reads). No exact error
strings are documented; none are pattern-matched here.
