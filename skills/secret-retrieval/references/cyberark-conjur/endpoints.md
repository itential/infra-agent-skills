# Endpoint Wiring — CyberArk Conjur Secret Retrieval

Literal API calls behind each capability named in `procedure.md`. `{account}` is the Conjur
organization/account name configured for the deployment; `{login}` and `{identifier}` must be
URL-encoded wherever a path segment contains characters like `@`, `/`, `+`, or `&`.

Source: github.com/cyberark/conjur-openapi-spec (CyberArk's canonical Conjur OpenAPI description),
cross-referenced against CyberArk's hosted developer documentation for the same endpoints, retrieved
2026-09-29.

## Get an API Key (Login)

`GET /authn/{account}/login`

Auth: HTTP Basic — `Authorization: Basic base64(<login>:<password>)`.

Response (200, `text/plain`): the identity's API key as a raw string.

Errors: `400`, `401`, `404`, `422`, `500`.

## Authenticate (Exchange API Key for Access Token)

`POST /authn/{account}/{login}/authenticate`

Body (`text/plain`): the raw API key string obtained from Login (50–56 characters).

Optional header: `Accept-Encoding: base64` — returns a pre-base64-encoded token instead of raw
JSON, convenient for directly building the `Authorization` header on subsequent calls.

Response (200, `text/plain` or JSON depending on `Accept-Encoding`): a short-lived access token.

Usage on subsequent calls: `Authorization: Token token=<base64-encoded token>`.

Errors: `400`, `401`, `404`, `422`, `500`.

## Get a Secret

`GET /secrets/{account}/{kind}/{identifier}`

`{kind}` is almost always `variable`. Optional query: `version` — a specific retained version
number (Conjur keeps the most recent 20 by documented default).

Auth: `Authorization: Token token=<access token>` (from Authenticate above).

Response (200, `text/plain`): the raw secret value.

Errors: `400`, `401`, `403` (inadequate privileges), `404`, `422`.

## Get Multiple Secrets (Batch)

`GET /secrets?variable_ids={comma-delimited, URL-encoded fully-qualified ids}`

Example `variable_ids` value: `myorg:variable:secret1,myorg:variable:secret2`.

Optional header: `Accept-Encoding: base64`.

Response (200, JSON): an object mapping each requested fully-qualified id to its value, e.g.
`{"myorg:variable:secret1": "<value1>", "myorg:variable:secret2": "<value2>"}`.

Errors: `400`, `401`, `403`, `404` (one or more resources not found), `406` (encoding issue),
`422`.

## Set a Secret

`POST /secrets/{account}/{kind}/{identifier}`

Auth: `Authorization: Token token=<access token>`.

Body (`text/plain`): the raw new secret value.

The target variable resource must already exist via Conjur policy — this call sets/overwrites its
value, it does not create the resource.

Errors: `400`, `401`, `403`, `404`, `422`.
