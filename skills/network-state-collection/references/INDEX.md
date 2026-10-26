# Network State Collection — Tool Index

| Tool | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS / Genie | [cisco-pyats/](cisco-pyats/procedure.md) | Parse command output, learn feature state, and compare saved network snapshots | Collection and comparison report observed data; they do not diagnose root causes or approve a network change. Needs a pyATS testbed or captured output. |
| IP Fabric | [ip-fabric/](ip-fabric/procedure.md) | Read discovered state from snapshots through table queries, compare two snapshots, optionally start a discovery snapshot | Observed data only. No native snapshot diff is documented in the sources read; comparison is by repeating the same query on both snapshots. |
| Forward Networks | [forward-networks/](forward-networks/procedure.md) | Read modeled state with NQE queries per snapshot, diff query results between two snapshots, list devices | Observed data only. Does not start collections or manage snapshots. |
| Auvik | [auvik/](auvik/procedure.md) | Read discovered devices, networks, interfaces, and components per tenant | Read-only REST API (v1); current discovered state only, no snapshots or diff (save results to compare before/after). Request-rate limits and IP-block behavior are unverified; a 403 may be a role fault or a block. Notes, audit, warranty, lifecycle, and backup reads are not covered. |

The platform reference contains its source citations, execution sequence, tools, and verification.
New platforms require their own procedure and a check of the router's shared claims.

Shared-concept note: with IP Fabric and Forward Networks listed, the router no longer claims that volatile-field exclusions or parser support apply everywhere; those are stated as conditional, and coverage is described as varying by tool and platform.

Auvik keeps no snapshot to select or diff; its procedure reads current discovered state. The shared rules on snapshot comparability, empty results, and partial coverage apply to the platforms that keep snapshots, and to Auvik as current-state reads.
