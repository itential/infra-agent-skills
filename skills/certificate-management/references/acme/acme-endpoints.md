# Endpoint Wiring — ACME Protocol (RFC 8555)

Literal request shapes behind each capability named in `acme-procedure.md`. Every path below is
relative to whatever base URL a specific CA's directory resource returns for that operation — RFC
8555 does not fix literal paths, only the resource types and the fields each carries; a CA is free to
place `newOrder`, `revokeCert`, etc. at whatever URL it wants, which is exactly why the directory
fetch is the required first step. Every authenticated request in this protocol is a JWS
(JSON Web Signature)-wrapped POST — there is no unauthenticated GET for account/order/authorization
resources; reads use "POST-as-GET" (an empty JWS payload) against the resource's own URL. Citation:
RFC 8555, IETF, retrieved 2026-09-17.

## Directory

Tool hint: `GET` (or POST-as-GET) the CA's published directory URL (CA-specific — not fixed by the
protocol; Let's Encrypt's production directory, as one example of a concrete ACME CA, is commonly
published as `https://acme-v02.api.letsencrypt.org/directory`, but this procedure and this file treat
that as one example CA's URL, not a protocol-fixed value).

Response fields: `newNonce`, `newAccount`, `newOrder`, `newAuthz` (optional), `revokeCert`,
`keyChange`, and an optional `meta` object (`termsOfService`, `website`, `caaIdentities`,
`externalAccountRequired`).

## Nonce

Tool hint: `HEAD` or `GET` the directory's `newNonce` URL. Response carries the fresh nonce in a
`Replay-Nonce` header — no response body is required to be meaningful.

## New account

Tool hint: `POST` the directory's `newAccount` URL, JWS-signed, with a payload containing `contact`
(array of contact URLs, e.g. `mailto:` addresses), `termsOfServiceAgreed` (boolean), and optionally
`externalAccountBinding` if the CA requires it (per its `meta.externalAccountRequired` flag).

Response: `201 Created` with a `Location` header giving the account URL (used as the JWS `kid` for
all later requests from this account). Account resource fields: `status` (valid | deactivated |
revoked), `contact`, `orders` (a URL for listing this account's orders).

## New order

Tool hint: `POST` the directory's `newOrder` URL, JWS-signed, payload `identifiers` (array of
`{type: "dns", value: "<domain>"}` objects; a wildcard domain is expressed as its base domain with a
leading `*.`), optionally `notBefore`/`notAfter`.

Response order object fields: `status` (pending | ready | processing | valid | invalid), `expires`,
`identifiers`, `authorizations` (array of authorization URLs to complete), `finalize` (URL to POST
the CSR to once ready), and — once valid — a `certificate` field (URL to download the issued cert).

## Read an authorization

Tool hint: POST-as-GET the authorization URL from the order's `authorizations` array.

Response fields: `identifier` (`{type, value}`), `status` (pending | valid | invalid | deactivated |
expired | revoked), `challenges` (array), `expires`, and `wildcard` (boolean, present/true only for a
wildcard identifier's authorization).

## Respond to a challenge

Tool hint: `POST` the specific challenge's own `url` (found inside the authorization's `challenges`
array), JWS-signed, with an empty object `{}` as the payload — this signals "ready to validate," it
does not itself carry the challenge value (the challenge value was already provisioned out-of-band:
at the HTTP path for `http-01`, or the DNS TXT record for `dns-01`).

Challenge object fields: `type` (`http-01` | `dns-01`, among others a CA may offer), `url`, `token`,
`status` (pending | processing | valid | invalid).

- `http-01`: the client must make the key authorization value (built from the challenge `token` and
  the account key, per the protocol's own key-authorization construction) retrievable over plain HTTP
  at `http://<identifier-value>/.well-known/acme-challenge/<token>`.
- `dns-01`: the client must publish a TXT record at `_acme-challenge.<identifier-value>` whose value
  is the base64url-encoded SHA-256 digest of that same key authorization value.

## Finalize an order

Tool hint: `POST` the order's own `finalize` URL, JWS-signed, payload `{"csr": "<base64url DER
CSR>"}`. Only valid once every identifier's authorization has already settled to `valid` — otherwise
expect a rejection rather than the order silently queuing.

## Download the certificate

Tool hint: POST-as-GET the order's `certificate` URL (only present once the order is `valid`).
Response: the issued certificate and its chain, as `application/pem-certificate-chain`.

## Revoke a certificate

Tool hint: `POST` the directory's `revokeCert` URL. Payload: `certificate` (base64url-encoded DER
certificate bytes), optional `reason` (an integer revocation-reason code — the exact accepted set was
not independently verified; confirm against the target CA's own documentation and RFC
5280's CRL reason-code registry before relying on a specific non-default value). Authentication is
either via a JWS signed with the certificate's own private key, or via the requesting account's key.
Response: `200 OK` with no required body.

## Error format

Errors are returned as `application/problem+json` documents with `type` (a URN of the form
`urn:ietf:params:acme:error:<name>`), `detail` (human-readable text), and an optional `subproblems`
array carrying per-identifier errors when an order spans multiple identifiers. Named error types
surfaced by the spec include `badNonce`, `malformed`, `unauthorized`, `rateLimited`, `badCSR`, `caa`,
`dns`, `connection`, and `userActionRequired`. A `badNonce` error response itself carries a fresh
`Replay-Nonce` header for immediate retry.
