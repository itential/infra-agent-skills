# Cisco ISE — Wire-Level Reads

Sources: Cisco DevNet, Cisco Identity Services Engine API v1 (developer.cisco.com/docs/identity-services-engine/latest/) —
API families, Read a Resource, Pagination, Monitoring REST API introduction, Session Management
calls; retrieved 2026-10-26. `<ise-host>` is a placeholder. All calls are GET.

## Configuration API (ERS)

Access: HTTPS on port 443; the documentation also lists 9060 for ERS (which one applies depends on
the deployment; unverified). Basic authentication. Idle session timeout is documented as 60 seconds.
Accept/Content-Type headers: not documented in the pages read; assumption: JSON or XML via `Accept`.

| Operation | Route | Notes |
|---|---|---|
| List resource | `/ers/config/{resource}` | Query: `filter=field.OP.value` (repeatable), `filtertype=or`, `size` (default 20, max 100), `page` (from 1), `sortasc`, `sortdsc`. Operators: EQ, NEQ, GT, LT, STARTSW, NSTARTSW, ENDSW, NENDSW, CONTAINS, NCONTAINS. Items carry name, id, description, link. |
| Read endpoint | `/ers/config/endpoint` (list) | Unverified: the `endpoint` resource name; filters `mac`, `groupId`, `profileId`, `staticGroupAssignment` (seen only in community sources) |
| Read endpoint by id / name | `/ers/config/endpoint/{id}`, `/ers/config/endpoint/name/{name}` | Unverified: both forms, from community sources |
| Read endpoint identity group | `/ers/config/endpointgroup/{id}` | Unverified: resource name |

Error strings and status codes for ERS: not documented in the pages read.

## Monitoring API (MnT)

Base: `https://<ise-host>/admin/API/mnt/`. Internal-database accounts only. XML by default
(`Accept: application/xml`). Case-sensitive paths. Backslash is the only invalid character.

| Operation | Route suffix | Response |
|---|---|---|
| Active count | `Session/ActiveCount` | `sessionCount` with `count` |
| Posture count | `Session/PostureCount` | same |
| Profiler count | `Session/ProfilerCount` | same |
| Active list | `Session/ActiveSessionsList` | user_name, calling_station_id, nas_ip_address, acct_session_id, audit_session_id, server, nas_ipv6_address, framed_ipv6_address |
| Auth list in window | `Session/AuthSessionsList/{starttime}/{endtime}` | same fields; `null` allowed for either bound |
| By MAC | `Session/MACAddress/{mac}` | full session attributes; MAC uppercase `XX:XX:XX:XX:XX:XX` |
| By username | `Session/UserName/{username}` | same |
| By NAS IP | `Session/IPAddress/{nas-ip}` | same |
| By endpoint IP | `Session/EndPointIPAddress/{endpoint-ip}` | same, with framed IP |
| By audit session id | `Session/Active/SessionID/{audit-session-id}/0` | session state, posture status, endpoint policy, counters |

Mutating calls in the same family (not used): `Session/Delete/MACAddress/{mac}`,
`Session/Delete/SessionID/{sid}`, `Session/Delete/All` (HTTP DELETE).
