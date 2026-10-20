# PagerDuty — Incident Lifecycle

Create, find, annotate, acknowledge, reassign, escalate, snooze, merge, resolve, and reopen an incident on a PagerDuty account using its REST API (the REST API v2, wiring in `endpoints.md`).
Covers the incident record only. Services, escalation policies, schedules, on-call overrides, maintenance windows, event ingestion, and responder requests are separate objects and out of scope.

Written against PagerDuty's developer documentation for the incidents REST resources, its REST API rate-limit page, and its incident-lifecycle overview in the product docs, all retrieved 2026-10-19. One detail (reopening through the API) rests on a weaker source and is marked below. Where the documentation does not say how the platform behaves, this file says so instead of filling the gap. The account's own configuration (services, escalation policies, priorities, acknowledgement timeout, permissions) is set by its administrators and can differ from what is described here.

Assumes an authenticated REST client for the account is available and that writes can be attributed to a valid account user (see `endpoints.md`). Because PagerDuty can change an incident on its own (timeouts, snooze expiry), every change is read back.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Raise and take an incident:** *Find an incident* (check for an existing one) → *Create the incident* → *Acknowledge* → *Record a note* → *Confirm the outcome*.
- **Hand off or escalate:** *Reassign* or *Escalate* → *Record a note* → *Confirm the outcome*.
- **Finish an incident:** *Resolve* (gated) → *Confirm the outcome*. If the problem returns, *Reopen* (gated).
- **Collapse duplicates:** *Merge incidents* (gated) → *Confirm the outcome*.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup matched or did not match |
| CREATED, ACKNOWLEDGED, REASSIGNED, ESCALATED, SNOOZED, MERGED, RESOLVED, REOPENED | The read-back shows the requested change |
| NOTED | A note was added (the read-back or note list shows it) |
| UPDATED | Other requested fields (title, urgency, priority) read back as asked |
| NOT_APPLIED | The call succeeded but the read-back differs from the request. Report the expected and actual values |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error. Include the status and body |

## State model

PagerDuty has three incident statuses and no separate closed state; resolved is the end state.

| Status | Documented behavior |
|---|---|
| triggered | The starting status once a service raises the incident. It follows the service's escalation policy and notifies the on-call responders |
| acknowledged | Someone has claimed it, which pauses escalation. If the acknowledgement timeout passes without resolution, the incident goes back to triggered and escalation resumes |
| resolved | Finished. No further notifications are sent. The product documentation says a resolved incident can be reopened |

- A snoozed incident goes back to triggered when the snooze time ends.
- A resolved incident has no assignee, so filtering by assigned user returns only triggered and acknowledged incidents.
- On services with a very large number of open incidents (the documented threshold is 100,000), PagerDuty auto-resolves new incidents after 24 hours.
- There is no hold status and no separate close step. Do not apply `hold` or `close` actions here; report that PagerDuty has no such state.

## Operations

Each operation names the tool operation it binds to (see Tools and `endpoints.md`).

### Find an incident

Binds to: find_incidents, read_incident.

- Look up by identifier or number with read_incident. Otherwise search with find_incidents, filtering by status, deduplication key, service, team, urgency, or time window.
- Searches are paged and limited to a date window (default one month, at most six months unless the window is lifted); a miss may only mean the window was too narrow.
- Report FOUND with each match's identifier and status, or NOT_FOUND. An empty list is not an error.

### Create the incident

Binds to: create_incident.

- Provide a title and the affected service. Optional: urgency, priority, deduplication key, details text, escalation policy, and assignees.
- Writes need the email of a valid account user as the actor (see `endpoints.md`).
- Creating an incident notifies responders through the service's escalation policy. This is the documented effect, not a separate paging step.
- Search by deduplication key first when repeating a request, so a retry does not raise a second incident (assumption: the key matches against existing incidents as it does for events).
- Success: CREATED, with the incident number, status triggered, and the service read back.

### Record a note

Binds to: create_note.

- Add the note text to the incident. A single incident holds at most 2000 notes.
- Assumption: notes are visible to everyone who can view the incident; the sources do not describe a separate internal channel, so keep content appropriate for all viewers.
- Success: NOTED, with the note present when notes are read back.

### Acknowledge

Binds to: update_incident (status).

- Set the status to acknowledged. It claims ownership and pauses escalation until the acknowledgement timeout.
- Success: ACKNOWLEDGED when the read-back shows acknowledged and an acknowledgement entry for the acting user.

### Reassign

Binds to: update_incident (assignments).

- Set the new assignee user(s) on the incident. A resolved incident has no assignee (documented); assumption: assignment applies to open incidents only.
- Success: REASSIGNED when the read-back assignments match.

### Escalate

Binds to: update_incident (escalation level or escalation policy).

- Move the incident to a later level of its escalation policy, or apply a different escalation policy. The level count and policy contents are the account's own; read them rather than guessing a level.
- Success: ESCALATED when the read-back shows the new level or policy.

### Update other fields

Binds to: update_incident (title, urgency, priority).

- Send only the fields that change. Priority takes a priority reference or a priority name; priority names are account-defined, so read them from the account before use.
- Success: UPDATED when the read-back matches.

### Snooze

Binds to: snooze_incident.

- Provide a duration in seconds, from 1 up to 604800 (seven days). When it ends the incident returns to triggered.
- Whether snooze applies to incidents that are not acknowledged is not stated; read the status back.
- Success: SNOOZED when the response and the read-back show the snooze applied.

### Merge incidents

Binds to: merge_incidents. Source incidents: those listed; target: the surviving incident.

**Stop and confirm with the operator before merging.** Tell them: the alerts of every source incident move to the target and the sources are resolved automatically; the documentation gives no way to undo a merge. If the operator declines, report DECLINED and make no call.

- The target must be open. Only incidents that carry alerts, or were created manually in the web interface, can be merged.
- The combined incident may not exceed 1000 alerts; the platform returns an error past that.
- Success: MERGED when the target holds the alerts and each source reads back as resolved.

### Resolve

Binds to: update_incident (status, resolution).

**Stop and confirm with the operator before resolving.** Tell them: no further notifications are sent for it once it is resolved. If the operator declines, report DECLINED and make no call.

- Set the status to resolved and include a resolution text. The resolution text goes into the resolve log entry as a note and is not shown directly in the web interface.
- Success: RESOLVED when the read-back shows resolved. The resolve reason may be empty or null on an incident that was not resolved by this call.

### Reopen

Binds to: update_incident (status). Source status: resolved.

**Stop and confirm with the operator before reopening.** Tell them: responders are notified again according to the escalation policy. If the operator declines, report DECLINED and make no call.

- The product documentation states resolved incidents can be reopened but names no API call. PagerDuty's published API description indicates that setting the status to triggered or acknowledged on a resolved incident reopens it. This was seen only in an OpenAPI description copy and was not found on the retrieved reference page, so treat it as unverified: if the call is refused, report FAILED and ask the operator how to proceed.
- Per that same description, reopening to triggered assigns it using the supplied assignees or escalation policy (else the current policy), and reopening to acknowledged assigns it to the acting user.
- Success: REOPENED when the read-back shows triggered or acknowledged.

### Confirm the outcome

Binds to: read_incident.

After every change, read the incident and compare status, assignments, escalation level, urgency, and priority with the request. Report the status named in the operation, or NOT_APPLIED with expected and actual values.

## Patterns

- **The platform changes incidents by itself.** Acknowledgement timeout returns an incident to triggered; snooze expiry does the same. A read-back that shows triggered after an acknowledge or snooze may mean the timer already ran.
- **Writes need an acting user.** Every incident write is attributed to an account user, so an automation needs a dedicated user whose email it can supply.
- **Rate limiting.** The documented default is 960 requests per minute per key or user. Make requests one at a time per token, back off on HTTP 429, and wait for the number of seconds in the reset header (see `endpoints.md`). Prefer webhooks to polling.

## Known limitations

- Covers the incident record only; services, escalation policies, schedules, overrides, maintenance windows, event ingestion, status updates, and responder requests are not covered.
- No hold and no separate close; resolved is the end state.
- Reopening through the API is unverified (see Reopen).
- Separate-visibility notes, and the effect of snoozing a non-acknowledged incident, are not stated in the sources.
- **A merge cannot be undone by this procedure, and a resolve stops notifications.**

## Tools

| Operation | Description | Category |
|---|---|---|
| find_incidents | List incidents by status, key, service, team, urgency, or window | Read |
| read_incident | Read one incident by identifier or number | Read |
| create_incident | Raise a new incident on a service | Write |
| update_incident | Change status, assignment, escalation, urgency, priority, title, or resolution | Write |
| create_note | Add a note to an incident | Write |
| list_notes | Read an incident's notes | Read |
| snooze_incident | Snooze an incident for a number of seconds | Write |
| merge_incidents | Merge source incidents into a target incident | Write |

## Verification checklist

- [ ] A created incident came back with a number and status triggered, on the intended service
- [ ] Every write carried an acting user's email
- [ ] The operator confirmed before resolving, reopening, and merging
- [ ] A resolve included resolution text
- [ ] `hold` and `close` requests were reported as not available rather than mapped to another state
- [ ] A 429 was backed off using the reset header, not retried immediately
- [ ] Every change was read back and reported with its status, or as NOT_APPLIED
