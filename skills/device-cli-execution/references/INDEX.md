# Device CLI Execution — Platform Index

| Vendor / platform | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS / Unicon | [cisco_pyats/](cisco_pyats/procedure.md) | Execute approved CLI commands or apply an approved configuration through a device session | The caller supplies platform-documented commands and verification criteria. This is a transport procedure, not a generic configuration design or rollback recipe. |
| Cisco RADKit | [cisco_radkit/procedure.md](cisco_radkit/procedure.md) | Authorized remote-service command transport | Service discovery and publisher result/error handling |
| Netmiko | [netmiko/procedure.md](netmiko/procedure.md) | Read-only approved CLI commands | Host-key verification required; no configuration transfer |
| Juniper Junos | [juniper_junos/procedure.md](juniper_junos/procedure.md) | Operational CLI session and supplied read commands | No configuration mode or rollback recipe |

The platform reference contains its source citations, execution sequence, tools, and verification.
New platforms require their own procedure and a check of the router's shared claims.
