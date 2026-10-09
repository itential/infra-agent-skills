# VMware ESXi VM and snapshot inventory

Read registered VM identities and a selected VM’s snapshot tree on ESXi 8.x.

## 1. Resolve the VM

An already authorized ESXi shell/SSH session runs `vim-cmd vmsvc/getallvms`. The returned VM identifier is selected from the requested VM's row, together with its name and datastore configuration path. Connection or command failure ends lookup; no VM identifier is guessed.

## 2. Read snapshots

`vim-cmd vmsvc/snapshot.get VMID` uses that returned identifier. The result supplies the snapshot tree, including snapshot IDs, names, creation times and recorded snapshot state. A failed command is not proof of no snapshots. No create/remove/power operation follows from this read.

## 3. Report inventory

The result identifies the host, VM and returned tree. Published guidance notes that snapshot files may exist outside Snapshot Manager's inventory; an empty managed tree does not prove that no delta files exist.

## Patterns

A VM identifier is resolved on the host being queried. Recorded guest type or snapshot state does not prove current guest-OS health.

## Known limitations

Only the inspection portion of the cited procedures is included. SSH enablement, snapshot removal/consolidation and automatic age/severity policy are outside scope. ESXi is not treated as a generic Linux host.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authorized ESXi shell/SSH | Transport the two inspection commands | Hypervisor read |

## Verification checklist

- VM identifier comes from the selected host.
- Snapshot IDs and timestamps retain their native meaning.
- No mutation or automatic age-based deletion occurred.

## Sources

- [Broadcom ESXi 8 snapshot identification steps](https://knowledge.broadcom.com/external/article/419319). Retrieved 2026-10-09.
- [Broadcom snapshot visibility limitations](https://knowledge.broadcom.com/external/article?legacyId=1004343). Retrieved 2026-10-09.
