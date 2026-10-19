# Endpoint Wiring — iTop CMDB Configuration Item Management

Literal calls behind each capability named in `procedure.md`.

Source: iTop documentation, "REST/JSON services" (itophub.io wiki, `latest` branch), retrieved
2026-10-19.

Base URL: `https://<itop-root>/webservices/rest.php`. Every operation is a single endpoint; the
operation is named inside the JSON document, not in the path.

Request shape: POST (preferred) or GET, with form parameters:
- `version` — API version, required. The documentation's examples use `1.3`. (Assumption: other
  values are valid only if the instance supports them; an unsupported value returns code 10.)
- `json_data` — the operation document, as JSON text.
- `auth_user` + `auth_pwd`, or `auth_token` (application or personal token). HTTP Basic is also
  supported. Using GET in a browser requires `url` in the instance's `allowed_login_types`
  configuration. Prefer HTTPS and POST.
- `callback` — optional, for JSONP.

Required account rights: the REST Services User profile, plus write and bulk-write permission on each
class modified.

## Read CIs

`json_data`: `{"operation": "core/get", "class": "<Class>", "key": <id | "OQL SELECT" | {criteria}>,
"output_fields": "<a,b | * | *+>", "limit": <n>, "page": <n>}`

Response: `{"objects": {"<Class>::<id>": {"code": 0, "class": "...", "key": <id>, "fields": {...}}},
"code": 0, "message": "Found: <n>"}`. No match gives `"objects": null`. One class per call.

## Create a CI

`json_data`: `{"operation": "core/create", "class": "<Class>", "fields": {...},
"output_fields": "...", "comment": "..."}`

Field value formats: scalar as-is; external key as id, OQL or criteria; blob as
`{"data": "<base64>", "filename": "...", "mimetype": "..."}`; case log as a string,
`{"add_item": {"message": "..."}}` (optional `user_login`, `date`, `format`), or `{"items": [...]}`
which replaces the whole log; link set as an array of relationship objects.

Response: the created object with its key and the requested fields.

## Update a CI

`json_data`: `{"operation": "core/update", "class": "<Class>", "key": <id | OQL | {criteria}>,
"fields": {...}, "output_fields": "...", "comment": "..."}`

The key must match exactly one object. Error text for a multi-match: "Several items found (xx) for
query…".

## Delete a CI

`json_data`: `{"operation": "core/delete", "class": "<Class>", "key": <id | OQL | {criteria}>,
"simulate": true | false, "comment": "..."}`

Response lists every deleted or modified object with a status code and message. Status codes:
0 OK, 1 ISSUE, 2 AUTO_DELETE, 3 AUTO_DELETE_ISSUE, 4 REQUEST_EXPLICITELY, 5 AUTO_UPDATE,
6 AUTO_UPDATE_ISSUE.

## Read related CIs

`json_data`: `{"operation": "core/get_related", "class": "<Class>", "key": <id | OQL>,
"relation": "impacts" | "depends on", "direction": "up" | "down", "depth": <n>,
"redundancy": true | false}`

Response: `{"objects": {...}, "relations": {"<origin-class>::<origin-key>": [{"key":
"<destination-class>::<destination-key>"}]}, "code": 0, "message": "Scope: <n>; Found: <Class>=<n>,
..."}`. Depth defaults to 20. (The source also says the search depth is limited to 4 iterations; it does not
reconcile the two figures, so treat the effective limit as unknown and check the response scope.)

## Top-level error codes

| Code | Name | Meaning |
|---|---|---|
| 0 | OK | Success |
| 1 | UNAUTHORIZED | Missing or wrong credentials, or insufficient rights |
| 2 | MISSING_VERSION | `version` missing |
| 3 | MISSING_JSON | `json_data` missing |
| 4 | INVALID_JSON | Malformed JSON |
| 5 | MISSING_AUTH_USER | `auth_user` missing |
| 6 | MISSING_AUTH_PWD | `auth_pwd` missing |
| 10 | UNSUPPORTED_VERSION | Version not available |
| 11 | UNKNOWN_OPERATION | Operation not valid for the version |
| 12 | UNSAFE | Operation risks data loss |
| 100 | INTERNAL_ERROR | Execution failure |

Unknown (not stated in the source): HTTP status codes accompanying these errors, and rate limits.
