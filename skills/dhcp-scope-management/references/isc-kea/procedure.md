# ISC Kea — Subnet/Reservation Management Procedure (subnet_cmds + host_cmds hooks)

Manages DHCPv4 subnet ("scope") configuration and per-client reservations on ISC Kea, via the Kea
Control Agent's command API — specifically the `subnet_cmds` and `host_cmds` hook libraries, which
let a running `kea-dhcp4` process take these changes without a full config reload/restart. Coverage
here is DHCPv4-primary; the IPv6 command names exist and structurally mirror their IPv4
counterparts per the cited source, but are unverified beyond the cited source. Assumes an
authenticated (or otherwise permitted) HTTP client against a Kea Control Agent that has
`libdhcp_subnet_cmds.so` and `libdhcp_host_cmds.so` loaded on the target `kea-dhcp4` server is
already available. See `endpoints.md` for the literal command/response JSON. Citation: ISC Kea's
own upstream documentation source (`doc/sphinx/arm/{ctrl-channel,hooks-subnet-cmds,
hooks-host-cmds}.rst`, `kea` project, ISC GitLab, master branch, plus the rendered Kea 2.6.1
Administrator Reference Manual for Control Agent networking/auth details) — retrieved 2026-09-17.
The exact release this master-branch source corresponds to wasn't pinned to one version number;
treat command shapes as "current upstream Kea, approximately the 2.6/2.7 line" and re-verify
against the target deployment's actual Kea version before relying on them, especially given that
Kea's own subnet-ID auto-generation behavior is documented to have changed as recently as 2.6.0.

## Operational procedure

### Prerequisite: reaching the command API

Kea's command interface is a JSON envelope of `command` (required), an optional `service` array
naming which running daemon(s) should receive it (e.g. `dhcp4`), and an optional `arguments` map of
command-specific parameters. Every response carries a `result` code, a human-readable `text`, and an
optional `arguments` payload. `result` 0 means success; the same numeric result code does not mean
the same thing across every command in this API — for instance `reservation-get` uses `result: 0`
for both "found" and "not found" (distinguished by the `text`/`arguments` content, not the code),
while `reservation-get-page` uses `result: 3` specifically to signal "no more pages" — check the
per-command note below rather than assuming a single global meaning for any one result code. When
reached through the Kea Control Agent over HTTP, the command JSON is the POST body sent to the
Control Agent's root path, and the agent wraps the daemon's response in a one-element JSON array;
an authentication/authorization failure at the Control Agent layer itself returns a differently
shaped, unwrapped object instead of that array — don't parse every response assuming the array
wrapper is always present.

### Load the required hook libraries (one-time, per `kea-dhcp4` config)

`subnet_cmds` and `host_cmds` are optional hook libraries — the commands below only exist on a
`kea-dhcp4` process that has them loaded in its `hooks-libraries` configuration. If a command below
returns "unsupported," check that the relevant hook is actually loaded before assuming a syntax
error.

### Create a subnet (a "scope" in this skill's vocabulary)

1. Choose a subnet ID. As of Kea 2.6.0, IDs must be explicitly assigned by the caller — don't rely
   on Kea auto-generating one, and don't mix explicitly-chosen IDs with auto-generated ones in the
   same deployment, since the source specifically warns this risks collisions. IDs must be greater
   than zero and less than 4294967295.
2. Submit the subnet-add command with the subnet's CIDR, its chosen ID, and (typically) at least one
   pool range within that CIDR for Kea to actually lease from — a subnet with no pool is valid
   configuration but has nothing to hand out.
3. Set any subnet-scoped or pool-scoped options needed (e.g. routers, lease time) as part of the same
   create call.
4. Confirm success: result 0 and the response's echoed subnet entry matches the requested CIDR and
   ID.

### Update a subnet — full replace vs. partial (delta) update

- The plain subnet-update command **fully overwrites** the named subnet's configuration: any pool or
  option not included in the update payload is removed, not left alone. Use it only when the caller
  intends to replace the subnet's entire configuration, not to add one setting on top of what's
  already there.
- To change or add just part of a subnet's configuration without restating everything else, use the
  delta-add (to add/overwrite specific pools or options) or delta-del (to remove specific pools or
  options, identified by their own key — a pool by its pool-range string, an option by its name/code
  plus option space) commands instead.

### Delete a subnet

- **Stop and confirm with the operator before deleting a subnet that may have active leases.**
  Deleting the subnet's configuration object does not delete the leases or host reservations that
  were issued against it — those persist as orphaned records tied to a subnet ID that no longer has
  a configuration entry, which the source flags as a real risk if that same numeric ID gets reused
  by a later subnet-add.
- Consider whether outstanding leases/reservations under the subnet need to be cleaned up
  separately (via the lease/reservation management commands) before or after removing the subnet
  configuration — the subnet-delete command itself does not do this.

### Create a shared network (grouping multiple subnets under one broadcast domain)

1. Create the shared network, optionally defining its member subnets inline in the same call, or
2. Create subnets independently first, then attach an existing subnet to an existing shared network
   by referencing the subnet's ID and the network's name.
3. To remove a subnet from a shared network without deleting the subnet itself, detach it by name +
   ID — this demotes it back to a standalone subnet rather than deleting its configuration.
4. When deleting a shared network itself, decide explicitly whether its member subnets should be
   kept as standalone subnets (the default behavior) or deleted along with the network — the command
   supports both, controlled by an explicit parameter; **confirm with the operator before choosing
   the delete-subnets-too option**, since it is the more destructive of the two and not the default.

### Create a per-client lease reservation

1. Determine the target subnet's numeric ID (or use 0 for a reservation that isn't scoped to any one
   subnet — a "global" reservation).
2. Choose the identifying field the client will present: hardware/MAC address is the simplest case;
   Kea also supports matching by DUID, circuit ID, client ID, or flex-id.
3. Submit the reservation-add command with the subnet ID, the chosen identifier, and (if a specific
   address is being guaranteed rather than just identifying the client for other policy purposes) an
   IP address.
4. Confirm success: a plain confirmation text in the response (no structured echo of the created
   reservation is part of the documented success response for this command, per the source).
5. Note that adding a reservation this way requires the target `kea-dhcp4` to have a writable host
   reservation database backend configured — a deployment using only in-memory/config-file
   reservations can't accept new reservations through this command.

### Look up a reservation

- By address or by identifier within a known subnet: use reservation-get. Its "not found" case still
  returns result 0 — check the response text/arguments to distinguish found from not-found, not the
  result code alone.
- By identifier across every subnet (not scoped to one): use reservation-get-by-id — note this
  command specifically forbids supplying a subnet ID at all, unlike most of the other reservation
  commands where it's mandatory or optional.
- By address alone, or by hostname: dedicated by-address and by-hostname lookup commands exist for
  cases where the identifier type isn't known up front (hostname matching is documented as
  case-insensitive).
- For listing every reservation in a subnet: prefer the paginated form over the all-at-once form in
  any deployment where the number of reservations could be large — the source itself flags the
  all-at-once command as potentially disruptive at scale. The paginated form signals "no more
  results" using result 3, together with an empty result set — a different meaning for result 3 than
  its general "resource not found" sense elsewhere in this API, so don't treat it as an error
  condition when paging to the end.

### Update a reservation

- Like subnet-update, reservation-update is a full overwrite of the named reservation's fields —
  any field not included in the update payload is removed from the existing reservation, not left
  alone.

### Delete a reservation

- **Stop and confirm with the operator before deleting a reservation that a live client currently
  depends on for its assigned address.** Use the same identifying parameters as the lookup commands
  (by address, or by subnet ID + identifier) to target the specific reservation to remove.

## Patterns

- **Full-overwrite semantics apply to both subnet-update and reservation-update — treat every field
  omitted from an update payload as "will be removed," not "will be left alone."** Use the delta
  commands (subnet side only; no reservation-side delta commands are documented in the sources) when a
  partial change is actually intended.
- **Result codes are not uniformly interpreted across commands.** The same numeric code (0 or 3 in
  particular) carries a different practical meaning depending on which command returned it — check
  the per-command behavior described above rather than hard-coding a single "0 = success, 3 =
  missing" rule across this entire API.
- **Static reservations cannot be embedded inside a subnet-add/subnet-update payload.** Manage
  reservations through the separate `host_cmds` commands (or static configuration-file reservations,
  not covered here), never as a nested field on the subnet object itself.

## Known limitations

- DHCPv4-primary coverage — IPv6 command names (`subnet6-*`, IPv6-specific reservation nuances like
  prefix delegation) are unverified beyond the source's own statement that they
  structurally mirror the IPv4 commands; verify against Kea's own IPv6-specific documentation before
  relying on this file for a DHCPv6 deployment.
- Does not cover lease management directly (querying or expiring an active lease independent of its
  reservation/subnet configuration) — only the subnet/reservation configuration objects that
  determine what Kea *will* assign, not live lease state itself.
- Does not cover Kea's Configuration Backend (database-stored configuration, as opposed to the
  in-memory/file-based configuration these hook commands operate on) — if the target deployment uses
  a Configuration Backend, confirm whether these same commands still apply as documented, since that
  wasn't independently checked here.
- The exact Kea release line this procedure was verified against was not pinned to a specific
  version number (see the citation note above) — re-confirm command/field availability against the
  target deployment's actual `kea-dhcp4`/Control Agent version before relying on this procedure
  unmodified.

## Tools

| Operation | Description | Category |
|---|---|---|
| List Subnets | List every configured subnet with its ID and shared-network membership | DHCP |
| Get Subnet | Retrieve one subnet's configuration by ID or CIDR | DHCP |
| Add Subnet | Create a new subnet with a caller-chosen ID | DHCP |
| Update Subnet (full) | Replace a subnet's entire configuration | DHCP |
| Update Subnet (delta) | Add/overwrite or remove specific pools/options on a subnet without a full replace | DHCP |
| Delete Subnet | Remove a subnet's configuration — confirm with the operator first (see Known limitations) | DHCP |
| Add/Get/Delete Shared Network | Group subnets under one shared network, or attach/detach an existing subnet | DHCP |
| Add Reservation | Create a per-client reservation, matched by MAC/DUID/circuit-ID/client-ID/flex-id | DHCP |
| Get Reservation | Look up a reservation by address, by identifier, by hostname, or across all subnets by identifier | DHCP |
| Update Reservation | Replace an existing reservation's fields (full overwrite) | DHCP |
| Delete Reservation | Remove one or all reservations for a subnet or client — confirm with the operator first | DHCP |

## Verification checklist

- [ ] A caller-chosen subnet ID was used (not left to auto-generation) and confirmed unique before
      subnet-add
- [ ] subnet-update / reservation-update were used only when a full replace was actually intended;
      delta-add/delta-del used for a partial subnet change
- [ ] Result codes were interpreted per the specific command's own documented meaning, not a single
      global assumption (see Patterns)
- [ ] Any subnet or reservation deletion was confirmed with the operator first, and the fate of
      orphaned leases/reservations under a deleted subnet was considered
- [ ] Command/field availability was checked against the target deployment's actual Kea version
      rather than assumed from this procedure's citation alone
