# SD-WAN Site Onboarding — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step)
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Prisma SD-WAN | `prisma_sdwan/` | Find or create a site blueprint (site template), deploy branch sites from it, assign edge devices to device shells, confirm deployment and onboarding, remove a deployment (optional), release a device, delete a device shell, delete a site | Only one platform is documented, so `SKILL.md`'s universal concepts are hedged. Other platforms may not be blueprint-driven (template-based) at all, so re-check every universal concept when a second vendor is added. Deployment status values, the release bindings, and the effect of deleting a deployment are not fully documented and are marked in the procedure. Circuit-label removal is not supported. Data-center sites, snapshot import, FIPS mode, and variable editing are not covered |

## Adding a new vendor

1. Create `references/<vendor>/procedure.md` in the shape of an existing single-vendor capability:
   Common Sequences → Status vocabulary → Operations → Patterns → Known limitations → Tools →
   Verification checklist (`AGENTS.md` rule 12).
2. Add `endpoints.md` alongside it if the platform is REST/API-driven; CLI-driven platforms keep
   commands inline in `procedure.md` (`AGENTS.md` rule 6).
3. If this vendor also appears in `sdwan_policy_management`'s, `wireless_network_management`'s, or
   `vpn_tunnel_management`'s index, note it in the Notes column. Never merge reference files across
   skills.
4. Add one row to the table above.
5. Check every claim in `SKILL.md`'s "Universal concepts" against the new vendor's behavior and correct
   that section explicitly if one does not hold (`AGENTS.md` rule 4). A second vendor is the first
   real test of them.
6. Do not add vendor-specific procedure content to the top-level `SKILL.md`.
