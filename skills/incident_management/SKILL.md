---
name: incident_management
description: Create, read, update, assign, acknowledge, resolve, and close incident records (and, where a platform models them separately, problem records) on a supported ITSM or on-call platform. The break/fix counterpart to change_management: it covers unplanned-disruption records and their lifecycle, not planned changes. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. No vendor coverage yet — see references/INDEX.md.
argument-hint: "[platform] [action: create|read|update|assign|acknowledge|resolve|close] [record id or fields]"
---

# Incident Management

Runs an incident record lifecycle — open, update, assign, acknowledge, resolve, close — on whichever platform the
caller is targeting, following that platform's own documented state model and required fields.

## When to use this skill

- Opening, reading, updating, assigning, acknowledging, resolving, or closing an incident (or problem)
  record on a supported platform. Which of those actions a platform exposes is platform-dependent; see
  `references/INDEX.md`.
- Not for planned changes — see `change_management`. Linking an incident to a change is a
  platform-specific field or relation and is documented in that platform's own procedure.
- Not for delivering a message to a channel or person — see `notifications`. An on-call platform's
  paging of a responder is part of its incident record lifecycle and belongs here; a plain chat or
  email message does not.
- Not for monitor, threshold, or alert-rule definitions — see `alert_monitor_management`.

## Universal concepts (shared incident-handling vocabulary, not a wire standard)

*(To be filled in as vendors are added — see `AGENTS.md` rule 4: only claims verified true across
every vendor actually listed belong here. Do not pre-populate this section with assumptions before
a vendor's real behavior has been checked against them.)*

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- No vendor coverage yet — see `references/INDEX.md`. A platform not listed there needs a new
  reference file before this skill can be used for it.
- Does not cover planned changes (see `change_management`), configuration-item records (see
  `cmdb_asset_management`), or notification delivery (see `notifications`).

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
      resolving or closing a record, and any bulk update
- [ ] Outcome reported using the platform procedure's own status vocabulary
