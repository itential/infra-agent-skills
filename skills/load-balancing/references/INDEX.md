# Load Balancing — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| F5 BIG-IP LTM | `f5-big-ip-ltm/` | Object-level iControl REST CRUD for `ltm virtual` (VIP) and `ltm pool`/pool members. | Grounded in F5 clouddocs' iControl REST API reference, which carries F5's own notice that it is community-contributed content not monitored by F5 — see the procedure's sourcing caveat. Does not cover AS3 declarative onboarding. Auth mechanism not independently confirmed. |
| Citrix ADC (NetScaler) | `citrix-adc/` | NITRO REST CRUD for `lbvserver` (VIP), `service` (pool-member equivalent), and `lbvserver_service_binding`. | Grounded in NetScaler developer docs (current-release/14.1 tree). Does not cover the `servicegroup` object/binding variant — flagged as an unconfirmed gap, not covered. Two documented auth mechanisms not fully reconciled with each other in the source — see `endpoints.md`. |
| HAProxy | `haproxy/` | Config-file `frontend`/`backend`/`server` block definition, plus Runtime API (stats socket) commands for live server state (drain/maintenance/weight) without reload. | CLI/config-driven — no `endpoints.md` (see `AGENTS.md` rule 6). Does not cover HAProxy's separate REST-based Data Plane API — its docs are a JS-rendered page that couldn't be retrieved as content in this research pass; flagged as a known gap for a future contribution. |
| Cloudflare Load Balancing | `cloudflare/` | REST CRUD for load balancers (hostname-based), pools with origins, and monitors; origin enable/disable; pool health and reference reads. | Hostname-identified, with no listener address. Does not cover custom `rules` (beta), Enterprise PoP steering, or Cloudflare DNS records. Delete behavior for in-use pools and the merge-vs-replace behavior of `origins` updates are undocumented in the sources used. |
