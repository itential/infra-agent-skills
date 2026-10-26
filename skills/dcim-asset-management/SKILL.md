---
name: dcim-asset-management
description: Create, read, update, and delete a physical data-center asset (server, PDU, patch panel, network device chassis) and its rack-unit placement on a supported Data Center Infrastructure Management (DCIM) platform. Distinct from cmdb-asset-management, which manages logical Configuration Items and their service/relationship model — this skill manages the physical object's location, not its logical role. The same real-world server is often represented in both systems from two different angles; that overlap is expected, not a reason to merge the skills. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. Currently covers NetTerrain (Graphical Networks), NetBox, and Nautobot — see references/INDEX.md for the full vendor list.
argument-hint: "[platform] [action: create_asset|read_asset|update_asset|delete_asset|assign_rack_unit] [asset identifier, fields]"
---

# DCIM Asset Management

Manages physical data-center assets and their rack-unit placement on whichever DCIM platform the
caller is targeting, following that platform's own documented procedure exactly.

## When to use this skill

- Creating, reading, updating, or deleting a physical asset record, or assigning/reassigning its
  rack-unit position, on a supported platform.
- Not for a logical Configuration Item's service/relationship model (what depends on what,
  application ownership) — see `cmdb-asset-management` for that. The same physical server commonly
  has a record in both systems: this skill's record is "where is it and what powers it," the CMDB's
  is "what does it do and what relies on it." Confirming or syncing a physical asset's identifier
  between the two systems is a real, expected integration point, not something either skill
  performs automatically — check both systems' own procedures if a caller needs both facts.
- Not for environmental/power-draw monitoring (temperature, humidity, real-time power consumption)
  — that is read-only telemetry, a different shape from this skill's CRUD operations, and does not
  exist as a capability in this repository yet.

## Universal concepts (shared DCIM vocabulary, not a wire standard)

No claims are stated as shared across vendors. Each platform's own procedure states what holds for
it; do not assume shared behavior.

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

- Vendor coverage is limited to what's listed in `references/INDEX.md` — a platform not listed there
  needs a new reference file before this skill can be used for it.
- Does not cover logical CI/service-relationship data — see `cmdb-asset-management` for that.
- Does not cover environmental or real-time power-draw monitoring — that would be a separate,
  read-only/diagnostic-shaped capability, not part of this CRUD-shaped one.

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
      destructive changes (asset deletion, rack-unit unassignment affecting a live device)
- [ ] Outcome reported using the platform procedure's own status vocabulary
