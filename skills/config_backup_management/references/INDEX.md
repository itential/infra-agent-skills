# Config Backup Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Prisma SD-WAN (unified API) | `prisma_sdwan/` | Capture a site's configuration as a YAML file, check capture jobs, retrieve the file, list captures; redeploy a YAML file (new site or existing site by name; not a documented rollback), check and list redeploy jobs | A single implementation exists today, so `SKILL.md`'s universal concepts are hedged. Per-site only; device-level snapshot, Jinja site templates, and bulk site-template deployment are not covered. Job status values other than warning and failed, the exact exclusions from a capture, and the effect of a redeploy on an existing site are not stated in the sources and are marked in the procedure |

## Adding a new vendor

1. Create `references/<vendor>/procedure.md` following the shape of an existing single-vendor
   capability: Common Sequences → Status vocabulary → Operations (each with `Binds to:`) → Patterns →
   Known limitations → Tools → Verification checklist (`AGENTS.md` rule 12).
2. Add `endpoints.md` (wire-level calls) alongside it if the platform is REST/API-driven; CLI-driven
   platforms keep commands inline in `procedure.md` (`AGENTS.md` rule 6).
3. Add one row to the table above.
4. Check every claim in `SKILL.md`'s "Universal concepts" against the new vendor's behavior, and
   correct that section explicitly if it doesn't hold (`AGENTS.md` rule 4).
5. Do NOT add vendor-specific procedure content to `SKILL.md`.
