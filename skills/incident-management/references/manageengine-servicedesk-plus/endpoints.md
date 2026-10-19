# Endpoints — ManageEngine ServiceDesk Plus requests (v3 REST API)

Literal wiring layer for `procedure.md`. Operation names in its Tools table map to the calls below.

Written against ManageEngine's v3 REST API reference pages for requests and request notes, retrieved 2026-10-19. The operation list and input field names were also cross-checked against the curated OpenAPI file for this product in the Itential `assets` repository, a secondary source (it covers only list/get/add/edit/delete for requests). Details not on a retrieved page are marked as assumptions or unverified. Values are placeholders.

## Base URL, headers, and authentication

Base URL pattern (on-premises): `{protocol}://{host}:{port}/api/v3`, where the host, port, and any base-path prefix are the instance's own (assumption: the secondary OpenAPI file says the base path is configured per instance). Cloud edition: `<service domain or custom domain>/app/<portal>/api/v3`, as shown on the cloud reference page.

Headers:

- On-premises: `authtoken: <TECHNICIAN_API_KEY>`. The vendor's community guidance and the secondary OpenAPI file show the key as a header; some sources mention a query-parameter form, which was not confirmed.
- Cloud: `Authorization: Zoho-oauthtoken <ACCESS_TOKEN>`. The OAuth scope names for request writes were not retrieved (unverified); consult the vendor's OAuth page.
- `Accept: application/vnd.manageengine.sdp.v3+json`.
- Payloads are sent as a form parameter named `input_data` holding a JSON string, with `Content-Type: application/x-www-form-urlencoded` (community sample; the reference pages describe the `input_data` parameter). Assumption: the same applies to every write below.

## Responses and errors

Success is a response body with a `response_status` block whose `status_code` is `2000` and status `success`. Other status codes, error messages, HTTP-level error behavior, and rate limits were not on the retrieved pages (unverified). Report FAILED with the actual HTTP status and the `response_status` block.

## find_requests

```
GET /requests
```
Documented as a paged list. The list takes an `input_data` parameter with `list_info` (row count, start index, sort field and order, optional `search_criteria`, get-total-count switch). A list-view-filter listing exists at `GET /list_view_filters/show_all`. Assumption: restricting to the Incident type uses a `search_criteria` entry on the request type field; the exact field and condition names were not on the retrieved pages. Success: HTTP 200 with `status_code` 2000.

## read_request

```
GET /requests/{request_id}
```
Response `request` object includes subject, request type, status, priority, impact, urgency, group, technician, requester, category fields, and read-only timestamps. A summary variant exists at `GET /requests/{request_id}/summary`. Success: HTTP 200.

## create_request

```
POST /requests
```
`input_data` shape (field names from the reference and the OpenAPI copy; the `request_type` and `requester` object shapes are assumed from sibling examples):

```
{ "request": { "subject": "<text>", "description": "<text>",
  "request_type": {"name": "Incident"},
  "requester": {"name": "<name>"},
  "impact": {"name": "<name>"}, "urgency": {"name": "<name>"},
  "priority": {"name": "<name>"}, "category": {"name": "<name>"},
  "group": {"name": "<name>"}, "technician": {"name": "<name>"} } }
```
Only `subject` is documented as mandatory by the product; the instance may require more. Success: `status_code` 2000 with the created `request` including its `id`.

## edit_request

```
PUT /requests/{request_id}
```
Same `request` object as create, with only the changed fields. Success: `status_code` 2000.

## pickup_request

```
PUT /requests/{request_id}/pickup
```
Documented input: `input_data` of `1`. Success: `status_code` 2000.

## assign_request

```
PUT /requests/{request_id}/assign
```
`input_data`: `{ "request": { "group": {"name": "<group>"}, "technician": {"name": "<technician>"} } }` (the wrapper object is assumed; the page lists `group.name` and `technician.name`). Success: `status_code` 2000.

## create_note

```
POST /requests/{request_id}/notes
```
`input_data`:

```
{ "request_note": { "description": "<text>", "show_to_requester": false,
  "notify_technician": false, "add_to_linked_requests": false,
  "mark_first_response": false } }
```
The response returns the created `request_note` with its id, creator, and creation time. Success: `status_code` 2000.

## list_notes

```
GET /requests/{request_id}/notes
```
Assumption: a paged note list exists at the collection route; the retrieved page described adding a note. Verify against the vendor's request-note reference before relying on it.

## add_resolution

```
POST /requests/{request_id}/resolutions
GET /requests/{request_id}/resolutions
```
Add takes a `resolution` object with content (attachments allowed). The exact field name for the resolution text (assumed `content`) was not confirmed. Success: `status_code` 2000; the GET reads it back.

## close_request

```
PUT /requests/{request_id}/close
```
`input_data`:

```
{ "request": { "closure_info": { "requester_ack_resolution": true,
  "requester_ack_comments": "<text>", "closure_comments": "<text>",
  "closure_code": {"name": "<Configured closure code>"} } } }
```
The closure code name has to match the instance's configured name including capitalization. Success: `status_code` 2000 and a closed status on read-back.

## Not wired

Delete, merge-requests, problem/change/project association, and tag operations exist in the reference but are outside this procedure's scope (see Known limitations in `procedure.md`).
