# Network Access Control Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Aruba ClearPass Policy Manager | `aruba-clearpass/` | Read/list, create, update (including block/release via status), replace, delete in the endpoint repository | OAuth2 bearer token; quarantine/release is a status change (Known/Unknown/Disabled), not a separate operation; no group assignment, session read, or policy authoring documented; status meanings come from a secondary summary of the admin guide |
