# Freshservice — Change Management Lifecycle Procedure

Create, update, move, delete, and manage approvals on a Freshservice change request via the Freshservice
API v2 Changes resource (`/api/v2/changes`). Covers create, read, update, move (workspace transfer),
delete, notes, and the full approvals/approval-group/approval-chain surface — does not cover Change
Tasks or Time Entries (documented as related modules but not extracted into this procedure; see Known
limitations). Assumes an authenticated API client for Freshservice (HTTP Basic with an API key, or
OAuth 2.0 with the relevant `freshservice.changes.*` scopes) is already available to the calling agent.

**Critical scope boundary up front: this API cannot approve or reject a change.** The only
programmatic approval-status transition available is cancelling a pending approval. Approving or
rejecting is only possible via the approver's own action in the Freshservice product (UI or approval
email) — see Patterns and Known limitations.

## Operational procedure

### Common Sequences

**Submit a new change and drive it through to close (no approval required by this change's type/model):**
1. Create — with the given fields, explicitly setting `status`, `priority`, `impact`, `risk`, and
   `change_type` (the source does not document defaults for these on create).
2. Update — advance `status` through its lifecycle (Open → Planning → ... → Closed) as work progresses,
   confirming via View after each transition.
3. View — confirm final `status` reached Closed (6).

**Submit a change that requires approval:**
1. Create — with the given fields.
2. Create an Approval Group — with the approver list and approval type (Everyone/Anyone/Majority/First
   Responder). Optionally set an approval chain rule first if multiple approval groups must run in a
   specific order/level.
3. **Wait for the approvers' own action** — this skill/API cannot approve or reject on their behalf.
   Poll List all Change Approvals or View a Change Approval to observe `approval_status` changing to
   `approved` (1) or `rejected` (2) via the approver's own action in the product.
4. If rejected: report REJECTED — do not proceed to advance `status` toward release/close.
5. If approved: Update the change's `status` to advance it (e.g. toward Pending Release), then Close
   once the change is implemented.

**Withdraw a pending approval request (not the same as approve/reject):**
1. Cancel a Change Approval (single approver) or Cancel Approval Group (whole group) — sets
   `approval_status` to `cancelled` (3). Use this when the change itself is being withdrawn or
   re-scoped, not as a way to reject on the approver's behalf.

**Just update fields on an existing change (no state transition):**
1. Update — directly against the known change. `workspace_id` cannot be changed this way — use Move
   if the change needs to change workspace.

If a caller's ask doesn't match one of these shapes, use the individual capability sections directly and
still confirm success at each step before proceeding to the next — never chain calls without checking
the prior one actually returned a usable record.

### Create

Create a change with the given fields. `requester_id` is mandatory. Explicitly set `status`, `priority`,
`impact`, `risk`, and `change_type` from the enums in `endpoints.md` — the source doesn't document a
default for these on create (only `approval_status` is observed defaulting to `4` in example responses,
and that default's meaning isn't confirmed against the named approval-status enum — treat it as
platform-internal, not something to rely on semantically).

If associating a maintenance window, pass only `{"id": <maintenance_window_id>}` — other maintenance
window properties (dates, description) are not settable through this API; use the web UI for those.

Confirm success: the response `change` object includes `id`, and every field set in the request is
echoed back with the value submitted.

### View / View List

View a single change by ID, optionally with `?include=stats` to get lifecycle timestamps
(`closed_at`, `planning_at`, `assigned_at`, `approval_at`, `pending_release_at`, `pending_review_at`) —
each `include` costs an additional API credit, so only request it when those timestamps are actually
needed.

For a list, use `query` (field-based filter, cannot combine with `view`) or `view` (a saved Change
Management view). See `endpoints.md` for the exact query syntax and operators. Default list excludes
deleted/spam changes.

### Update

Update the given fields on the change record — this is how `status` transitions happen; there's no
separate "transition" endpoint, `status` is just a field like any other on a `PUT`. `workspace_id`
cannot be updated this way (see Move).

**Confirm before a status change that closes or releases a change, or before any update to a
change already in or past Approval status** — this affects a change record other systems/approvers may
be actively acting on. State the change ID, current status, and the target status before proceeding.

### Move (workspace transfer)

Transfers a change to a different workspace, optionally reassigning `group_id`/`owner_id` in the same
call. Applicable only to accounts using workspaces. This is the only way to change `workspace_id` after
creation — Update explicitly cannot do this.

### Delete

Deletes the change. The source documents this as a **soft delete** ("Deleted changes are not
permanently lost... retrieve them using the Restore Change API") but does not include the Restore
endpoint's exact path in the extracted material — confirm its existence and path against the live API
reference or the target tenant before promising restore is possible through this skill. **Stop and
confirm with the operator before deleting** — even though it's documented as recoverable, restore
capability wasn't independently verified here.

### Manage Approvals

- **List/View approvals** — read-only, to check current approval state before deciding next steps.
- **Create an Approval Group** — define who must approve and how (`approval_type`: Everyone/Anyone/
  Majority/First Responder) and the approver list. Optional `email_content` overrides the default
  notification.
- **Update an Approval Group** — change its approver list/type/notification content.
- **Update the approval chain rule** — sets multi-level approval ordering (`rule`) when more than one
  approval group must run in sequence rather than in parallel.
- **Send a reminder** — re-notifies the approver(s) on a specific pending approval; does not change
  status.
- **Cancel a Change Approval / Cancel an Approval Group** — the only status change this API can make:
  sets `approval_status` to `cancelled` (3). **This is not a rejection** — don't use it as a substitute
  for a REJECTED outcome; report it as CANCELLED and note that the approver never acted, rather than
  implying they declined.

**There is no create/approve/reject-by-API call.** If the caller's request is "approve this change" or
"reject this change" via automation, **stop and report this is out of scope for this API** — it can only
be done by the approver's own action in the Freshservice product. This skill can create the approval
request, cancel it, remind the approver, and observe the resulting status — nothing more.

### Add a Note

Create a note (`body`, HTML) on the change, optionally with `notify_emails` to alert specific addresses.
Use for audit-trail/communication purposes — notes don't affect `status` or `approval_status`.

## Patterns

- **`status` is just a field, not a guarded state machine from the API's perspective.** Unlike
  ServiceNow's Change Management API (which exposes an explicit gate-check for available next states),
  Freshservice's Changes API lets `status` be set directly via Update with no documented transition-
  validation endpoint. The calling agent is responsible for only moving `status` forward in a sequence
  that makes operational sense (Open → Planning → Approval → Pending Release → Pending Review → Closed)
  — the API itself won't stop an out-of-order or backward transition the way a gated system would. Treat
  every status-changing Update as needing the same care a gate-check would otherwise provide.
- **Approval is observed, not driven, by this API.** The only approval-status write this API supports
  is cancellation — approve/reject is exclusively the approver's own action. Any workflow built on this
  skill that needs to "wait for approval" must poll List/View Change Approvals rather than expect a
  synchronous approve call to ever succeed.
- **Numeric enums may not be complete for every tenant.** Freshservice allows custom fields and
  potentially custom values per account — use the List Change Fields capability to confirm the live
  enum before assuming the documented Status/Priority/Impact/Risk/Change-Type values in `endpoints.md`
  are exhaustive for the target tenant.
- **Maintenance window association is ID-only through this API.** Attempting to also set the window's
  dates/description via the Changes API silently has no effect on those fields — set them via the web UI
  if they need to be initialized, then only ever reference the window by `id` here.

## Known limitations

- Covers create, view/view list, update, move, delete, notes, and the full approvals surface (approval,
  approval group, approval chain rule) — does not cover Change Tasks or Time Entries, which the source
  references as related modules but weren't extracted into this procedure.
- **Cannot approve or reject a change via this API** — only cancel a pending approval/approval group.
  Approve/reject requires the approver's own action in the Freshservice product. Any request to
  automate approval/rejection itself is out of scope for this skill.
- **Delete is documented as recoverable via a "Restore Change" API**, but that endpoint's exact path
  wasn't found in the extracted source material — do not promise restore capability without confirming
  it against the live API reference or the target tenant first.
- A few source-documented details carry internal inconsistencies flagged in `endpoints.md` (the
  `View a Change Approval` endpoint's OAuth scope is listed as a Tickets scope; the approval-chain-rule
  endpoint's sample cURL uses `POST` against a documented `PUT` method) — verify both against the live
  tenant/API reference before depending on either exactly as documented.
- No documented auto-abort-timer or built-in rollback mechanism exists for a change moving through
  status transitions — unlike a network-device install-mode upgrade, there's no platform-enforced safety
  net here; any confirmation gating is this skill's own discipline, not something Freshservice enforces.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create Change | Create a new change record | Change Records |
| View / View List Changes | Read a single change or a filtered/sorted list | Change Records |
| Update Change | Update fields (including `status`) on an existing change | Change Records |
| Move Change | Transfer a change to a different workspace (only way to change `workspace_id`) | Change Records |
| Delete Change | Soft-delete a change | Change Records |
| Create/Update/Cancel Approval Group | Define or modify who must approve a change and how | Approval Workflow |
| List/View Change Approvals | Read current approval status per approver | Approval Workflow |
| Send Reminder | Re-notify a pending approver | Approval Workflow |
| Cancel Change Approval | Cancel (not reject) a pending individual approval | Approval Workflow |
| Update Approval Chain Rule | Set multi-level/sequential approval ordering | Approval Workflow |
| Create Note | Add an audit-trail note to a change | Change Records |
| List Change Fields | Discover the tenant's live field/enum configuration | Discovery |

## Verification checklist

- [ ] `status`, `priority`, `impact`, `risk`, and `change_type` were explicitly set on create — not
      left to an undocumented default
- [ ] Any status-changing Update was confirmed via a follow-up View, not assumed successful from the
      request alone
- [ ] No approve/reject action was attempted via API — any such request was reported as out of scope
      and redirected to the approver's own action in the product
- [ ] A Cancel (approval or approval group) was reported as CANCELLED, never mislabeled as REJECTED
- [ ] `workspace_id` changes went through Move, never attempted via Update
- [ ] Delete was only performed after explicit operator confirmation, and restore capability was not
      promised without confirming the Restore endpoint against the live tenant
- [ ] Final report includes the change `id`, and pre/post `status` and `approval_status` values
