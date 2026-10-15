# Endpoints — Salesforce Contact CRUD

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST
client/adapter is assumed available. Paths below use `vXX.0` as a stand-in for whichever REST API
version the calling tool targets (Salesforce versions the API by number, e.g. `v62.0`); confirm the
exact version segment the target org/tool expects rather than assuming it's fixed.

## Authentication — token host vs. API host

Salesforce issues OAuth 2.0 access tokens through a connected app / external client app using one of
Salesforce's supported grant flows (authorization code / web server, client credentials, JWT bearer,
device — the exact flow depends on the integration's own trust model and is a caller decision, not
part of this procedure). The token exchange itself is a POST to a token endpoint under a login/
authorization host (for example `https://login.salesforce.com/services/oauth2/token`, or an org's own
My Domain equivalent).

**The token response body carries the host to use for subsequent API calls** — a field named
`instance_url` alongside `access_token`, `token_type` (`Bearer`), and related fields. Every Contact
CRUD call below is made against that `instance_url`, not against the login/token host. Every call
carries the token as `Authorization: Bearer <access_token>`.

## Base path

```
{instance_url}/services/data/vXX.0/sobjects/Contact
```

## Create a Contact

```
POST {instance_url}/services/data/vXX.0/sobjects/Contact
Content-Type: application/json
Authorization: Bearer <access_token>
```

Body: a flat JSON object of field name/value pairs (e.g. `LastName`, `FirstName`, `Email`, `Phone`,
plus any other accessible standard or custom field). No field is implicitly defaulted beyond what the
org itself configures.

**Success:** HTTP 201. Response body:
```
{"id": "<18-char record id>", "success": true, "errors": []}
```

**Failure:** HTTP 4xx with a JSON array body, each element shaped like:
```
{"message": "<human-readable text>", "errorCode": "<code>", "fields": ["<field name>", ...]}
```
Surface `message`/`errorCode`/`fields` verbatim per `procedure.md` step 7 — do not paraphrase or
invent a code not present in the response.

## Retrieve a Contact

```
GET {instance_url}/services/data/vXX.0/sobjects/Contact/{recordId}?fields=<comma-separated field list>
Authorization: Bearer <access_token>
```

`recordId` is the Salesforce record identifier (an 18-character id is the safe form to use
case-insensitively; a 15-character id is case-sensitive). The `fields` query parameter is optional —
omitting it returns every field the authenticated user is permitted to see.

**Success:** HTTP 200 with a JSON object of field name/value pairs.

**Failure:** HTTP 404 (record id not found, or not visible to the authenticated user — the response
does not distinguish the two) with the same error-array shape as Create.

## Update a Contact

```
PATCH {instance_url}/services/data/vXX.0/sobjects/Contact/{recordId}
Content-Type: application/json
Authorization: Bearer <access_token>
```

Body: a flat JSON object containing only the fields being changed — this is a partial update.

**Success:** HTTP 204, empty response body.

**Failure:** same error-array shape as Create, on a 4xx status.

## Delete a Contact

**Destructive — see `procedure.md` step 6's confirmation gate before issuing this call.**

```
DELETE {instance_url}/services/data/vXX.0/sobjects/Contact/{recordId}
Authorization: Bearer <access_token>
```

**Success:** HTTP 204, empty response body.

**Failure:** HTTP 404 if the record id doesn't exist (already deleted, or never existed); same
error-array shape as Create for other 4xx conditions.

## Status codes observed across all four calls

- `400` — malformed request (invalid field name, badly-formed payload).
- `401` — access token missing, invalid, or expired.
- `403` — the authenticated user lacks object/field-level or sharing permission for the operation.
- `404` — the object type or record id was not found (or not visible).
- Salesforce's own REST API documentation does not enumerate every possible `errorCode` string beyond
  these status-level categories — treat any `errorCode` value the response actually returns as
  authoritative rather than checking it against a fixed list.
