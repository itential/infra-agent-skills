# Cisco ISE — Wire-Level Reads

Source: Cisco DevNet, Cisco Identity Services Engine API v1 (developer.cisco.com/docs/identity-services-engine/latest/) —
Monitoring REST API introduction and session management calls; retrieved 2026-10-26. `<ise-host>` is a placeholder. All calls are GET.

Endpoint-record and endpoint identity group reads through the configuration (ERS) API are not
bound: the resource names, filter fields and record fields could not be confirmed against Cisco's
reference. Unverified, so no route is listed.

## Monitoring API (MnT)

Base: `https://<ise-host>/admin/API/mnt/`. Internal-database accounts only. Basic authentication. XML by default
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

Error strings and status codes: not documented.
