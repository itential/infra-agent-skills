# Opsgenie — Incident Lifecycle

Create, find, annotate, add responders to, re-prioritize, resolve, close, reopen, and delete an incident on an Atlassian Opsgenie account using its REST API (wiring in `endpoints.md`).
Covers the incident record only. Alerts, on-call schedules, escalation policies, services, teams, integrations, post-incident reviews, and status pages are separate objects and out of scope.

Written against Atlassian's Opsgenie incident API reference and its API rate-limiting page, both retrieved 2026-10-19. The product's announced end of support comes from a web search summary on the same date; the Atlassian pages themselves were not fetched, so treat it as secondary and confirm it (see Known limitations). Where the documentation does not say how the platform behaves, this file says so instead of filling the gap. The account's own configuration (plan, teams, services, permissions) is set by its administrators and can differ from what is described here.

Assumes an authenticated REST client for the account is available. Because every write is processed asynchronously, each one is followed by a request-status check and a read-back.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Raise and work an incident:** *Find an incident* (check for an existing one) → *Create the incident* → *Check the request* → *Add a responder* (gated) → *Record a note* → *Confirm the outcome*.
- **Finish an incident:** *Resolve* (gated) → *Check the request* → *Close* (gated) → *Check the request* → *Confirm the outcome*. If the problem returns, *Reopen* (gated).
- **Remove a mistaken incident:** *Delete* (gated) → *Check the request* → *Confirm the outcome*.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup matched or did not match |
| ACCEPTED | The platform answered 202 with a request identifier; the change is not yet confirmed |
| CREATED, NOTED, RESPONDER_ADDED, PRIORITY_SET, RESOLVED, CLOSED, REOPENED, DELETED | The request-status check reports success and the read-back shows the requested change |
| UPDATED | Other requested fields (message, description, tags, details) read back as asked |
| NOT_APPLIED | The request reported success but the read-back differs from the ask. Report the expected and actual values |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error, or the request-status check reported failure. Include the status and body |

## State model

The documented examples show the statuses `open` and `closed`. Assumption: a resolved incident reads back with the status `resolved`, because resolve and close are separate operations, but the reference does not list the full set of status values. Read the status back and report exactly what the platform returns.

| Operation | Documented behavior |
|---|---|
| Create | Accepted asynchronously. The new incident is open |
| Resolve | Accepted asynchronously. The documentation gives no required starting state |
| Close | Accepted asynchronously. The documentation gives no required starting state and does not say whether an unresolved incident can be closed |
| Reopen | Accepted asynchronously. The documentation gives no required starting state |
| Delete | Accepted asynchronously. Removes the incident |

- There is no acknowledge operation and no assignee on an incident; ownership is expressed by adding responders (a team or a user). Do not apply `acknowledge`, `assign`, or `hold` actions here; report that Opsgenie's incident API has no such operation.
- Incidents can be addressed by their identifier or by a short numeric `tiny` identifier; state which kind is supplied.
- The incident API is documented for the Standard and Enterprise plans only.

## Operations

Each operation names the tool operation it binds to (see Tools and `endpoints.md`).

### Find an incident

Binds to: find_incidents, read_incident.

- Look up one incident by identifier or tiny identifier with read_incident. Otherwise search with find_incidents using the platform's search query, sort field, and order.
- Results are paged (limit 1 to 100, default 20). A miss may only mean the first page did not reach the match.
- Report FOUND with each match's identifier and status, or NOT_FOUND. An empty list is not an error.

### Create the incident

Binds to: create_incident.

- Provide a message (the title; at most 130 characters). Optional: description, responders, tags, details (custom key/value properties), priority (P1 to P5, default P3), a note, impacted services, status page entry, and a stakeholder-notification flag.
- Adding responders at creation notifies them (assumption: documented only as the purpose of responders). Search first when repeating a request, so a retry does not raise a second incident; the create call has no documented deduplication key.
- The call returns only a request identifier. Continue with *Check the request*.
- Success: CREATED when the request-status check reports success with an incident identifier and the read-back shows the incident open.

### Check the request

Binds to: get_request_status.

- Every write below returns a request identifier. Read the request status with it. Success is the success flag in the response together with an incident identifier; a failure carries a descriptive message (for example that the incident does not exist).
- If the request is not yet processed, wait and read again; the documentation gives no processing time. Apply the rate-limit pattern below.
- Never report a write as done on the 202 alone; report ACCEPTED until the check succeeds.

### Record a note

Binds to: add_note.

- Provide the note text (at most 25000 characters). Notes can also ride along on resolve, close, reopen, add-responder, and tag calls.
- Assumption: notes are visible to everyone who can view the incident; the sources do not describe a separate internal channel.
- Success: NOTED when the request check succeeds and the note appears when notes are listed.

### Add a responder

Binds to: add_responder.

**Stop and confirm with the operator before adding a responder.** Tell them: the named team or user is added to the incident and will be alerted (assumption: the documentation states the responder is added, not how it is notified). If the operator declines, report DECLINED and make no call.

- Provide the responder as a team or a user, by identifier. An optional note can be attached.
- Success: RESPONDER_ADDED when the request check succeeds and the read-back lists the responder.

### Update other fields

Binds to: set_priority, update_message, update_description, add_tags, remove_tags, add_details, remove_details.

- Priority takes P1 to P5. Message is the title. Description may be an empty string. Tags: up to 20, each up to 50 characters. Details are key/value pairs, up to 8000 characters in total; removing details takes up to 10 keys.
- Send only what changes, one call per field group, and check each request.
- Success: UPDATED (or PRIORITY_SET) when the read-back matches.

### Resolve

Binds to: resolve_incident.

**Stop and confirm with the operator before resolving.** Tell them: the incident is declared resolved; the documentation does not state what notifications this stops or whether it can be reversed other than by a reopen. If the operator declines, report DECLINED and make no call.

- Optional note. The documentation gives no required starting state; if the platform refuses, report FAILED with its message.
- Success: RESOLVED when the request check succeeds and the read-back status is the resolved state.

### Close

Binds to: close_incident.

**Stop and confirm with the operator before closing.** Tell them: closing ends the incident record; the documentation does not say whether a closed incident can be reopened, although a reopen operation exists. If the operator declines, report DECLINED and make no call.

- Optional note. Resolve first where the team's process separates them; the documentation does not require it.
- Success: CLOSED when the request check succeeds and the read-back status is closed.

### Reopen

Binds to: reopen_incident.

**Stop and confirm with the operator before reopening.** Tell them: the incident returns to an active state; the documentation does not say who is notified. If the operator declines, report DECLINED and make no call.

- Optional note. The documentation gives no required starting state; if the platform refuses, report FAILED with its message.
- Success: REOPENED when the request check succeeds and the read-back status is open.

### Delete

Binds to: delete_incident.

**Stop and confirm with the operator before deleting.** Tell them: this removes the incident record; the documentation describes no undo. If the operator declines, report DECLINED and make no call.

- Success: DELETED when the request check succeeds and a read of the incident reports it does not exist.

### Confirm the outcome

Binds to: read_incident, list_notes.

After every change, read the incident (and its notes after a note) and compare status, priority, responders, message, tags, and details with the request. Report the status named in the operation, or NOT_APPLIED with expected and actual values.

## Patterns

- **Writes are asynchronous.** A 202 means queued. Poll the request status; a read-back taken too early may show the old state.
- **Rate limiting.** Incident calls have their own limit bucket, separate from alerts and other domains. The limits depend on the plan and user count and are not fixed numbers. The state is reported in response headers (see `endpoints.md`); a throttled request gets HTTP 429, and a request in the burst state is delayed by the platform. Back off exponentially and retry rather than looping.
- **Regional host.** An account on the EU instance must use the EU host or requests fail (see `endpoints.md`).

## Known limitations

- Covers the incident record only; alerts, on-call, escalation policies, services, teams, integrations, post-incident reviews, and status pages are not covered.
- No acknowledge, assign, hold, or escalate operation. Ownership is by responders only.
- The full set of status values, required starting states for resolve/close/reopen, and per-call error strings are not documented on the pages read. Treat any state transition as unverified until read back.
- **Product lifecycle:** a web search summary indicated that Atlassian has announced end of sale and end of support for Opsgenie, with data not moved to Jira Service Management deleted afterwards. The primary notices were not fetched and no dates are stated here because none could be verified. Confirm the schedule with Atlassian before relying on this procedure for new work.
- **A delete cannot be undone by this procedure.**

## Tools

| Operation | Description | Category |
|---|---|---|
| find_incidents | List incidents by search query, sort, and order | Read |
| read_incident | Read one incident by identifier or tiny identifier | Read |
| list_notes | Read an incident's notes | Read |
| get_request_status | Read the outcome of an asynchronous write | Read |
| create_incident | Raise a new incident | Write |
| add_note | Add a note to an incident | Write |
| add_responder | Add a team or user as responder | Write |
| set_priority | Set priority P1 to P5 | Write |
| update_message | Change the title | Write |
| update_description | Change the description | Write |
| add_tags / remove_tags | Add or remove tags | Write |
| add_details / remove_details | Add or remove custom properties | Write |
| resolve_incident | Resolve an incident | Write |
| close_incident | Close an incident | Write |
| reopen_incident | Reopen an incident | Write |
| delete_incident | Delete an incident | Write |

## Verification checklist

- [ ] Every write was followed by a request-status check, not reported on the 202 alone
- [ ] The operator confirmed before adding a responder, resolving, closing, reopening, and deleting
- [ ] `acknowledge`, `assign`, and `hold` requests were reported as not available rather than mapped to another operation
- [ ] The EU host was used for an EU account
- [ ] A 429 was backed off exponentially, not retried immediately
- [ ] Every change was read back and reported with its status, or as NOT_APPLIED
