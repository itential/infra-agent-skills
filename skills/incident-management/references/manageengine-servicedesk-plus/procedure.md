# ManageEngine ServiceDesk Plus — Incident Request Lifecycle

Create, find, update, annotate, take, assign, resolve, and close a request of type Incident on a ServiceDesk Plus instance through its v3 REST API (wiring in `endpoints.md`).
Covers the request record only. Problems, changes, projects, tasks, worklogs, approvals, SLAs, and asset records are separate objects and out of scope, except for the association operations noted under Known limitations.

Written against ManageEngine's v3 REST API request and request-note reference pages (on-premises and cloud editions), retrieved 2026-10-19. The pages describe the operations and their inputs but were only partly retrievable: error codes, rate limits, and several behaviors are not stated in what was read and are marked unverified. The operation list was cross-checked against the curated OpenAPI file for this product in the Itential `assets` repository, a secondary source that is not ManageEngine documentation. Statuses, closure codes, categories, priorities, mandatory fields, and technician permissions are configured by the instance's administrators and can differ from what is described here.

Assumes an authenticated REST client for the instance is available (see `endpoints.md`). Because the platform can reject or alter a write according to its own configuration, every change is read back.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Raise and take an incident:** *Find an incident* (check for an existing one) → *Create the incident* → *Pick up* or *Assign* → *Record a note* → *Confirm the outcome*.
- **Hand off:** *Assign* → *Record a note* → *Confirm the outcome*.
- **Finish an incident:** *Add the resolution* → *Close* (gated) → *Confirm the outcome*.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup matched or did not match |
| CREATED, UPDATED, PICKED_UP, ASSIGNED, RESOLUTION_ADDED, CLOSED | The read-back shows the requested change |
| NOTED | A note was added (the read-back or note list shows it) |
| NOT_APPLIED | The call succeeded but the read-back differs from the request. Report the expected and actual values |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error. Include the HTTP status and the response status block |

## State model

Request statuses are defined by each instance's administrators; the documentation names Open, In Progress, and Closed as examples and describes the transitions as configurable. This file therefore does not assume a fixed list.

- Closing is a distinct operation that takes closure details (see Close), separate from editing the status field.
- Whether the instance has a separate resolved status, whether it can be reopened through the API, and which transitions are allowed are not stated in the sources read. Read the instance's configured statuses rather than guessing a status name.
- There is no hold or acknowledge operation documented for this API. Do not map `hold` or `acknowledge` requests to another state; report that the platform procedure has no such step. Picking a request up (below) is the documented way for a technician to claim it.

## Operations

Each operation names the tool operation it binds to (see Tools and `endpoints.md`).

### Find an incident

Binds to: find_requests, read_request.

- Read one request by its identifier with read_request. Otherwise page through find_requests, using a list view filter or search criteria so the result is limited to requests of type Incident.
- Assumption: the way to restrict a search to the Incident request type (a search criterion on the type field) was not shown on the pages read; check the vendor's list-request reference for the criteria syntax before relying on it.
- Report FOUND with each match's identifier, subject, and status, or NOT_FOUND. An empty list is not an error.

### Create the incident

Binds to: create_request.

- Provide a subject (the only field the documentation marks mandatory) and set the request type to Incident. Optional documented attributes include requester, description, priority, impact, urgency, category tree, group, and technician. The instance may make more fields mandatory.
- Run *Find an incident* first when repeating a request. The sources describe no deduplication key or idempotency support, so a retry can create a second record.
- Priority, impact, urgency, and categories are instance-defined names; read the valid values rather than inventing them. Where the instance derives priority from impact and urgency, set the inputs rather than the result (assumption: this applies only if the instance is configured that way).
- Success: CREATED, with the new request's identifier, subject, and request type Incident read back.

### Update other fields

Binds to: edit_request.

- Send only the fields that change, for example subject, description, priority, group, or category.
- Success: UPDATED when the read-back matches. A field the instance rejects or rewrites is NOT_APPLIED.

### Pick up

Binds to: pickup_request.

- Assigns the request to the technician who owns the credential making the call. The documented input is the single value 1.
- Success: PICKED_UP when the read-back shows that technician as the owner.

### Assign

Binds to: assign_request.

- Name the group, the technician, or both. The documented inputs are names.
- Assumption: the named group and technician must exist and be permitted for this request; the sources do not state the failure response.
- Success: ASSIGNED when the read-back group and technician match.

### Record a note

Binds to: create_note.

- Add the note text. Optional documented switches: show the note to the requester, notify the technician, copy it to linked requests, and mark it as the first response.
- Show-to-requester is a boolean; the sources read do not state its default. Set it explicitly to false for internal content and to true only when the requester should see it.
- Success: NOTED, with the note present when the request's notes are read back.

### Add the resolution

Binds to: add_resolution.

- Add resolution text to the request. Attachments are allowed. The documentation describes a resolution as required when the instance's closure rules demand it; the exact rule is the instance's own.
- Success: RESOLUTION_ADDED when the resolution reads back.

### Close

Binds to: close_request.

**Stop and confirm with the operator before closing.** Tell them: the request moves to its closed state, and the documentation describes no API call to reopen it. If the operator declines, report DECLINED and make no call.

- Provide the closure details: a closure code (given by name; the capitalization has to match the instance's configured name, for example "Success" rather than "success"), closure comments, and whether the requester acknowledged the resolution, with optional acknowledgement comments.
- Mandatory fields such as the resolution can block a close. The vendor's community guidance says to fill them with an update to the request, then close; treat that as secondary guidance.
- Success: CLOSED when the read-back shows a closed status. Reopening is not documented; if the operator asks for it, report that it is not covered.

### Confirm the outcome

Binds to: read_request.

After every change, read the request and compare status, type, group, technician, priority, and category with what was requested. Report the status named in the operation, or NOT_APPLIED with expected and actual values.

## Patterns

- **Names, not identifiers, in several inputs.** Group, technician, closure code, and priority are passed by name in the documented examples; an exact-match mismatch (including capitalization) is the likeliest cause of a rejected write.
- **Mandatory fields are instance-specific.** The same call can succeed on one instance and fail on another because an administrator made another field mandatory or tied closing to a resolution.
- **Input is a JSON document in a single form parameter.** Writes carry their payload as a JSON string named input_data, not as a raw JSON body (see `endpoints.md`).
- **Success is reported in the response body.** The documented success code is 2000 in the response's status block; check it as well as the HTTP status.
- **Rate limits.** The sources read state none. Treat limits as unknown: send requests one at a time, and on an HTTP 429 or any throttling response back off and honor a Retry-After header if present.

## Known limitations

- Covers the incident request record only. Problems, changes, projects, tasks, worklogs, approvals, and assets are not covered; the platform offers operations to associate an incident with a problem or change, which this file does not describe.
- No documented hold, acknowledge, or reopen operation; closing is described as final.
- Deleting a request is not covered: the retrieved reference was cut off before describing whether deletion is permanent or moves to a trash.
- Error codes beyond the success code, and error response strings, were not retrievable and are not listed.
- Paging an on-call responder, major-incident handling, and SLA behavior are not covered.
- **Closing cannot be undone by this procedure.**

## Tools

| Operation | Description | Category |
|---|---|---|
| find_requests | List requests with a filter or search criteria | Read |
| read_request | Read one request by identifier | Read |
| create_request | Raise a new request of type Incident | Write |
| edit_request | Change fields on a request | Write |
| pickup_request | Assign the request to the calling technician | Write |
| assign_request | Assign the request to a group and/or technician | Write |
| create_note | Add a note to a request | Write |
| list_notes | Read a request's notes | Read |
| add_resolution | Add resolution text to a request | Write |
| close_request | Close a request with closure details | Write |

## Verification checklist

- [ ] A created request came back with an identifier and request type Incident
- [ ] Group, technician, closure code, and priority were exact-match names for the instance
- [ ] Payloads were sent as the input_data form parameter and the response status block was checked
- [ ] The operator confirmed before closing
- [ ] `hold`, `acknowledge`, and reopen requests were reported as not available rather than mapped to another state
- [ ] Note visibility to the requester was set explicitly
- [ ] Every change was read back and reported with its status, or as NOT_APPLIED
