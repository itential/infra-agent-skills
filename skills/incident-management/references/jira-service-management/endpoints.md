# Endpoints — Jira Service Management incidents (Cloud REST)

Literal wiring layer for `procedure.md`. Operation names in its Tools table map to the calls below.

Written against Atlassian's developer pages for the service desk request resources and the Jira platform assign-issue operation, retrieved 2026-10-19. Details not on a retrieved page are marked as assumptions or as taken from a copy of the OpenAPI definition in the community assets repository (a secondary source, not Atlassian's own page). Values are placeholders.

## Base URL, headers, and authentication

Base URL: `https://<your-domain>.atlassian.net` (assumption: taken from the placeholder host in the secondary OpenAPI copy; Cloud sites use their own domain, and an OAuth 2.0 (3LO) gateway host is a documented alternative that was not checked).

- Authentication: OAuth 2.0 or Basic with an API token. Documented classic scopes: `write:servicedesk-request` (create, comment, transition) and `read:servicedesk-request` (reads). Documented granular scopes for create: `read:request:jira-service-management`, `write:request:jira-service-management`, `read:user:jira`; for comment: `write:comment:jira-service-management`, `read:user:jira`. Scopes for the platform assign call were not read (unverified).
- `Content-Type: application/json` on calls with a body.
- The service desk resources may require an experimental-API opt-in header on some operations (unverified, not seen on retrieved pages; if a call is refused, check the vendor reference before retrying).

## Rate limits and errors

No figures were found on the retrieved pages. On HTTP 429 back off and honor any `Retry-After` header. Documented statuses on the request calls: 400 (bad payload), 401 (not authenticated), 403 (no permission), 404 (request not found, on get and comment), 422 (validation failure, on create), 500. Error body strings were not read; report FAILED with the actual status and body.

## list_request_types

```
GET /rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype
GET /rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/field
```
Read the request types and the chosen type's fields. Listed in the secondary OpenAPI copy; the official page for these was not retrieved (unverified).

## create_incident

```
POST /rest/servicedeskapi/request
```
```json
{
  "serviceDeskId": "<service desk id>",
  "requestTypeId": "<incident request type id>",
  "requestFieldValues": { "summary": "<summary>", "description": "<details>" },
  "raiseOnBehalfOf": "<account id, optional>",
  "requestParticipants": ["<account id>"]
}
```
`raiseOnBehalfOf` and `requestParticipants` are refused for customer-only credentials. Success: 201 with `issueId`, `issueKey`, `summary`, `requestTypeId`, `serviceDeskId`, `createdDate`, `reporter`, `requestFieldValues`, `currentStatus` (`status`, `statusCategory`, `statusDate`), and `_links`.

## read_incident

```
GET /rest/servicedeskapi/request/{issueIdOrKey}
```
Same shape as the create response; hidden fields are omitted. Success: 200.

## find_incidents

```
GET /rest/servicedeskapi/servicedesk/{serviceDeskId}/queue/{queueId}/issue
```
Lists issues in a queue. Listed in the secondary OpenAPI copy only (unverified).

## create_comment

```
POST /rest/servicedeskapi/request/{issueIdOrKey}/comment
```
```json
{ "body": "<comment text>", "public": false }
```
`public: false` makes an internal comment hidden from the customer. Field names are assumed from the operation's documented pattern; the schema section did not load (unverified). Success: 201.

## assign_issue

```
PUT /rest/api/3/issue/{issueIdOrKey}/assignee
```
```json
{ "accountId": "<account id>" }
```
`accountId` of null unassigns; `-1` selects the project's default assignee. Needs the assign-issue permission on the project. Success: 204 with no body. This is the Jira platform API, not the service desk API.

## list_transitions

```
GET /rest/servicedeskapi/request/{issueIdOrKey}/transition
```
Returns the transitions available to the caller. Success: 200. Response field names were not read; take the identifier field from the actual response.

## perform_transition

```
POST /rest/servicedeskapi/request/{issueIdOrKey}/transition
```
Body: the chosen transition identifier and an optional comment (assumed field names `id` and `additionalComment`, from the secondary OpenAPI copy; the official body schema did not load, so unverified). Success is expected as a no-content or 2xx response; confirm by reading the request back. For agent-side transitions the Jira platform transitions operation (`POST /rest/api/3/issue/{issueIdOrKey}/transitions`) is the alternative; its page did not load (unverified).
