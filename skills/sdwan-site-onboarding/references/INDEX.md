# SD-WAN Site Onboarding — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step)
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Prisma SD-WAN | `prisma-sdwan/` | Find or create a site blueprint (site template), deploy branch sites from it, assign edge devices to device shells, confirm deployment and onboarding, remove a deployment (optional), release a device, delete a device shell, delete a site | Deployment status values, the release bindings, and the effect of deleting a deployment are not fully documented and are marked in the procedure. Circuit-label removal is not supported. Data-center sites, snapshot import, FIPS mode, and variable editing are not covered |
| Versa Director | `versa-director/` | Check prerequisites, create a branch device through the Director device workflow, activate it (global zero-touch, URL-based, command-line, USB, cloud-init), confirm it in inventory and task list, commit template changes | The unit is a device in an organization and device group, linked to a post-staging template, not a site deployed from a blueprint. Creating the organization, device group, or templates, removing or replacing a device, switch (SD-LAN) management, uCPE, and cloud-connector deployments are not covered. Workflow request schema, template-commit route, task routes, duplicate-name behavior, and whether a new device needs a post-activation commit are unverified and marked in the procedure |

Versa's equivalent of a site is a device linked to a device group and template, created before the hardware is activated, and its removal path is not documented, so the removal concept stays hedged.
