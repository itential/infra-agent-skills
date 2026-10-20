# Jira Service Management — Incident Lifecycle

Create, read, comment on, assign, and move an incident on a Jira Service Management (Cloud) site, using the service desk REST resources for customer requests and, for agent-side assignment, the Jira platform REST API (wiring in `jira-service-management/endpoints.md`).
Covers an incident as one request on an incident-type request type. Problems, changes, alerts, on-call schedules, and status pages are out of scope.

Written against Atlassian's developer pages for the service desk request resources (create, get, comment, transition) and the Jira platform assign-issue operation, plus Atlassian's support documentation on incident workflows, all retrieved 2026-10-19. Several pages loaded only in part, so the gaps are marked **unverified** below. The site's own configuration (request types, workflow, statuses, permissions) is set by its administrators and can differ from what is described here.

Assumes an authenticated REST client for the Cloud site is available (see `endpoints.md` for scopes). Because workflows can change a request on their own (automation, transition screens), every change is read back.

**Neighbouring product, separate file.** Jira Service Management also appears under `change-management`. The change and incident procedures stay separate because the records, request types, and state vocabularies differ; do not reuse that file for incidents.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Raise and work an incident:** *Find the incident request type* → *Create the incident* → *Assign* → *Record a comment* → *Confirm the outcome*.
- **Move through the workflow:** *List available transitions* → *Perform a transition* (gated when it resolves) → *Confirm the outcome*.
- **Reopen:** *List available transitions* → *Perform a transition* (gated) → *Confirm the outcome*.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup matched or did not match |
| CREATED, ASSIGNED, COMMENTED, TRANSITIONED, RESOLVED, REOPENED | The read-back shows the requested change |
| NOT_APPLIED | The call succeeded but the read-back differs from the request. Report the expected and actual values |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error. Include the status and body |

## State model

An incident is a request, and its states are the statuses of the workflow attached to its request type. Atlassian's support documentation describes a default incident workflow whose statuses include open, reopened, pending, work in progress, waiting for customer, waiting for support, escalated, done, and canceled, and says resolved incidents are closed automatically. That list came from search results and the page's own transition detail did not load, so treat it as **unverified**: read the actual statuses and transitions from the site rather than assuming names.

- A status change is a transition chosen by identifier from the list the platform returns for that request; do not guess identifiers.
- Whether a resolved incident can be reopened, and whether resolve and close are separate steps, depends on the site's workflow and is not stated in the retrieved sources. Read the transition list to find out.
- There is no documented hold or acknowledge state in the default list above. Do not map `hold` or `acknowledge` to another status; report that the site's workflow has no such state unless its transition list shows one.

## Operations

Each operation names the tool operation it binds to (see Tools and `endpoints.md`).

### Find the incident request type

Binds to: list_request_types.

- A service desk offers several request types; the incident type's identifier and its required fields are site-specific. Read the service desk's request types and the chosen type's fields before creating anything. Assumption: the incident type is identified by name or by an incident-compatible work type; the sources do not give a fixed identifier.

### Create the incident

Binds to: create_incident.

- Provide the service desk identifier, the incident request type identifier, and values for that type's required fields, keyed by field identifier. Optional: raise on behalf of another user and add participants; both are refused for credentials with customer-only permission.
- Success: CREATED, with the request's key and identifier and its current status read back.
- A 422 means the field values failed validation; report FAILED with the body.

### Find or read an incident

Binds to: read_incident, find_incidents.

- read_incident takes an identifier or key. Hidden fields are omitted from the response.
- find_incidents lists a service desk's queue issues. Queue contents depend on the queue's own saved filter, so a miss may only mean the incident is in another queue.
- Report FOUND with key and status, or NOT_FOUND.

### Record a comment

Binds to: create_comment.

- Send the comment text with a visibility flag. A comment marked not public is internal and is not shown to the customer; a public one is. Check the flag before writing sensitive content.
- Success: COMMENTED, with the comment present when comments are read back (assumption: a comments read exists alongside create).

### Assign

Binds to: assign_issue.

- Set the assignee by account identifier. Setting it to null leaves the issue unassigned; the value `-1` selects the project's default assignee. The call needs assign permission on the project and returns no body.
- This call belongs to the Jira platform API, not the service desk API.
- Success: ASSIGNED when the read-back shows the assignee. **Unverified:** how read-back exposes the assignee through the service desk request resource; if it does not, read the issue through the platform API.

### List available transitions

Binds to: list_transitions.

- Read the transitions available to the caller for this request now; identifiers differ per workflow and per current status.

### Perform a transition

Binds to: perform_transition.

- Choose a transition identifier from the list just read and send it, with an optional comment. Customer-permission credentials may be limited in which transitions they can run; agent-side moves may need the Jira platform transition call instead (**unverified**, its page did not load).
- **Resolving:** stop and confirm with the operator before any transition that moves the incident to a resolved, done, or canceled status. Tell them it declares the service restored and the site's workflow decides whether it can be reopened. If the operator declines, report DECLINED and make no call.
- **Reopening:** stop and confirm with the operator before moving a resolved incident back to an open status, and tell them it re-engages the workflow's notifications and automation. If the operator declines, report DECLINED and make no call.
- Success: TRANSITIONED, or RESOLVED / REOPENED for those moves, when the read-back status matches the target.

### Confirm the outcome

Binds to: read_incident.

After every change, read the request and compare status and assignee with what was requested. Report the status named in the operation, or NOT_APPLIED with expected and actual values.

## Patterns

- **Statuses are workflow-defined.** Names and transitions differ between sites; always read the transition list.
- **Two APIs.** Request creation, comments, and customer transitions use the service desk resources; assignment uses the Jira platform API, which needs its own scope and permission.
- **Rate limiting.** The sources retrieved give no figure for the service desk resources. On HTTP 429, back off and honor any `Retry-After` header; make requests one at a time.

## Known limitations

- Covers one incident request only; problems, changes, alerts, on-call, responders, status pages, and the incident-specific Incidents REST API are not covered.
- Status names, the resolve/close split, reopening, and agent-side transitions are not confirmed (see State model).
- No hold or acknowledge state unless the site's workflow adds one.
- **Resolving can trigger automation and customer notification that this procedure cannot undo.**

## Tools

| Operation | Description | Category |
|---|---|---|
| list_request_types | List a service desk's request types and a type's fields | Read |
| create_incident | Create a request on an incident request type | Write |
| read_incident | Read one request by identifier or key | Read |
| find_incidents | List issues in a service desk queue | Read |
| create_comment | Add a public or internal comment | Write |
| assign_issue | Set, clear, or default the assignee (Jira platform API) | Write |
| list_transitions | List transitions available now | Read |
| perform_transition | Run one transition by identifier | Write |

## Verification checklist

- [ ] The incident request type and its required fields were read before creating
- [ ] A created incident came back with a key and a status
- [ ] Comment visibility was set deliberately
- [ ] Transition identifiers came from the platform's list, not a guess
- [ ] The operator confirmed before resolving and before reopening
- [ ] `hold` and `acknowledge` requests were reported as not available unless the site's transitions offer them
- [ ] A 429 was backed off, not retried immediately
- [ ] Every change was read back and reported with its status, or as NOT_APPLIED
