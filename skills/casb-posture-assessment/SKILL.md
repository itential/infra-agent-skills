---
name: casb-posture-assessment
description: Read an organization's currently observed CASB risk and compliance posture (discovered shadow-IT applications, risky OAuth grants, policy-violation events, sanctioned-app risk scores) on a supported Cloud Access Security Broker (CASB) platform, and map findings to that platform's own documented risk categories. Read-only diagnostic assessment, not a policy-writing operation — see casb-policy-management for creating/updating/deleting policies. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. No vendor coverage yet — see references/INDEX.md.
argument-hint: "[platform] [assessment: shadow_it|oauth_grants|policy_violations|risk_score] [scope: org|user|app]"
---

# CASB Posture Assessment

Reads an organization's currently observed CASB risk/compliance posture on whichever platform the
caller is targeting, mapping discovered findings to that platform's own documented risk categories —
not a configuration-change skill.

## Why this skill has a different shape than most others in this repo

This skill is **diagnostic-shaped**, not CRUD-shaped (see `AGENTS.md` rule 2) — the useful output is
a posture assessment (what shadow-IT apps were discovered, which OAuth grants look risky, which
policies were violated and by whom) plus the platform's own supporting evidence, not a created,
updated, or deleted record. This skill has no destructive-action confirmation gates because reading
discovered/observed state doesn't change anything on the platform. If a future addition to this
skill ever proposes a remediation action (revoking an OAuth grant, quarantining a file, blocking an
app), that action needs its own confirmation gate exactly like any CRUD skill's destructive step —
and likely belongs in `casb-policy-management` or a dedicated remediation skill, not folded in here.

## When to use this skill

- Reading an organization's discovered shadow-IT applications, risky OAuth/API grants, policy
  violation events, or a sanctioned app's risk score, on a supported platform.
- Not for creating, updating, or deleting an access-control or DLP policy — see
  `casb-policy-management` for that. This skill only reads and reports observed state; it never
  writes a policy or performs remediation.

## Universal concepts (shared CASB posture vocabulary, not a wire standard)

*(To be filled in as vendors are added — see `AGENTS.md` rule 4: only claims verified true across
every vendor actually listed belong here. Do not pre-populate this section with assumptions before
a vendor's real behavior has been checked against them.)*

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Identify the assessment type** — shadow-IT discovery, OAuth-grant risk, policy-violation
   events, or an app/user risk score. This determines which read/report path in
   `references/<platform>/procedure.md` to follow; not every platform supports every assessment
   type.
3. **Open `references/<platform>/procedure.md`** and follow it exactly — it maps that platform's
   own discovered/observed data to its documented risk categories.
4. **Report the finding together with its supporting evidence** (the literal API/report output that
   backs it) — never present a risk score or finding without the evidence behind it.

## Known limitations

- No vendor coverage yet — see `references/INDEX.md`. A platform not listed there needs a new
  reference file before this skill can be used for it.
- Read-only assessment only. Does not write policy, revoke a grant, quarantine a file, or perform
  any other remediation — see `casb-policy-management` for policy writes; remediation actions may
  need a separate future capability.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new
finding type, a corrected field, a changed API path — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific read-only operations it uses.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] Assessment type confirmed as supported by that platform before attempting it
- [ ] That platform's own `procedure.md` was followed for the requested assessment type
- [ ] Every finding reported together with the literal evidence that supports it — never a bare
      risk score or conclusion
- [ ] No policy change or remediation action was performed — this skill is read-only
