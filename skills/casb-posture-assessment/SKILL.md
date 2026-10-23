---
name: casb-posture-assessment
description: Read an organization's currently observed CASB risk and compliance posture (security and compliance findings on connected SaaS and cloud integrations, DLP content matches, and, where a platform provides them, discovered shadow-IT applications, risky OAuth grants, or app risk scores) on a supported Cloud Access Security Broker (CASB) platform, and map findings to that platform's own documented risk categories. Covers Cloudflare One CASB. Read-only diagnostic assessment, not a policy-writing operation — see casb-policy-management for creating/updating/deleting policies. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. Assessment types per platform are in references/INDEX.md.
argument-hint: "[platform] [assessment: posture_findings|content_findings|shadow_it|oauth_grants|policy_violations|risk_score] [scope: org|integration|asset|user|app]"
---

# CASB Posture Assessment

Reads an organization's currently observed CASB risk/compliance posture on whichever platform the
caller is targeting, mapping discovered findings to that platform's own documented risk categories —
not a configuration-change skill.

## Why this skill is diagnostic-shaped

This skill reads and interprets state; it does not create, update, or delete records. The useful
output is a posture assessment (which findings exist, how severe they are, which assets they affect,
plus shadow-IT apps, risky OAuth grants, or violated policies where a platform provides them)
together with the platform's own supporting evidence. It has no destructive-action confirmation
gates because reading observed state changes nothing on the platform. Any action that would change
state (revoking an OAuth grant, quarantining a file, blocking an app, ignoring a finding) is outside
this skill; it would need its own confirmation gate, and policy changes belong in
`casb-policy-management`.

## When to use this skill

- Reading an organization's security and compliance findings, DLP content matches, discovered
  shadow-IT applications, risky OAuth/API grants, policy violation events, or a sanctioned app's
  risk score, where the platform provides them (see `references/INDEX.md`).
- Not for creating, updating, or deleting an access-control or DLP policy — see
  `casb-policy-management` for that. This skill only reads and reports observed state; it never
  writes a policy or performs remediation.

## Universal concepts (shared CASB posture vocabulary, not a wire standard)

- Observed state is as of the platform's last scan or sync, not live, where documented. Report how
  recent it is when it matters.
- Platforms may let operators suppress findings from the default view. Say whether suppressed items
  were included.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Identify the assessment type** — security/compliance findings, DLP content matches, shadow-IT
   discovery, OAuth-grant risk, policy-violation events, or an app/user risk score. This determines
   which read/report path in `references/<platform>/procedure.md` to follow; not every platform
   supports every assessment type.
3. **Open `references/<platform>/procedure.md`** and follow it exactly — it maps that platform's
   own discovered/observed data to its documented risk categories.
4. **Report the finding together with its supporting evidence** (the literal API/report output that
   backs it) — never present a risk score or finding without the evidence behind it.

## Known limitations

- A platform not listed in `references/INDEX.md` is not covered by this skill.
- Read-only assessment only. Does not write policy, revoke a grant, quarantine a file, or perform
  any other remediation — see `casb-policy-management` for policy writes. Remediation actions
  are not covered by either skill unless a platform's policy procedure includes them.

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
