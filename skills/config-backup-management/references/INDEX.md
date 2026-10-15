# Config Backup Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Prisma SD-WAN (unified API) | `prisma-sdwan/` | Capture a site's configuration as a YAML file, check capture jobs, retrieve the file, list captures; redeploy a YAML file (new site or existing site by name; not a documented rollback), check and list redeploy jobs | A single implementation exists today, so `SKILL.md`'s universal concepts are hedged. Per-site only; device-level snapshot, Jinja site templates, and bulk site-template deployment are not covered. Job status values other than warning and failed, the exact exclusions from a capture, and the effect of a redeploy on an existing site are not stated in the sources and are marked in the procedure |
