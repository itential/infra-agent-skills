# Compute Instance Provisioning — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| _(none yet)_ | | | |

## Adding a new vendor

1. Create `references/<vendor>/procedure.md` following the shape of an existing single-vendor
   capability (e.g. `skills/cmdb_asset_management/references/servicenow/procedure.md`) as a
   template: Operational procedure → Patterns → Known limitations → Tools → Verification checklist.
2. Add `endpoints.md` (wire-level calls) alongside it, if the platform is REST/API-driven — CLI-driven
   platforms keep commands inline in `procedure.md` instead (see `AGENTS.md` rule 6).
3. Keep this vendor's procedure scoped to the instance lifecycle. A cloud platform's other services
   (networking, storage, identity) do not belong in this reference directory.
4. Add one row to the table above, replacing the placeholder row.
5. Check every existing claim in `SKILL.md`'s "Universal concepts" section against this vendor's
   actual behavior before assuming it holds — correct that section explicitly if it doesn't (see
   `AGENTS.md` rule 4). The first vendor fills that section in; the second is the first real test of it.
6. Do NOT add vendor-specific procedure content to the top-level `SKILL.md` — see that file's own
   contribution note.
