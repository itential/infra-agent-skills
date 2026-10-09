# controller-data-query: platform references

| Platform | Procedure | Scope | Notes |
|---|---|---|---|
| Cisco Meraki | [cisco_meraki/procedure.md](cisco_meraki/procedure.md) | Discover and execute a read operation | Official Meraki MCP; beta catalogue |
| Cisco Catalyst Center | [cisco_catalyst_center/procedure.md](cisco_catalyst_center/procedure.md) | Discover and execute a read operation | Release-matched official MCP; server also exposes mutations |
| Arista CloudVision | [arista_cloudvision/procedure.md](arista_cloudvision/procedure.md) | Native inventory, event and existing probe-statistics reads | REST Resource API stream handling; no workspace/tag mutations. |
| Cisco ACI APIC | [cisco_aci/procedure.md](cisco_aci/procedure.md) | Systems, endpoints, current faults and named-object reads | Native REST queries; recomputed pagination and source filter defects documented. |

Router correction: CloudVision uses documented native REST resources, so live MCP discovery is not a universal prerequisite. Each vendor reference supplies its own discovery or native query sequence.
