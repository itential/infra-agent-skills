---
name: crm-contact-management
description: Create, read, update, and delete contact records (individual people) on a supported customer relationship management (CRM) platform — currently Salesforce (REST API, generic sobjects/Contact endpoints). Distinct from cmdb-asset-management (internal infrastructure/service inventory) and change-management (internal ITSM change requests) — this skill manages external-facing customer/prospect contact data, a different object model and typically a different platform entirely. Contact records only; account/organization records are not covered. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. See references/INDEX.md for exact per-vendor scope.
argument-hint: "[platform] [action: create_contact|read_contact|update_contact|delete_contact] [record identifier, fields]"
---

# CRM Contact Management

Manages contact records on whichever CRM platform the caller is targeting, following
that platform's own documented procedure exactly.

## When to use this skill

- Creating, reading, updating, or deleting a contact (an individual person) record on a supported
  CRM platform.
- Not for internal infrastructure inventory (see `cmdb-asset-management`) or internal ITSM change
  requests (see `change-management`) — those are internally-facing records on different platforms
  with a different object model; this skill is specifically customer/prospect relationship data.
- Not for deals/opportunities, support cases/tickets, or marketing-campaign objects — this skill
  covers only the contact record type (account/organization records are not covered either); a platform not listed here for those other
  object types needs its own future capability, not an expansion of this one.

## Universal concepts (shared CRM vocabulary, not a wire standard)

There is no wire-level standard behind CRM contact records the way DNS has RFC 1035 — these claims are
drawn from Salesforce's own documented behavior, the only vendor covered so far, and must be
re-checked against each new vendor added (see `AGENTS.md` rule 4):

- **A contact record's identity is platform-assigned, not caller-supplied.** The unique record
  identifier is generated at creation time; a create call never accepts a caller-chosen ID.
- **A contact's name is the one structurally-required field; nearly everything else is optional
  unless an org/tenant has layered its own validation on top.** Don't assume fields like email or
  phone are mandatory just because they're commonly populated in practice.
- **Updates are partial, not whole-record replacements.** Sending only the changed fields is both
  sufficient and correct — omitted fields keep their existing stored values rather than being cleared.
- **A successful write and a duplicate-detection match are two different facts.** Where a platform
  offers built-in matching/duplicate-management, it can be enabled or disabled per org — never assume
  a create call was deduplicated against an existing record unless that platform's own procedure
  confirms it ran.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away, and don't conflate a new record being created with an existing one being matched/updated,
   on a platform that performs deduplication before write.

## Known limitations

- Vendor coverage is currently Salesforce only — see `references/INDEX.md`. A platform not listed
  there needs a new reference file before this skill can be used for it.
- Scope is Contact records only (create/read/update/delete). Account/organization records are not
  covered for any vendor; adding them is future work.
- Does not cover deals/opportunities, support cases/tickets, marketing campaigns, or any other CRM
  object type beyond contact records.
- Does not cover internal infrastructure or ITSM records — see `cmdb-asset-management` and
  `change-management` for those.

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
- [ ] That platform's own `procedure.md` was followed, including its own deduplication/matching
      behavior and confirmation gates on destructive changes (contact deletion)
- [ ] Outcome reported using the platform procedure's own status vocabulary, distinguishing a newly
      created record from a matched/updated existing one where the platform makes that distinction
