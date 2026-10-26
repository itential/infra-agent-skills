---
name: incident-management
description: Create, read, update, assign, acknowledge, hold, resolve, reopen, and close an incident record on a supported ITSM or incident-response platform — currently ServiceNow (standard state model), PagerDuty, Opsgenie, Jira Service Management, and ManageEngine ServiceDesk Plus. The break/fix counterpart to change-management, it covers records for unplanned disruptions and their lifecycle, not planned changes. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. Check references/INDEX.md for which platforms and operations are covered; paging an on-call responder and problem or major-incident handling are not covered.
argument-hint: "[platform] [action: create|read|update|assign|acknowledge|hold|resolve|reopen|close] [incident number or fields]"
---

# Incident Management

Runs an incident record lifecycle — create, update, assign, acknowledge, hold, resolve, reopen, close — on whichever
platform the caller is targeting, following that platform's own documented state model and required
fields.

## When to use this skill

- Creating, reading, updating, assigning, acknowledging, placing on hold, resolving, reopening, or closing
  an incident record on a supported ITSM or incident-response platform. Which of those actions a platform supports is
  platform-dependent; see `references/INDEX.md`.
- Not for planned changes — see `change-management`. Linking an incident to an existing change is part
  of the platform's own procedure; creating or advancing the change is not.
- Not for delivering a message to a channel or person — see `notifications`.
- Not for monitor, threshold, or alert-rule definitions, or for acknowledging or resolving an alert
  raised by an observability platform — see `alert-monitor-management`. This skill covers incident
  records on an ITSM platform.
- Not for problem records, major-incident handling, or paging an on-call responder; no procedure here
  covers them yet.

## Universal concepts (shared incident-handling vocabulary, not a wire standard)

Several platforms are documented today, so these are claims expected to hold for any listed platform, and
do not extend automatically to a platform not listed in `references/INDEX.md`. Where a platform
differs, its own procedure wins.

- **An incident moves through named states from open to resolved.** Some platforms add states before
  that (acknowledged, on hold) or after it (closed). The state names and the transitions allowed between
  them are the platform's own, and some platforms let each site or workflow define them; do not assume one platform's names or end state on another.
- **Resolving and closing are different steps, where the platform separates them.** Resolving declares
  the service restored and can usually be undone by reopening; closing is final where documented. Treat both as
  confirmation points and report which one happened.
- **Internal notes and caller-visible comments are separate channels, where the platform separates
  them.** Check which one a platform's note field reaches before writing sensitive content.
- **Where a platform computes priority from impact and urgency,** set the inputs rather than the result.
- **A platform may change a record in response to a write** (clearing a hold reason, adjusting an
  assignment, refusing a transition). Some platforms apply writes asynchronously, so
  wait for the request to complete before reading the record back to confirm the state you asked for.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- Platform coverage is in `references/INDEX.md`; a platform not listed there needs a new reference
  file before this skill can be used for it.
- Does not cover planned changes (see `change-management`), configuration-item records (see
  `cmdb-asset-management`), notification delivery (see `notifications`), or alert handling on
  observability platforms (see `alert-monitor-management`).
- Does not cover problem records, major-incident management, or on-call paging.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed API path — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates on
      resolving and closing an incident
- [ ] Outcome reported using the platform procedure's own status vocabulary
