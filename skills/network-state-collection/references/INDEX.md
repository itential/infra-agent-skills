# Network State Collection — Tool Index

| Tool | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS / Genie | [cisco-pyats/](cisco-pyats/procedure.md) | Parse command output, learn feature state, and compare saved network snapshots | Collection and comparison report observed data; they do not diagnose root causes or approve a network change. Needs a pyATS testbed or captured output. |
| IP Fabric | [ip-fabric/](ip-fabric/procedure.md) | Read discovered state from snapshots through table queries, compare two snapshots, optionally start a discovery snapshot | Observed data only. No native snapshot diff is documented in the sources read; comparison is by repeating the same query on both snapshots. |
| Forward Networks | [forward-networks/](forward-networks/procedure.md) | Read modeled state with NQE queries per snapshot, diff query results between two snapshots, list devices | Observed data only. Does not start collections or manage snapshots. |
| Zabbix | [zabbix/](zabbix/procedure.md) | Read current host, monitoring-interface availability, and item state | Read-only JSON-RPC API; current state only, no snapshots or diff (save results to compare before/after). Problems, triggers, and event history are not covered. Interface reads must name fields explicitly because the full interface object can include SNMP credentials. |

The platform reference contains its source citations, execution sequence, tools, and verification.
New platforms require their own procedure and a check of the router's shared claims.

Platforms that read current or time-bounded state keep no snapshot or diff. To compare, save the first result and repeat the same read with the same filters and time bounds.
