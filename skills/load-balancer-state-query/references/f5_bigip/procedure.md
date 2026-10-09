# BIG-IP configuration and state observations

Read BIG-IP TMSH v17 LTM virtual/pool/iRule data and platform/failover/synchronization observations.

Sources: F5 TMSH v17 manual [virtual](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_virtual.html), [pool](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html), [rule](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_rule.html), [version](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_version.html), [hardware](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_hardware.html), [failover](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_failover.html), [sync status](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_sync-status.html), retrieved 2026-10-09. Commands below run from the root TMSH context, with the intended partition/object names.

## Common Sequences

- LTM object evidence: Read virtual configuration → Read virtual state → Read selected pool configuration → Read pool state → Read referenced iRules if requested.
- Platform evidence: Read software and hardware → Read failover state → Read synchronization state.

### Read virtual configuration

`list ltm virtual` discovers accessible virtual servers. `list ltm virtual <virtual-name> all-properties` returns the selected object's configuration, including its pool/profiles/rules where configured. Success is the intended named object. The publisher describes forwarding virtual servers that need no pool; an absent pool is not universally a fault.

### Read virtual state

`show ltm virtual <virtual-name> all-properties` returns native status/statistics. Success is the observation for the intended object. The command can expose additional hardware-offload statistics on platforms that support them; absent platform-specific data is not zero. These sources do not prescribe universal connection, traffic or availability severity thresholds.

### Read selected pool configuration

For a pool named in the virtual configuration, `list ltm pool <pool-name> all-properties` exposes configuration, members and monitor relationships. Success is that pool's configuration. If the virtual has no configured pool, the virtual evidence completes without inventing a pool target. A configured priority-group minimum and a minimum-up-member action are separate settings; one is not substituted for the other.

### Read pool state

`show ltm pool <pool-name> detail` retrieves the pool and associated detail. Success is native status/statistics for the intended pool and returned members. The minimum-up-member action applies only when the corresponding checking feature is enabled. Uneven traffic or zero connections alone is not the documented proof of a failed member.

### Read referenced iRules

`list ltm rule <rule-name>` retrieves the named rule definition. `show ltm rule <rule-name>` retrieves supported rule statistics. Success is the selected definition/statistics, not a syntactic or security verdict. The procedure does not infer a memory leak from a string match or execute a rule editor.

### Read software and hardware

`show sys version detail` returns release, kernel and applied-hotfix information. `show sys hardware` returns platform hardware information. Success is the responding device's actual output.

### Read failover state

`show sys failover` returns the system's failover state and time in that state. The documented state vocabulary includes active, standby, offline and forced_offline. Success is the observed state; no role transition is requested.

### Read synchronization state

`show cm sync-status` returns the local device's configuration-synchronization state. Success is the native state output, not an assertion that another device or all application traffic is healthy.

For every read, these manual pages do not enumerate command-specific error strings. Permission, missing-object, unsupported-command or session failures remain failed observations with the native detail. The procedure does not turn them into empty successful inventories.

## Patterns

- Object properties and runtime statistics use different commands.
- No-pool virtual servers can be legitimate forwarding configurations.
- Failover role and configuration-synchronization state answer different questions.

## Known limitations

- The literal payloads are TMSH commands; the NetClaw pyATS REST-mapping wrapper is not assumed.
- Full GTM, APM, AFM, analytics, certificate and profile catalogues remain outside this subset.
- Log identifiers and diagnostic cause rules from the source were not verified by these manual pages and are not reproduced.
- No mutation, failover, counter reset or configuration load occurs here.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authenticated TMSH session | Run the documented read commands within the intended device/partition context | Read |

## Verification checklist

- Device, TMSH release, partition and selected object names are recorded.
- Configuration and runtime observations remain separately identified.
- Native status/errors and missing platform-specific fields are preserved.
- No unsupported diagnosis or universal capacity threshold is asserted.
