# Endpoint Wiring — 1Password Connect Secret Retrieval

Literal API calls behind each capability named in `procedure.md`. All calls are the 1Password
Connect Server REST API, JSON request/response bodies, authenticated with a Bearer token issued
when the Connect server was deployed.

Source: www.1password.dev/connect/connect-api-reference/ (redirect target of
developer.1password.com/docs/connect), retrieved 2026-09-29.

## Authentication header (all calls below)

```
Authorization: Bearer <connect access token>
Content-Type: application/json
```

## List Vaults

`GET /v1/vaults`

Optional query: `filter` — SCIM-style expression, e.g. `filter=name eq "Automation Vault"`.

Response: array of vault summary objects (id, name, and related metadata) — no items.

## List Items in a Vault

`GET /v1/vaults/{vaultUUID}/items`

Optional query: `filter` — SCIM-style title/tag filter.

Response: array of item summary objects — titles, ids, categories, tags — **without** field
contents.

## Get an Item's Full Contents (including field values)

`GET /v1/vaults/{vaultUUID}/items/{itemUUID}`

Response: the full item object, including a `fields` array. Each field entry carries `id`, `label`,
`type` (e.g. `STRING`, `CONCEALED`, `EMAIL`, `URL`, `OTP`), `purpose` (e.g. `USERNAME`, `PASSWORD`,
`NOTES`, or omitted for a custom field), and `value`.

Errors: `401` invalid/missing token; `403` vault not in token's scope; `404` item or vault not
found.

## Create an Item

`POST /v1/vaults/{vaultUUID}/items`

Body: a full item object —
```
{
  "title": "<item title>",
  "category": "LOGIN | PASSWORD | API_CREDENTIAL | SECURE_NOTE | ...",
  "vault": { "id": "<vaultUUID>" },
  "fields": [
    {
      "label": "<field label>",
      "type": "STRING | CONCEALED | ...",
      "purpose": "PASSWORD",
      "value": "<literal value>"
    }
  ],
  "tags": ["..."],
  "urls": [{ "href": "..." }]
}
```
A field may instead carry `"generate": true` plus a `recipe` object (`length`, `characterSets`,
`excludeCharacters`) to have 1Password generate the value server-side instead of accepting a
caller-supplied literal.

Response (200): the created item object, including 1Password-assigned `id` values for the item and
each field.

Errors: `400` invalid item category or malformed input; `401`; `403` vault not in scope.

## Update an Item — Full Replace

`PUT /v1/vaults/{vaultUUID}/items/{itemUUID}`

Body: a complete item object as in Create — this replaces the entire item, so fields not included
are dropped.

Response (200): the updated item object.

## Update an Item — Partial (RFC 6902 JSON Patch)

`PATCH /v1/vaults/{vaultUUID}/items/{itemUUID}`

Body: an array of patch operations, e.g.
```
[
  { "op": "replace", "path": "/fields/<fieldID>/value", "value": "<new value>" }
]
```
Supported ops: `add`, `remove`, `replace`, targeting field-level (and other item-level) JSON
pointers.

Response (200): the updated item object.

## Delete an Item

`DELETE /v1/vaults/{vaultUUID}/items/{itemUUID}`

Response (204): no body — deletion is permanent per 1Password's own documentation.

Errors: `401`; `403` vault not in scope; `404` item not found.
