# CASB Posture Assessment — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` — a read/report
path organized by assessment type (shadow-IT discovery, OAuth-grant risk, policy-violation events,
risk score, security/compliance findings, DLP content matches), not a linear CRUD sequence. The
assessment types offered differ by platform.

| Vendor / Platform | Directory | Assessment types covered | Notes |
|---|---|---|---|
| Cloudflare One CASB | `cloudflare/` | Posture findings (list, filter by severity/vendor/integration, finding-type explanation, affected assets with remediation status) and DLP content findings; diagnosis of stale or missing findings | Single platform documented. Read-only. Scopes: whole account, one integration, or one asset. No shadow-IT discovery, OAuth-grant, or app risk-score data is documented for this platform. Findings are as of the last scan (documented intervals conflict: 1 to 24 hours and 24 to 48 hours); free accounts cannot view instance details. Rate limits, page-size limits, and API error codes are undocumented and marked unknown in the vendor files. |
