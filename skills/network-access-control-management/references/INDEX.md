# Network Access Control Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Aruba ClearPass Policy Manager | `aruba-clearpass/` | Read/list, create, update (including block/release via status), replace, delete in the endpoint repository | OAuth2 bearer token; quarantine/release is a status change (Known/Unknown/Disabled), not a separate operation; no group assignment, session read, or policy authoring documented; status meanings come from a secondary summary of the admin guide |
| Cisco Identity Services Engine (ISE) | `cisco-ise/` | **Read-only**: read endpoint records (by MAC or filtered list), read endpoint identity group, read live session state, session list and counters | Config API for endpoints plus separate monitoring API for sessions (internal-database accounts only); no writes, quarantine, release, session deletion, or policy-rule reads; endpoint and group field/filter names are marked unverified in the file. NAC object model, separate from any zero-trust access skill |

ISE has no write operation in this skill, so its procedure has no confirmation gates; any other platform's quarantine or delete steps keep theirs.
