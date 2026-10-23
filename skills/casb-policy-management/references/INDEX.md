# CASB Policy Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Cloudflare One CASB | `cloudflare/` | Create/read/update/enable/disable/delete finding-triggered remediation and webhook policies. Automatic remediation exists only for Microsoft 365 and Google Workspace file and folder findings; other finding types support webhooks only. | Single platform documented. Needs a paid CASB plan; remediation needs a read-write integration. Policies here are triggered by findings. Not covered: access-control or standalone DLP policies (no such policy objects are documented). Read-call token permission, rate limits, and API error codes are undocumented and marked unknown in the vendor files. |
