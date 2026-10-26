# Network State Collection — Tool Index

| Tool | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS / Genie | [cisco-pyats/](cisco-pyats/procedure.md) | Parse command output, learn feature state, and compare saved network snapshots | Collection and comparison report observed data; they do not diagnose root causes or approve a network change. Needs a pyATS testbed or captured output. |
| IP Fabric | [ip-fabric/](ip-fabric/procedure.md) | Read discovered state from snapshots through table queries, compare two snapshots, optionally start a discovery snapshot | Observed data only. No native snapshot diff is documented in the sources read; comparison is by repeating the same query on both snapshots. |
| Forward Networks | [forward-networks/](forward-networks/procedure.md) | Read modeled state with NQE queries per snapshot, diff query results between two snapshots, list devices | Observed data only. Does not start collections or manage snapshots. |
| Cisco ACI APIC | [cisco-aci/](cisco-aci/procedure.md) | Read live system nodes, endpoints, faults, or one managed object by distinguished name | Read-only, REST. Reads live state, not snapshots; paged reads are recomputed per page and are not a consistent snapshot. No comparison call. Does not create tenants or any other object. |

The platform reference contains its source citations, execution sequence, tools, and verification.
New platforms require their own procedure and a check of the router's shared claims.

Shared-concept note: with IP Fabric, Forward Networks, and Cisco ACI APIC listed (APIC reads live state rather than snapshots), the router no longer claims that volatile-field exclusions or parser support apply everywhere; those are stated as conditional, and coverage is described as varying by tool and platform.
