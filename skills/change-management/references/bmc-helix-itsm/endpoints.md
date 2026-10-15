# Endpoint Wiring — BMC Helix ITSM Change Request Lifecycle (Simplified REST API)

Literal API calls behind each capability named in `procedure.md`. Base URL:
`https://<Innovation Suite server URL>`. Auth: OAuth 2.0 token-based, obtained via a login request
(below); the resulting JWT/cookie is used on subsequent calls.

## Login (obtain authentication token)

Tool hint: `POST /api/rx/authentication/loginrequest`.

```
POST <Innovation Suite server URL>/api/rx/authentication/loginrequest
Host: localhost
Accept: application/json
X-Requested-By: XMLHttpRequest
Content-Type: application/json;charset=UTF-8

{
  "userName": "user",
  "password": "userpassword",
  "locale": "en-us"
}
```
`locale` is optional. Response body is an encoded JWT (opaque string); the call also returns a cookie
used by some client flows for subsequent requests. The token acts as a temporary password with a
configurable idle/absolute expiry — protect it as securely as a real password; if leaked, delete the
associated user account to prevent unauthorized access (per BMC's own documented recommendation).

## Search Change Requests

Tool hint: `POST /api/com.bmc.dsm.itsm.itsm-rest-api/v2/change/search?filter=<FilterName>&optimize=Y`.

Headers: `Accept: application/json`, `Content-Type: application/json`.

Body fields: `limit` (page size), `offset` (pagination offset), `sortBy` (array of
`{"field": "<name>", "order": "asc"|"desc"}`), `fields` (array of field names to return, as a string
in one documented example — confirm exact array-vs-string-encoding against the target instance's API
version), `criteria.bindingExpression` (`"AND"`/`"OR"`), `criteria.conditions` (array of
`{"fieldName": ..., "operation": ..., "fieldValue": ...}` — the source's own two worked examples
render `conditions` inconsistently, once as an array and once as an escaped JSON string; verify the
exact expected encoding against the target instance before relying on either form verbatim).

Example (verbatim, from BMC docs):
```
curl -X 'POST' \
'https://<Innovation Suite server URL>/api/com.bmc.dsm.itsm.itsm-rest-api/v2/change/search?filter=My Group Need Attention Tickets&optimize=Y \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
"limit": 10,
"offset": 10,
"sortBy": [{ "field" : "priority", "order": "desc"}],
"fields": "['\''id'\'','\''status'\'']",
"criteria": {
"bindingExpression": "AND",
"conditions": "{\r\n              \"fieldName\": \"status\",\r\n              \"operation\": \"eq\",\r\n              \"fieldValue\": \"27000\"\r\n          },\r\n          {\r\n              \"fieldName\": \"assignee\",\r\n              \"operation\": \"eq\",\r\n              \"fieldValue\": \"Allen Allbrook\"\r\n          }"
}
}'
```

Second worked example (verbatim, `conditions` as a proper array this time):
```json
{
  "limit": 2,
  "offset": 0,
  "criteria": {
    "bindingExpression": "AND",
    "conditions": [
      {"fieldName": "status", "operation": "neq", "fieldValue": "10"},
      {"fieldName": "status", "operation": "neq", "fieldValue": "11"},
      {"fieldName": "status", "operation": "neq", "fieldValue": "12"},
      {"fieldName": "status", "operation": "neq", "fieldValue": "13"}
    ]
  }
}
```
(`neq` = not-equal, `eq` = equal — the two documented operations shown; other comparison operations
may exist but weren't confirmed in this extraction.)

## Retrieve a Change Request by ID

Tool hint: `GET /api/com.bmc.dsm.itsm.itsm-rest-api/v2/change/{changeRequestId}`.

Example: `GET .../v2/change/CRQ000000000501`.

## Update a Change Request

Tool hint: `PATCH /api/com.bmc.dsm.itsm.itsm-rest-api/v2/change/{changeRequestId}`.

Headers: `Accept: application/json`, `Content-Type: application/json`.

Body: any subset of writable fields — only included fields are changed. Example (verbatim, reassigning
coordinator/group):
```json
{
  "coordinator": {"loginId": "PetramcoCMManager"},
  "coordinatorGroupId": "SGP000000000213",
  "coordinatorGroup": "Petramco Support Group1",
  "coordinatorGroupOrganization": "Petramco Support Org1",
  "coordinatorGroupCompany": "Petramco"
}
```

## Postman client header note (applies to all calls above)

When exercising these endpoints from a Postman-style client, BMC's documented example includes an
`X-Requested-By: XMLHttpRequest` header on requests in addition to `Content-Type: application/json` —
carry both headers, not just `Content-Type`, if a call fails with an unexpected auth/CSRF-shaped
error.
