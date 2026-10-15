---
name: change-management
description: Create, update, and manage the approval/close lifecycle of a change request on a supported ITSM platform — currently ServiceNow (sn_chg_rest, full gate-check/approve/reject/close), Freshservice (API v2 /api/v2/changes — no API-level approve/reject or gate-check, cancel-only), Jira Service Management (customer request against a change-configured request type; discoverable transitions but no readiness gate; assignee-only one-shot approve/decline), and BMC Helix ITSM (simplified REST API — search/retrieve/update, no discovery mechanism found for transitions/gates). Use when an agent needs to run any part of an ITSM change request lifecycle. Assumes an authenticated client/tool for the target platform's change management API is already available; this skill does not provision or authenticate it. Does not cover delete, CI association, conflict-checking, scheduling, or change-task endpoints on any platform. Not every platform supports every action — check references/INDEX.md before assuming approve/reject or gate-check are available.
argument-hint: "[platform] [action: create|update|approve|reject|check_gates|close|cancel_approval|transition] [change id or fields]"
---

# Change Management

Runs an ITSM change request lifecycle — create, update, approve/reject, gate-check, close — on whichever
platform the caller is targeting, following that platform's own documented procedure and state model.

## When to use this skill

- Creating, updating, closing, or managing the approval workflow of a change request on a supported
  ITSM platform — exactly which of those (including approve/reject and gate-check) the target platform
  supports is platform-dependent; see `references/INDEX.md`.
- Not for delete, CI association, conflict-checking, scheduling, or change-task endpoints — no platform
  procedure under this skill covers those.

## Universal concepts (common ITSM change-management vocabulary, not a wire standard)

Unlike a protocol-grounded skill (e.g. DNS/RFC 1035), there is no single spec every change-management
platform implements — this section states practice-level concepts common across ITSM tooling, not
RFC-derived rules. **Not every concept below is guaranteed on every platform** — confirm against
`references/INDEX.md` before assuming a capability exists:

- **A change moves through named states, but "how do I know what's next" varies by platform.**
  ServiceNow gates transitions with a dedicated readiness check; Jira exposes a "get available
  transitions" list (discoverable, but not a readiness gate — it just says what the workflow currently
  permits); Freshservice and BMC treat status as a plain field with no discovery mechanism found at
  all. Where no gate/discovery exists, the calling agent is responsible for sequencing status changes
  sensibly — the API itself won't stop an out-of-order one.
- **Approve/reject capability is a spectrum, not binary — check the specific platform.** ServiceNow
  lets this skill submit the approval decision directly on anyone's behalf (permission allowing). Jira
  allows an API-driven approve/decline, but strictly for the credential matching the assigned approver,
  and only once (no re-decision). Freshservice restricts the API to *observing* approval state and
  *cancelling* a pending request — approve/reject can only be done by the approver in the product
  itself. Check `references/INDEX.md` before promising any specific approve/reject capability to the
  caller; if the target platform doesn't support what's being asked, say so rather than attempting a
  workaround.
- **Approval and state are related but distinct.** A change can be approved but not yet in a closable
  state, or vice versa depending on the platform's model — check both explicitly rather than assuming
  one implies the other.
- **Close (or the platform's equivalent terminal state) is effectively irreversible.** Every platform
  procedure under this skill treats it as a required operator-confirmation point.
- **Cancelling a pending approval is not the same as rejecting it.** Where a platform only supports
  cancellation (no reject), report the outcome as CANCELLED, not REJECTED — cancelling means the request
  was withdrawn, not that an approver declined it.
- **Rejection, where supported, has real process consequences** beyond just "not approved" (e.g.
  auto-cancelling dependent tasks) — treat it as its own confirmation point, not a lesser version of
  approval.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. If it isn't
   one of the platforms in `references/INDEX.md`, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- Currently covers ServiceNow, Freshservice, Jira Service Management, and BMC Helix ITSM — see
  `references/INDEX.md` for exactly which actions each supports (they are not symmetric — see
  Universal concepts above). A platform not listed there needs a new
  `references/<platform>/procedure.md` before this skill can be used for it.
- Does not cover delete, CI association, conflict-checking, scheduling, or change-task endpoints on any
  platform.
- Approve/reject-by-API is platform-dependent, not guaranteed — check `references/INDEX.md` before
  telling a caller this skill can approve or reject a change on their behalf.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed API path — belong in that platform's own
`references/<platform>/procedure.md` and `endpoints.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates and error
      handling — not a generic/improvised sequence
- [ ] Outcome reported using the platform procedure's own status vocabulary
