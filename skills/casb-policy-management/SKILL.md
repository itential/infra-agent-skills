---
name: casb-policy-management
description: Create, read, update, and delete access-control and data-loss-prevention (DLP) policies bound to a sanctioned cloud application on a supported Cloud Access Security Broker (CASB) platform. Distinct from casb-posture-assessment, which reads an org's current CASB-observed risk/compliance state rather than writing policy. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. No vendor coverage yet — see references/INDEX.md.
argument-hint: "[platform] [action: create_policy|read_policy|update_policy|delete_policy] [policy identifier, bound app, fields]"
---

# CASB Policy Management

Manages access-control and DLP policies bound to a sanctioned cloud application on whichever CASB
platform the caller is targeting, following that platform's own documented procedure exactly.

## When to use this skill

- Creating, reading, updating, or deleting an access-control policy (e.g. block/allow/require-MFA
  for a given app-and-user-group combination) or a DLP policy (e.g. block upload of a document
  matching a sensitive-data pattern) on a supported platform.
- Not for reading an org's current discovered-risk or compliance-posture state — see
  `casb-posture-assessment` for that. This skill only writes/manages policy objects; it does not
  perform discovery or produce a risk assessment.

## Universal concepts (shared CASB policy vocabulary, not a wire standard)

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
- Does not cover shadow-IT discovery, risk scoring, or compliance-posture reporting — see
  `casb-posture-assessment` for that.

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
      destructive changes (policy deletion, which may remove active DLP/access enforcement)
- [ ] Outcome reported using the platform procedure's own status vocabulary
