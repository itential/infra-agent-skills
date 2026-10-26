# Zero Trust Access Policy Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full
step-by-step) plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Zscaler Internet Access (ZIA) | `zscaler-zia/` | Create/update/delete a URL/cloud-application filtering rule | Rules are evaluated in an explicit `order`; action vocabulary includes `ISOLATE` (cloud browser isolation), not just allow/block; a saved change is not enforced until a separate activation call, which is tenant-wide and may release other pending changes |
| Zscaler Private Access (ZPA) | `zscaler-zpa/` | Create/update/delete an access-policy rule (which users/groups may reach which application segments) under the `ACCESS_POLICY` policy set | Rule scope is expressed as a list of boolean `conditions`/operands, not flat fields; reordering is a separate dedicated endpoint from update |
| Netskope | `netskope/` | Create/update/delete a private-access (NPA) policy rule via REST API v2 | Update is a partial `PATCH`, not a full `PUT`; rule placement uses a `rule_order` directive (`top`/`bottom`/`before`/`after`) rather than a numeric field in the request body |

**Boundary with neighbouring capabilities:** network-layer firewall rule changes belong to
`firewall-management`, and SaaS/CASB inline data-control policy belongs to `casb-policy-management`;
this skill is for user/group-to-resource access rules on SASE/ZTNA platforms. (Zscaler ZIA firewall
filtering and Netskope real-time CASB rules are listed below as out of scope for that reason.)

**Not in scope for this skill:** ZIA firewall filtering / DLP / file-type-control rules, ZPA policy
set types other than access policy (timeout, client-forwarding, inspection, isolation), and Netskope
real-time (CASB inline), internet-access, and SaaS Posture Management policy families — see each
vendor's own `procedure.md` "Known limitations" for the precise boundary.

**Activation:** Zscaler ZIA stages every saved rule change until a separate activation step is run; activation is tenant-wide, is queued while other administrators still have unactivated edits, and cannot be cancelled once queued.
