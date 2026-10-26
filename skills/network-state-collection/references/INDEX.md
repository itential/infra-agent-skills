# Network State Collection — Tool Index

| Tool | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS / Genie | [cisco-pyats/](cisco-pyats/procedure.md) | Parse command output, learn feature state, and compare saved network snapshots | Collection and comparison report observed data; they do not diagnose root causes or approve a network change. Needs a pyATS testbed or captured output. |
| IP Fabric | [ip-fabric/](ip-fabric/procedure.md) | Read discovered state from snapshots through table queries, compare two snapshots, optionally start a discovery snapshot | Observed data only. No native snapshot diff is documented in the sources read; comparison is by repeating the same query on both snapshots. |
| Forward Networks | [forward-networks/](forward-networks/procedure.md) | Read modeled state with NQE queries per snapshot, diff query results between two snapshots, list devices | Observed data only. Does not start collections or manage snapshots. |
| Arista CloudVision | [arista-cloudvision/](arista-cloudvision/procedure.md) | Read device inventory and events (current or time-bounded) from the Resource API | Read-only, REST. Reads current or time-bounded state, not saved snapshots; no comparison call, so compare by repeating the same read. Collection responses are streams and are complete only when the stream ends. Does not onboard devices or change anything. |
| Zabbix | [zabbix/](zabbix/procedure.md) | Read current host, monitoring-interface availability, and item state | Read-only JSON-RPC API; current state only, no snapshots or diff (save results to compare before/after). Problems, triggers, and event history are not covered. Interface reads must name fields explicitly because the full interface object can include SNMP credentials. |
| Auvik | [auvik/](auvik/procedure.md) | Read discovered devices, networks, interfaces, and components per tenant | Read-only REST API (v1); current discovered state only, no snapshots or diff (save results to compare before/after). Request-rate limits and IP-block behavior are unverified; a 403 may be a role fault or a block. Notes, audit, warranty, lifecycle, and backup reads are not covered. |
| Cisco ACI APIC | [cisco-aci/](cisco-aci/procedure.md) | Read live system nodes, endpoints, faults, or one managed object by distinguished name | Read-only, REST. Reads live state, not snapshots; paged reads are recomputed per page and are not a consistent snapshot. No comparison call. Read-only; no write operations. |

The platform reference contains its source citations, execution sequence, tools, and verification.
New platforms require their own procedure and a check of the router's shared claims.

Platforms that read current or time-bounded state keep no snapshot or diff. To compare, save the first result and repeat the same read with the same filters and time bounds.
