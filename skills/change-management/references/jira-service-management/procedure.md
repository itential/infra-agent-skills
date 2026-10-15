# Jira Service Management — Change Request Lifecycle Procedure

Create, view status/history, transition, and manage approvals on a Jira Service Management customer
request (used as a change request when the target service desk's request type is configured for
change management) via the JSM Cloud REST API's `servicedeskapi` resource. Assumes an authenticated
REST client (OAuth 2.0 with the relevant `read:servicedesk-request`/`write:servicedesk-request`/
`read:request.approval:jira-service-management` scopes, or equivalent) against the target Jira Cloud
site is already available.

**Key modeling difference from ServiceNow/Freshservice:** JSM has no single dedicated "change" object
type — a change request is a customer request against whichever request type the target service desk
has configured for changes. Confirm the correct `serviceDeskId`/`requestTypeId` pair for change
requests on the target instance before creating anything — there's no universal "the change type" to
assume across different JSM configurations.

See `endpoints.md` for the literal request syntax behind every operation named below.

## Operational procedure

### Common Sequences

**Submit a new change request and drive it to resolution (no approval gate configured on this request
type):**
1. Create a Customer Request — with the change-request-type ID and required field values.
2. Get Customer Transitions — to see what states are currently reachable.
3. Perform a Customer Transition — advance through the workflow using a transition ID from step 2's
   list, not a guessed/hardcoded one.
4. Get Request Status — confirm the final state.

**Submit a change request that requires approval:**
1. Create a Customer Request.
2. Get Approvals — check whether an approval was actually created for this request (not every request
   type has an approval step configured).
3. **Wait for the approver's own decision** — this skill can query approval state but the decision
   itself is restricted to the assigned approver (see Patterns).
4. Once `finalDecision` shows `approved` or `declined`, proceed (transition forward) or stop (report
   DECLINED) accordingly.

**Just check current status/history of an existing request:**
1. Get Request Status — returns the full status history, most recent first, not just the current
   state.

If a caller's ask doesn't match one of these shapes, use the individual capability sections directly
and confirm success at each step before proceeding.

### Create a Customer Request

Create a request against the target service desk and request type, with field values keyed by field
ID (discoverable via a request-type-fields lookup — not detailed further here, see
`endpoints.md`). `raiseOnBehalfOf` and `requestParticipants` are both
permission-gated — neither is available to a caller with customer-only permission; confirm the calling
credential's actual permission level before assuming either field will be accepted.

Confirm success: the response includes the new request's key/ID — use that identifier for every
subsequent call in this procedure.

### Get Request Status

Returns the full status history for the request, in reverse-chronological order (most recent/current
status first) — not just a single current-state field. Use this both to confirm the current state and,
if needed, to see how the request arrived there.

### Get Customer Transitions / Perform a Customer Transition

**Always fetch available transitions before performing one** — there is no fixed, universal set of
transition IDs; they're specific to the target request type's configured workflow. Performing a
transition requires the numeric transition `id` from that list, not a status name or a guessed value.

**Stop and confirm with the operator before performing a transition that closes, cancels, or
otherwise finalizes the request** — there is no documented gate-check or rollback for a customer
transition; once performed, reversal means finding and performing an inverse transition, if the
workflow even has one, not something this API undoes automatically.

An optional comment can accompany a transition (`additionalComment.body`) to record a reason — passing
one requires the Add Comments permission in addition to the Transition Issues permission needed for
the transition itself; if the comment fails due to a permission gap, that's a different failure mode
than the transition itself failing, and should be reported distinctly.

### Get Approvals / Answer Approval

**Not every request type has an approval step — check before assuming one exists.** Get Approvals
returns the approvals actually present on the request; an empty result means there's nothing to wait
on, not an error.

**This skill can observe approval state, but answering an approval is restricted to the specific user
assigned as that approval's approver** — the API's own documented permission model is "User is
assigned to the approval request," with no approve-on-behalf capability. If the calling credential
isn't the assigned approver, Answer Approval will fail with a permission error; that's expected
behavior, not a bug to work around.

Where the calling credential *is* the assigned approver and answering programmatically is genuinely the
intent: submit a decision of `approve` or `decline`. **Once an approval has a `finalDecision`, it
cannot be re-decided** — confirm the current decision state via Get Approvals first if there's any
chance this approval was already answered, rather than attempting a redundant Answer Approval call.

## Patterns

- **Change management here is a configuration choice, not a first-class object type.** Unlike
  ServiceNow's dedicated Change Management API, JSM change requests are just customer requests against
  a specifically-configured request type. This means "does this instance support gate-checking /
  approval / a specific status vocabulary for changes" is entirely dependent on how that instance's
  service desk and request type were set up — confirm rather than assume any of it.
- **Transitions are always discovered, never hardcoded.** The get-transitions-then-perform-by-id
  pattern exists because transition IDs are workflow-specific — the same pattern JSM's own docs use
  everywhere transitions are involved, not something unique to change requests.
- **Approval answering is a one-shot, assignee-only action.** No re-decision, no approve-on-behalf —
  treat an already-decided approval as terminal, and a permission error on Answer Approval as a signal
  the calling credential isn't the assigned approver, not a transient failure to retry.

## Known limitations

- Covers create, status/history, transitions, and approval observation/answering (where the calling
  credential is the assigned approver) — does not cover request-type field discovery (needed to know
  which field IDs a given request type expects), participant/organization management, or SLA/queue
  operations.
- **No universal change-request status vocabulary exists across JSM instances** — the available
  statuses and transitions depend entirely on the target service desk's configured workflow. This
  procedure's steps describe the mechanism (discover-then-transition), not a fixed set of named states
  the way ServiceNow's Change Management API documents.
- **Approve/decline cannot be done on behalf of the assigned approver** — if the calling credential
  isn't that specific user, this is out of scope for this procedure, the same category of restriction
  Freshservice has on its own change-approval API (see that procedure file), though the exact mechanism
  differs (Freshservice disallows API approve/decline entirely; JSM allows it but only for the actual
  assignee).

## Tools

| Operation | Description | Category |
|---|---|---|
| Create Customer Request | Create a new request against a service desk/request type | Change Records |
| Get Request Status | Read the full status history of a request | Change Records |
| Get Customer Transitions | Discover which transitions are currently available on a request | Change Records |
| Perform Customer Transition | Advance a request's workflow state by transition ID | Change Records |
| Get Approvals / Get Approval by ID | Read current approval state on a request | Approval Workflow |
| Answer Approval | Submit approve/decline — assignee-only, one-shot | Approval Workflow |

## Verification checklist

- [ ] The correct `serviceDeskId`/`requestTypeId` pair for change requests was confirmed against the
      target instance, not assumed
- [ ] Get Customer Transitions was called before every Perform Customer Transition — no hardcoded
      transition IDs
- [ ] Get Approvals confirmed whether an approval step actually exists before waiting on one
- [ ] Answer Approval was only attempted by/on behalf of a credential matching the assigned approver,
      and only against an approval without an existing `finalDecision`
- [ ] Final report includes the request key/ID and the current status from Get Request Status, not
      just "the create call succeeded"
