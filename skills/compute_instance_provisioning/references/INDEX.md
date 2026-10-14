# Compute Instance Provisioning — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Amazon EC2 | `aws_ec2/` | Launch, read, start/stop/reboot, resize (change instance type), back up (volume snapshots or image), terminate | Only one platform is documented, so `SKILL.md`'s universal concepts are hedged. Instance lifecycle only; networks, security groups, volumes as their own objects, Auto Scaling, load balancers, and Spot/Reserved purchasing are out of scope. EC2 has no documented in-place revert to a snapshot |

## Adding a new vendor

1. Create `references/<vendor>/procedure.md` following the shape of an existing single-vendor
   capability (e.g. `skills/cmdb_asset_management/references/servicenow/procedure.md`) as a
   template: Common Sequences → Status vocabulary → Operations → Patterns → Known limitations → Tools →
   Verification checklist (`AGENTS.md` rule 12).
2. Add `endpoints.md` (wire-level calls) alongside it, if the platform is REST/API-driven — CLI-driven
   platforms keep commands inline in `procedure.md` instead (see `AGENTS.md` rule 6).
3. Keep this vendor's procedure scoped to the instance lifecycle. A cloud platform's other services
   (networking, storage, identity) do not belong in this reference directory.
4. Add one row to the table above.
5. Check every existing claim in `SKILL.md`'s "Universal concepts" section against this vendor's
   actual behavior before assuming it holds — correct that section explicitly if it doesn't (see
   `AGENTS.md` rule 4). Each added vendor re-tests those claims; a second vendor is the first real test of them.
6. Do NOT add vendor-specific procedure content to the top-level `SKILL.md` — see that file's own
   contribution note.
