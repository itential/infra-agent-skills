---
name: zero-trust-access-policy-management
description: Create, update, or delete an access/segmentation policy rule on a SASE or Zero Trust Network Access (ZTNA) platform — Zscaler Internet Access (ZIA) URL/cloud-app filtering rules, Zscaler Private Access (ZPA) application-segment access policy rules, or Netskope private-access (NPA) policy rules via Netskope's REST API v2. Use when a policy rule governing what a user, group, or device may reach (a URL/cloud app on ZIA, a private application segment on ZPA, or a private app on Netskope NPA) needs to be created, changed, or removed. Assumes an authenticated API client for the target platform is already available (Zscaler OneAPI OAuth2 client-credentials token for ZIA/ZPA, a Netskope API v2 token for Netskope); this skill does not provision or authenticate that client.
argument-hint: "[platform] [action] [rule_name] [fields...]"
---

# Zero Trust Access Policy Management

Creates, updates, or deletes one access/segmentation policy rule on a supported SASE/ZTNA platform,
following that platform's own documented procedure, field rules, and ordering/validation behavior
(`references/<vendor>/procedure.md`).

## When to use this skill

- A URL/cloud-app filtering rule needs to be created, updated, or deleted on Zscaler ZIA.
- An access policy rule governing which users/groups can reach an application segment needs to be
  created, updated, or deleted on Zscaler ZPA.
- A private-access (NPA) policy rule needs to be created, updated, or deleted on Netskope.
- Not for creating the underlying resource a rule references (a ZPA application segment/segment
  group as a standalone object with no rule, a Netskope private app definition, a ZIA URL category
  definition) unless the platform's own rule-creation procedure requires defining it inline as part
  of the same call — check the vendor's `procedure.md` for where that line falls.
- Not for network-layer firewall rules (see `firewall-management`) or SaaS/CASB inline data-control
  policies (see `casb-policy-management`) — this skill covers per-user/group access to URLs, cloud
  apps, and private application segments on a SASE/ZTNA platform.

## Universal concepts (apply regardless of platform)

- **A policy rule is an ordered match-then-action record.** Every platform here evaluates rules in a
  defined sequence and stops at the first match — where a new rule lands in that order (explicit
  `order`/`rule_order`/`priority` field, or an implicit top/bottom insertion) determines whether it
  ever actually applies. Confirm the platform's ordering behavior before creating a rule that must
  take precedence over (or defer to) an existing one.
- **Rules bind a scope (who/what/where) to an action (allow/block/isolate/etc.).** The scope side
  varies enormously by platform (users, groups, locations, device posture, source IP, destination
  app/category) but the create/update/delete lifecycle and the "does this match, then what happens"
  shape is shared.
- **Whether a saved rule change is live depends on the platform.** Where a platform documents no
  separate publish step, a create/update/delete reaches live traffic at once or on next policy
  evaluation. Where it documents one, the saved change is not enforced until that step runs, and a
  vendor's procedure states whether that step also applies other pending changes on the tenant.
  Treat every create/update/delete, and every publish step, as consequential to production traffic
  and gate it accordingly (see each vendor's own procedure).
- There is no single cross-vendor wire-level standard grounding SASE/ZTNA policy APIs (unlike, say,
  DNS's RFC 1035/2136) — every field name, action vocabulary, and scope-condition shape below is
  platform-specific; treat any apparent similarity between vendors as coincidental, not a shared
  contract, unless a vendor's own procedure says otherwise.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. If it
   isn't one of the platforms in `references/INDEX.md`, stop: this skill doesn't cover it, and does
   not improvise a generic procedure for an unsupported platform.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist. This file is intentionally the router; the real steps live per platform because rule
   scope models, action vocabularies, and ordering semantics genuinely differ across ZIA, ZPA, and
   Netskope (see `references/INDEX.md` for why).
3. **Report the outcome** using that platform procedure's own status vocabulary (e.g. `CREATED`,
   `UPDATED`, `DELETED`, `REJECTED_*`, `FAILED`) — don't normalize it away.

## Known limitations

- Does not cover defining the underlying referenced resource as a standalone lifecycle (a ZPA
  application segment or segment group's own create/update/delete outside of a rule, a Netskope
  private app or publisher's own lifecycle, a ZIA URL category's own custom-category management) —
  only the vendor's documented rule-creation flow that references those objects by ID/name is in
  scope. Where a vendor's rule-create procedure requires inline creation of a referenced object as a
  documented part of the same call, that inline step is in scope (see the vendor's own
  `procedure.md`).
- Does not cover ZIA firewall filtering rules, DLP rules, or file-type-control rules — only URL/cloud
  application filtering rules are in scope for ZIA under this skill.
- Does not cover ZPA policy types other than the access policy (application-segment reachability)
  type — timeout, client-forwarding, inspection, isolation, and other ZPA policy set types are out of
  scope.
- Does not cover Netskope's real-time (CASB inline) policy rules, internet-access rules, or SaaS
  Posture Management policies — only the private-access (NPA) policy rule family is in scope for
  Netskope under this skill.
- Platform coverage is exactly the three vendors in `references/INDEX.md` — a platform not listed
  there needs a new `references/<platform>/procedure.md` before this skill can be used for it.

## Contributing to this skill

**`SKILL.md` itself should only ever change for two reasons: a bug in the universal concepts/router
logic above, or adding a pointer to a newly-supported platform.** Platform-specific procedure
changes — a new error code, a corrected field name, a changed API path — belong in that platform's
own `references/<platform>/procedure.md` and `endpoints.md`, never here. If you're about to add
vendor-specific detail to this file, put it in the platform's reference file instead.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations/mechanisms.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates and error
      handling — not a generic/improvised sequence
- [ ] Rule ordering/priority was confirmed or explicitly set, not left to an unverified default
- [ ] Outcome reported using the platform procedure's own status vocabulary
