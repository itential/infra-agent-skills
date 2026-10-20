# Endpoint Wiring — Fortinet FortiManager Firewall Policy Management

Citations (docs.fortinet.com, retrieved 2026-10-19):
- Fortinet, "FortiManager 7.6.0 API Best Practices: Getting started" (auth methods, workspace URLs).
- Fortinet, "FortiManager 8.0.0 API Best Practices: Best Practices" (sessions, task polling, limits).
- Fortinet, FortiManager 7.6.0 New Features, "API enhancement to support install preview in the
  response for multiple devices" (preview request/response, result path).
- Fortinet, FortiManager 7.4.0 New Features, "Partial install pushes only the instructed
  configuration (JSON API) 7.4.1" (partial install request/response).

Object, policy and package paths marked *(assets)* come from the curated spec/README in
itential/assets (`Fortinet/FortiManager`), a secondary source; verify against the JSON API
reference for the target version.

Base: `POST https://<fortimanager-host>/jsonrpc`, one endpoint for everything. Body envelope:
`{"id": 1, "method": "<verb>", "params": [{"url": "<resource path>", "data": {...}}], "session": "<id>"}`.
Responses carry `result[].status` with `code` (0 = OK in vendor examples) and `message`, plus
`result[].url`; check it on every call.

## Authentication

| Mode | How | Notes |
|---|---|---|
| Session | `exec` on `sys/login/user` with admin credentials; the returned session id goes in the body `session` field | Admin needs "JSON API Access" enabled. Always log out (`sys/logout`, *path from general API convention, not on a page read*) — vendor says unreleased sessions fill the admin session limits |
| API token | Create a "Rest API Admin" with an admin profile, JSON API Access on, Read or Read-Write; send the generated key via the bearer authorization header | Key is permanent and users sharing it share one session. 7.2.2+ *(assets README)* |

Session caps are set by `system.admin.user.login-max` (per user) and `system.admin.setting.admin-max-login` (system-wide).

## Workspace-mode lock / commit / unlock

Vendor URL pattern, for ADOMs in workspace mode: `/dvmdb/adom/<adom>/workspace/lock`,
`/dvmdb/adom/<adom>/workspace/commit`, `/dvmdb/adom/<adom>/workspace/unlock`. Vendor guidance: lock
once, make all changes, commit once, unlock; each commit copies the database. The verb (`exec`)
and per-object lock variants were not confirmed on a page read.

## Objects and policies

| Capability | `method` | `params[].url` |
|---|---|---|
| Create address | `add` | `/pm/config/adom/<adom>/obj/firewall/address` *(assets)* |
| Read addresses | `get` | same *(assets)* |
| Update / delete address | `update` / `delete` | `/pm/config/adom/<adom>/obj/firewall/address/<name>` *(assumption: name-suffixed path; partial-install example uses `obj/firewall/address/Addr_1`)* |
| Read policy rules | `get` | `/pm/config/adom/<adom>/pkg/<package>/firewall/policy` *(assets)* |
| Create rule | `add` | same, `data` holds the rule *(assets)* |
| Update / delete rule | `update` / `delete` | `.../firewall/policy/<policyid>` *(assumption)* |

## Install and tasks

| Capability | `method` | `params[].url` |
|---|---|---|
| Install preview | `exec` | `/securityconsole/install/preview`; `data`: `adom`, `scope` list of `{oid, vdom_oid}` |
| Preview result | `exec` | `/securityconsole/preview/result` with the returned task id |
| Install package to device | `exec` | `/securityconsole/install/device` *(assets)*; a package-level path `/securityconsole/install/package` was not confirmed on a page read |
| Partial install (7.4.1+) | `exec` | `securityconsole/install/objects/v2`; `data`: `adom` (e.g. `"root"`), `objects` (entries like `["update", "obj/firewall/address/Addr_1", "", ""]`), `flags` (vendor example `0`) |
| Poll task | `get` | `/task/task/<id>` (vendor best-practices page; response fields not confirmed) |

Preview, install and partial install each return `result[0].data.task` (integer). Poll before
logging out: vendor warns an async task can be reported failed if its session ends first.
Concurrency depends on appliance resources; vendor says avoid tight polling loops and recommends
backoff retries on transient errors. Vendor lists HTTP 401, 403, 404, 500, 503 as codes to watch.

## Still unverified

Task response fields (percent, state, per-device history), update merge-vs-replace, rule field
names, NAT paths, exact lock verb, logout path. The executor should read the JSON API reference
for the target version (FNDN, `fndn.fortinet.net`) before relying on any of them.
