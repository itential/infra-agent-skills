---
name: cmdb-asset-management
description: Create, read, update, and delete Configuration Items (CIs) in a CMDB/asset-management platform, and read relationships between them — currently ServiceNow (Table API + CMDB Instance API, the latter routed through Identification and Reconciliation for deduplication) and iTop (REST/JSON services). Use when an agent needs to manage inventory/asset records themselves, distinct from change requests, tickets, or DNS/IPAM records that reference those assets. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. Does not cover discovery/service-mapping configuration, CI class schema administration, or writing new relationship records.
argument-hint: "[platform] [action: create|read|update|delete|read_relationships] [ci class/id, fields]"
---

# CMDB / Asset Management

Manages Configuration Item (CI) records and their relationships on whichever CMDB/asset-management
platform the caller is targeting, following that platform's own documented procedure — including any
deduplication/identification mechanism the platform provides for writes.

## When to use this skill

- Creating, reading, updating, or deleting a CI (server, application, service, etc.) or reading the
  relationships between CIs, on a supported platform.
- Not for change requests (see `change-management`), DNS records (see `dns-record-management`), IP
  address allocation (see `ipam-allocation`), or a physical asset's rack-unit/power placement (see
  `dcim-asset-management`) — those are adjacent records that may *reference* a CI by identifier
  (or represent the same physical device from a different angle), but managing them is out of scope
  here.

## Universal concepts (shared CMDB vocabulary, not a wire standard)

- **A CI write and a CI's identity are not the same question.** Some platforms (ServiceNow via IRE)
  route writes through an identification step that decides whether the payload matches an *existing*
  record before deciding to create a new one, while others simply create a new record on every create call — treat "the write succeeded" and "a new record was
  created" as two different facts to confirm, not one.
- **Where multiple sources feed the same platform, reconciliation rules (where they exist) decide which
  source wins on a contested field** — a successful write doesn't guarantee the value sticks if a
  higher-priority source claims that field. Don't assume last-write-wins on a platform with a documented
  reconciliation mechanism.
- **A relationship is directional — always check both sides.** "What does this CI depend on" and "what
  depends on this CI" are different queries; don't assume checking one direction covers both.
- **Deleting a CI is rarely gated by relationship checks at the platform level** — confirming nothing
  currently depends on a CI before deleting it is this skill's own discipline in every platform
  procedure under this category, not something to assume the platform enforces automatically. Some
  platforms go further and cascade a delete to linked objects, so check for a preview or dry-run option.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — including whether a
   write created a new record or matched/updated an existing one, where the platform makes that
   distinction.

## Known limitations

- Currently covers ServiceNow and iTop only — see `references/INDEX.md`. A platform not listed there needs a
  new reference file before this skill can be used for it.
- Does not cover discovery/service-mapping configuration, CI class schema administration, or writing
  new relationship records — only reading existing relationships is covered where documented.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes belong in that
platform's own `references/<platform>/procedure.md` and `endpoints.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own identification/reconciliation
      or equivalent deduplication behavior, and confirmation gates
- [ ] Outcome reported using the platform procedure's own status vocabulary, distinguishing a new
      record from a matched/updated existing one where the platform makes that distinction
