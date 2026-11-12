# ServiceNow — Incident Lifecycle

Log, update, assign, hold, resolve, close, and reopen an incident record on a ServiceNow instance using
REST access to the `incident` table (the table named in `endpoints.md`).
Covers the incident record only. Problem records, change requests, major-incident handling, and
communication plans are separate records and are out of scope.

Written against ServiceNow's Zurich release documentation for Incident Management and the Zurich Table
API reference, checked 2026-10-14. Where the documentation does not say how the API behaves, this file
says so instead of filling the gap. The instance's own configuration (mandatory fields, state-flow rules,
auto-close settings, assignment rules) is set by its administrators and can differ from the baseline here.

Assumes an authenticated REST client for the instance is available. The documentation describes the
form's Resolve and Close buttons; this file assumes that writing the same state through the table API has
the same effect, and every state change is therefore read back.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Log and route a new incident:** *Create the incident* → *Assign* → *Mark In Progress* → *Confirm the
  outcome*.
- **Work an incident:** *Record notes* → *Place on hold* when blocked → *Mark In Progress* to resume →
  *Link related records* → *Confirm the outcome*.
- **Finish an incident:** *Resolve* (gated) → *Close* (gated, or let auto-close run) → *Confirm the
  outcome*. If the caller disputes the fix while it is Resolved, *Reopen*.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup matched or did not match |
| CREATED, UPDATED, ASSIGNED, IN_PROGRESS, ON_HOLD, RESOLVED, REOPENED, CLOSED | The read-back shows the requested change |
| NOTED | A note was written (the read-back shows it in the journal) |
| LINKED | The related-record field holds the requested record |
| NOT_APPLIED | The call succeeded but the read-back differs from the request. Report the expected and actual values |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error. Include the status and body |

## State model

Only movements the documentation states are listed. Other transitions may exist or be refused by the
instance; the read-back catches a refusal.

| State | Documented behavior |
|---|---|
| New | The starting state for a freshly logged record. Sample stored value `1` |
| In Progress | Work has an owner and has begun. A reopen and a caller reply to an On Hold record both land here |
| On Hold | Waiting on someone else. Needs a hold reason, and Awaiting Caller also needs an additional comment. A record may be held repeatedly |
| Resolved | A fix is offered. The caller is told and may reopen; auto-close timing starts |
| Closed | Final. Cannot be reopened |
| Canceled | For records that turn out to need no work (a duplicate, unneeded, or not an incident). This procedure does not set it |

- A caller reply on an On Hold record blanks the hold reason, returns the record to In Progress, and emails
  the assignee and watchers.
- Hold reasons: Awaiting Caller, Awaiting Change, Awaiting Problem, Awaiting Vendor.
- Stored values: `1` for New comes from the sample record. `6` for Resolved and `7` for Closed come from
  scripts that set the incident state field next to the state field, so reading them as `state` values is
  an inference. Other stored values are not given; see *Choice values*.

## Choice values

State, hold reason, resolution code, impact, and urgency are choice fields: a stored code plus a display
label. Only the stored values listed under *State model* are given in the sources. For any other value, in
this order:

1. Send the label with display-value input enabled (assumption: it applies to choice labels; the reference
   describes it for display values generally). That flag applies to the whole body, so reference fields in
   the same call must then also be display names.
2. Otherwise read the field's choices with read_choices (see `endpoints.md`).
3. Otherwise stop with FAILED. Never guess a code.

## Operations

Each operation names the tool operation it binds to (see Tools and `endpoints.md`).

### Find an incident

Binds to: find_incidents.

- Look an incident up by its number, or by a filter such as active records on a given configuration item.
- Report FOUND with the matches (including each record's identifier, needed by every later call) or
  NOT_FOUND. An empty result is not an error; see `endpoints.md` for how API versions 1 and 2 report it.

### Create the incident

Binds to: create_incident. Role: itil, sn_incident_write, or admin.

- Provide a short description and the caller, plus what is known: category, subcategory, business
  service, configuration item, impact, urgency, assignment group. Caller and company are optional only
  for an incident raised from an alert or from a change request.
- Do not set priority; it is read-only and calculated from impact and urgency by the instance's lookup
  rules (the baseline sample maps high and high to Critical, low and low to Planning; the instance's own
  rules decide).
- Which fields are mandatory is set by the instance. If the platform rejects the request, report FAILED
  with the status and body; do not guess a missing field.
- Success: CREATED, with the generated incident number, state New, and a calculated priority read back.

### Record notes

Binds to: update_incident (additional comments or work notes).

- Additional comments are visible to everyone who can see the incident, the caller included; work notes
  are visible only to the assigned group and the work notes list.
- Use the field that matches the audience.
- Rich content: text wrapped in `[code]` and `[/code]` is rendered as HTML in a journal entry, so a
  work note can carry a table, list, link, or formatting, such as a structured diagnostic result.
  Several `[code]` blocks can appear in one entry; text outside them stays plain. Without the tags,
  HTML is shown as literal text.
  - Rendering requires the instance property `glide.ui.security.allow_codetag` to be true (the
    default); a hardened instance may have it off, in which case the tags and markup show as text.
  - Script elements are escaped even inside `[code]`. Invalid HTML inside a block can display as
    blank on some UI versions, so keep the markup simple and well formed.
  - A posted journal entry cannot be edited, so check the markup before writing it.
  - Assumption: the same `[code]` convention applies to an entry written through the REST API; read
    the entry back to confirm it was stored with the tags intact.
- Assumption: each write adds a journal entry rather than replacing a value.
- Success: NOTED, with the entry present on read-back.

### Update fields

Binds to: update_incident (by record identifier).

- Send only the fields that change. Read the record back: business rules can adjust fields.
- Success: UPDATED when the read-back matches; NOT_APPLIED with expected and actual values otherwise.

### Assign

Binds to: update_incident (assignment group, then assigned to).

- Changing the group clears the assigned-to user, so set the group, read back, then set the user.
- On create, a baseline rule fills the group from the configuration item or service offering when both
  group and assignee are empty, so a pre-filled group is not an error.
- Success: ASSIGNED, with both values read back.

### Mark In Progress

Binds to: update_incident (state). Use for New → In Progress and for resuming from On Hold. Take the
stored value for the state from *Choice values*. Success: IN_PROGRESS after read-back.

### Place on hold

Binds to: update_incident (state, hold reason, additional comments). Expected source state: In Progress (assumption: the sources name no other).

- Set the state to On Hold with one of the four hold reasons. Both are choice fields; see *Choice values*.
- For Awaiting Caller, include a comment (the additional comments field) saying what is needed.
- An incident can go on hold more than once before it is closed.
- Success: ON_HOLD when the read-back shows state On Hold, the reason set, and (for Awaiting Caller) the
  comment present.
- A later caller update moves it back to In Progress by itself. That is expected, not a failure.

### Link related records

Binds to: update_incident (the related change, problem, parent incident, and causing change fields).

- Set the related change request, problem, parent incident, or causing change. The target must exist; this
  procedure does not create changes or problems. Creating or advancing a change is `change-management`.
- Success: LINKED when the field holds the requested record on read-back.

### Resolve

Binds to: update_incident (state, resolution code, resolution notes). Role: itil, list_updater,
sn_incident_write, or admin. Expected source state: In Progress (assumption).

**Stop and confirm with the operator before resolving.** Tell them: the caller is sent a resolution
notification and may reopen, and the auto-close countdown starts. If the operator declines, report DECLINED and make no call.

- Provide both resolution fields, the code and the notes. The code is a choice field with instance-defined
  values; take it from the operator or the instance's choice list, never invent one.
- Whether the platform refuses a resolve without a code or notes is not stated, so supply both.
- Success: RESOLVED when the read-back shows state Resolved. The resolved-by and resolved-at values
  should be present (assumption: set by the platform on the state change; the sources list them as form
  fields); if absent, report them as missing in the evidence.

### Reopen

Binds to: update_incident (state). Source state: Resolved (documented).

- A Closed incident cannot be reopened. The documented route is a new incident, which the platform
  creates when the caller replies to the resolution email asking to reopen. The sources give no manual
  procedure for creating it through the API; ask the operator how to proceed.
- Reopening is open to write-role agents and to the incident's caller or opener.
- Success: REOPENED when the read-back shows In Progress. The reopen count and last-reopened fields
  should reflect it (assumption: filled by an API state write as by the form's Reopen action).

### Close

Binds to: update_incident (state). Role: itil_admin or admin, a higher bar than resolve.
Expected source state: Resolved (documented).

**Stop and confirm with the operator before closing:** a Closed incident cannot be reopened. If the operator declines, report DECLINED and make no call.

- Many instances close resolved incidents automatically after a configured number of days; zero
  disables it. An inactivity monitor can keep resetting the timer unless it is set not to fire while the
  incident is Resolved.
- Success: CLOSED when the read-back shows state Closed.

### Confirm the outcome

Binds to: read_incident (by record identifier; the identifier comes from the create or find response).

After every change, read the record and compare state, hold reason, assignment, and priority with the
request. Report the status named in the operation, or NOT_APPLIED with expected and actual values.

## Patterns

- **Two state fields exist.** The record has a state and an incident state; ServiceNow's guidance is to
  treat the state field as primary because it spans the whole cycle. Write the state field; read both.
- **Priority is derived.** To change priority, change impact or urgency. Responders cannot change the
  lookup rules.
- **Visibility.** Additional comments and resolution notices reach the caller by email; check the content
  is safe to send.
- **Edits after closure.** An administrator can still change a small documented set of fields on a closed
  or canceled incident (related-record links, watchers, and a few descriptive fields).

## Known limitations

- Covers the incident record only; problems, changes, major incidents, communication plans, and SLA
  administration are not covered.
- Cancellation is a documented state, but the sources do not describe how to cancel through the API or
  who may; this procedure does not cancel.
- Stored values other than New, Resolved, and Closed come from *Choice values*.
- **A Closed incident cannot be reopened,** and resolving starts the auto-close countdown.

## Tools

| Operation | Description | Category |
|---|---|---|
| find_incidents | Read incidents by number or filter | Read |
| read_incident | Read one incident by record identifier | Read |
| read_choices | Read a choice field's options from the instance | Read |
| create_incident | Insert a new incident | Write |
| update_incident | Change named fields on an incident, including state and notes | Write |

## Verification checklist

- [ ] A created incident came back with a number, state New, and a calculated priority; priority was not set
- [ ] Work notes held internal content; additional comments held only caller-safe text
- [ ] On hold carried one of the four reasons, plus a comment for Awaiting Caller
- [ ] No stored choice value was used that is not in the sources or read from the instance
- [ ] The operator confirmed before resolving and before closing
- [ ] Resolution code and notes were supplied when resolving
- [ ] Every state change was read back and reported with its status, or as NOT_APPLIED
