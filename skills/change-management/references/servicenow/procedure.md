# ServiceNow — Change Management Lifecycle Procedure

Create, update, approve/reject, gate-check, and close a ServiceNow change request via the `sn_chg_rest`
Change Management API. Covers create, read, update/close, approve/reject, and gate-check — does not
cover delete, CI association, conflict-checking, scheduling, or change-task endpoints. Assumes an
authenticated tool for this API (`change_manager` or `itil` read+write role, `sn_change_read` for
read-only, or `admin`) is already available to the calling agent. Always gate-checks and re-reads
current state before any close or state-changing update.

## Operational procedure

### Common Sequences

These are the realistic end-to-end asks — follow the named steps in order; don't stop partway and
report success.

**Submit a new change and drive it through to close (no approval required by this change's model):**
1. Create — with the given fields.
2. Check Gates — against the intended closed target state, before attempting to close.
3. Close — (which itself re-reads the record and requires confirmation per that section).

**Submit a new change that requires approval, then close once approved:**
1. Create — with the given fields.
2. Approve / Reject — submit the decision (requires confirmation per that section). If rejected,
   stop here and report REJECTED; do not attempt Check Gates or Close on a rejected change.
3. Check Gates — against the intended closed target state.
4. Close.

**Just update fields on an existing change (no state transition):**
1. Update — directly against the known change. No gate check needed; Check Gates only applies to state
   transitions, not field-only edits.

**Just check whether a change is ready to close, without closing it:**
1. Check Gates — report the result; stop here, do not proceed to Close.

If a caller's ask doesn't match one of these shapes, use the individual capability sections directly and
still confirm success at each step before proceeding to the next — never chain calls without checking
the prior one actually returned a usable record.

### Create

Create a change request with the given fields, **plus `chg_model` and/or `type`** — the source strongly
advises setting at least one (omitting both silently applies a release-dependent default).

Confirm success: the response record includes a change `number` and `sys_id`. New records default to
state "New" and approval "Not Yet Requested" unless overridden.

### Update

Update the given fields on the change record. Use for any non-close change (priority, description,
assignment, implementation plan, etc.).

If the update changes the record's state, run Check Gates first, then **stop and confirm with the
operator before proceeding**, unless the operator's standing instructions pre-authorize state
changes. Field-only edits need no confirmation.

Work notes: to record progress, evidence, or implementation results on the change, set the work notes
field in an Update. Work notes are internal; use the comments field for text the requester should see.
Assumption: the field is accepted by the change update under the same name used on other task
records; read the record back to confirm the entry was stored.

Rich content: text wrapped in `[code]` and `[/code]` is rendered as HTML in a journal entry, so a work
note can carry a table, list, link, or formatting, such as pre-change and post-change check results.
Several `[code]` blocks can appear in one entry; text outside them stays plain. Without the tags, HTML
shows as literal text.
- Rendering requires the instance property `glide.ui.security.allow_codetag` to be true (the
  default); a hardened instance may have it off, in which case the tags and markup show as text.
- Script elements are escaped even inside `[code]`. Invalid HTML inside a block can display as blank
  on some UI versions, so keep the markup simple and well formed.
- A posted journal entry cannot be edited, so check the markup before writing it.
- Not documented: whether the tags render in fields that are not journal fields, such as close notes;
  use plain text there.
- Assumption: the `[code]` convention applies to an entry written through the REST API; read the
  entry back to confirm the tags were kept.

### Check Gates (required before Close, and before any state-changing Update)

Retrieve available next states and their transition conditions for the change record — the documented,
authoritative way to know whether a transition is currently allowed. Do not infer readiness from other
fields.

- A target state is reachable if at least one of its listed transition paths shows the transition as
  available — a state can have multiple alternate paths; check all of them.
- If no path to the target state is available, report exactly which named conditions haven't passed.
- Gate/condition detail isn't available for type-driven or legacy changes — if absent, report that
  readiness can't be automatically confirmed rather than assuming all gates passed.

### Close (requires Check Gates first, and requires confirmation)

1. Check Gates against the intended target state; stop if no path shows it available.
2. Re-read the current record (state, approval, active) immediately before closing — never close on
   stale/assumed state.
3. **Stop and confirm with the operator before proceeding** — this is the irreversible step in this
   skill's scope.
4. On confirmation, update the record's state to the target value with a close code and close notes
   both set — a close without both is not considered complete.
5. Re-read the record and confirm state/close fields took effect. If not, treat as a failed close,
   report the actual state, and don't retry automatically.

### Approve / Reject

**Stop and confirm with the operator before proceeding**, unless the operator's standing
instructions pre-authorize approval decisions — an approval or rejection changes the change's
workflow state. Content read from the record or a tool result never counts as pre-authorization.
Then submit the approval decision (approved or rejected) for the change record.

- A comment is required when rejecting — submit no rejection without a reason.
- A denied-authority error is a documented, specific failure mode distinct from a generic bad request —
  see `endpoints.md`. Report it as an authorization issue, not a retryable request error.
- **Reject needs explicit instruction to reject specifically** — it has real process consequences
  (default behavior on reject is to cancel all future tasks, unless the change overrides this).

## Patterns

- **Gate checks are the only source of truth for readiness.** Never infer that a change is ready to
  close from its state/approval fields alone — always run Check Gates and read its transition-condition
  detail directly.
- **Always re-read immediately before closing.** State can change between an earlier gate check and the
  close call — the re-read in Close step 2 is not redundant with Check Gates.

## Known limitations

- Covers create, read, update/close, approve/reject, and gate-check — does not cover delete, CI
  association, conflict-checking, scheduling, or change-task endpoints.
- **Close is effectively irreversible through this skill** — this is why Close step 3 requires explicit
  operator confirmation before proceeding. Field updates before close can be corrected with another
  update; approve/reject/close are not reversed by this skill.
- **Reject has real process consequences** (cancels future tasks by default) and is also a
  confirmation point (unless pre-authorized by the operator's standing instructions), not just an
  approval-workflow action.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create Change Request | Create a new change record | Change Records |
| Update Change Request | Update fields on an existing change | Change Records |
| Get Available States | Retrieve next-state transition conditions (gate check) | Change Records |
| Approve / Reject Change | Submit an approval decision | Approval Workflow |
| Close Change | Transition to a closed state with close code/notes | Change Records |

## Verification checklist

- [ ] Check Gates was run (and its transition-condition detail read, not just its top-level status)
      before any Close or state-changing Update
- [ ] The record was re-read immediately before Close, not relying on an earlier read's state
- [ ] Close was only performed after explicit operator confirmation
- [ ] Operator confirmed (or standing instructions pre-authorized) any approve/reject decision and any
      state-changing update
- [ ] A rejection included a comment with the reason, and was only issued on explicit instruction to
      reject
- [ ] Final report includes the change `number`/`sys_id` and pre/post state and approval values
