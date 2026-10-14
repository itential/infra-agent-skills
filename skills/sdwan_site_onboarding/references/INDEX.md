# SD-WAN Site Onboarding — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step)
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Prisma SD-WAN | `prisma_sdwan/` | Find or create a site blueprint (site template), deploy branch sites from it, assign edge devices to device shells, confirm deployment and onboarding, remove a deployment (optional), release a device, delete a device shell, delete a site | Only one platform is documented, so `SKILL.md`'s universal concepts are hedged. Other platforms may not be blueprint-driven (template-based) at all, so re-check every universal concept when a second vendor is added. Deployment status values, the release bindings, and the effect of deleting a deployment are not fully documented and are marked in the procedure. Circuit-label removal is not supported. Data-center sites, snapshot import, FIPS mode, and variable editing are not covered |
