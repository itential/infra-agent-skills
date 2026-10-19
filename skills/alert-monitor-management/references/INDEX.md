# Alert & Monitor Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full
step-by-step for creating a monitor/check and acknowledging/resolving an alert) plus wire-level
`endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Datadog | `datadog/` | Create a monitor (Monitors API v1); mute/acknowledge via a Downtime (Downtimes API v2) | Single monitor object carries both the condition and most notification options; suppression is a separate Downtime resource, not a field on the monitor — the older per-monitor mute/unmute calls are deprecated in favor of this |
| New Relic | `new-relic/` | Create an alert policy + NRQL alert condition (NerdGraph GraphQL API); acknowledge/resolve the resulting issue (NerdGraph AI Ops issue mutations) | NerdGraph is the current/recommended API; the older REST Alerts API (`alerts_*.json` endpoints) is being retired — see that vendor's procedure for the exact split still functional today |
| LogicMonitor | `logicmonitor/` | Import/define a DataSource (datapoint thresholds define the alerting condition) and add an Alert Rule (routes/escalates matched alerts); acknowledge an alert (REST API v3) | Two-object model: DataSource datapoint thresholds decide *whether* an alert fires, Alert Rules decide *who's told and how* — do not conflate the two when asked to "create a monitor" |
| Paessler PRTG | `paessler-prtg/` | Create a sensor (PRTG API v2, `POST /api/v2/experimental/devices/{id}/sensor`); acknowledge an alarm (PRTG API v2 `POST /api/v2/sensors/{id}/acknowledge`, or the older HTTP API's `acknowledgealarm.htm`) | PRTG ships two parallel APIs — the newer REST-style API v2 and the older parameter-based HTTP API; PRTG's own v1 HTTP API documentation states that creating brand-new objects from scratch isn't supported through it (clone a template object instead), which is why this skill's create-sensor step uses API v2 |
| Centreon | `centreon/` | Create a host and a service check (REST API v2) and generate-and-reload the poller configuration; acknowledge or cancel the acknowledgement of a host/service problem | On-premises behavior only (the create calls differ on Cloud). Creation is staged until the poller is reloaded, and a reload applies every pending change. No documented manual resolve; host acknowledgement body fields unverified |
| OP5 Monitor | `op5-monitor/` | Create a host and a service check (configuration REST API) and save the staged changes; acknowledge a host/service problem (external-command API) | Basic-auth REST; saving applies all staged changes. Acknowledgement removal is not covered by the sources. No documented manual resolve |
| Thruk | `thruk/` | Create/replace/change/delete host and service config objects and save, check, reload; acknowledge or remove the acknowledgement of a host/service problem (REST API) | Front end to a Naemon-compatible core; new objects need the generic create call, per-object config calls only overwrite. Staged changes are shared with other users. Response and error formats undocumented |

**Not in scope for this skill:** notification-channel/escalation-chain creation as a standalone
task, dashboards, log-pipeline configuration, and synthetic/browser-check script authoring — see
`SKILL.md`'s "Known limitations."

Centreon, OP5 Monitor and Thruk model a check as a service attached to a host and make configuration a staged change applied by a poller reload or save; the universal concepts still hold, since none of them documents a manual resolve and all clear on a healthy check result.
