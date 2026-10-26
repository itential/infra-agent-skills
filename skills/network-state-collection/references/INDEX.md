# Network State Collection — Tool Index

| Tool | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS / Genie | [cisco-pyats/](cisco-pyats/procedure.md) | Parse command output, learn feature state, and compare saved network snapshots | Collection and comparison report observed data; they do not diagnose root causes or approve a network change. Needs a pyATS testbed or captured output. |
| IP Fabric | [ip-fabric/](ip-fabric/procedure.md) | Read discovered state from snapshots through table queries, compare two snapshots, optionally start a discovery snapshot | Observed data only. No native snapshot diff is documented in the sources read; comparison is by repeating the same query on both snapshots. |
| Forward Networks | [forward-networks/](forward-networks/procedure.md) | Read modeled state with NQE queries per snapshot, diff query results between two snapshots, list devices | Observed data only. Does not start collections or manage snapshots. |
| Arista CloudVision | [arista-cloudvision/](arista-cloudvision/procedure.md) | Read device inventory and events (current or time-bounded) from the Resource API | Read-only, REST. Reads current or time-bounded state, not saved snapshots; no comparison call, so compare by repeating the same read. Collection responses are streams and are complete only when the stream ends. Does not onboard devices or change anything. |

The platform reference contains its source citations, execution sequence, tools, and verification.
New platforms require their own procedure and a check of the router's shared claims.

Shared-concept note: with IP Fabric, Forward Networks, and Arista CloudVision listed (CloudVision reads live or time-bounded state rather than snapshots), the router no longer claims that volatile-field exclusions or parser support apply everywhere; those are stated as conditional, and coverage is described as varying by tool and platform.
