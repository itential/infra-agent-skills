# Network Access Control Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Aruba ClearPass Policy Manager | `aruba-clearpass/` | Read/list, create, update (including block/release via status), replace, delete in the endpoint repository | OAuth2 bearer token; quarantine/release is a status change (Known/Unknown/Disabled), not a separate operation; no group assignment, session read, or policy authoring documented; status meanings come from a secondary summary of the admin guide |
| Cisco Identity Services Engine (ISE) | `cisco-ise/` | **Read-only**: read live session state by MAC, username, NAS IP, endpoint IP or audit session id; session list; session counters | Monitoring API only, internal-database admin accounts only. No endpoint-record or group reads (configuration-API resource and field names unverified), no writes, quarantine, release, session deletion, or policy-rule reads. NAC object model, separate from any zero-trust access skill |
