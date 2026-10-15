# Cisco ASA — Firewall Policy Management Procedure

Manages network objects, extended access-list rules (and their application to an interface), and
static (auto) NAT on a Cisco ASA appliance. This procedure targets ASA specifically, not Cisco's
newer FTD/FMC (Firepower Management Center) platform — FMC's own REST API documentation could not be
reached from a public source during this research pass (its Quick Start Guide and reference pages
returned not-found from every path attempted), so FTD/FMC coverage is not included here; treat FTD/
FMC as a distinct, not-yet-covered platform rather than assuming this ASA procedure applies to it.
ASA itself supports both a CLI and a REST API; this procedure is written CLI-first because the CLI
syntax was directly confirmed against Cisco's public configuration guides for every operation below,
while the REST API's publicly-reachable documentation confirmed only its authentication model and a
single example resource (network objects) — see `endpoints.md` for exactly what was confirmed on the
REST side, and Known limitations for what wasn't. Assumes CLI access to the target ASA (console, SSH,
or an orchestration layer executing commands on your behalf) is already available.

## Operational procedure

### Create or update a network object

Enter object-definition mode for the object's name (creating it if new), then set exactly one
address-type subcommand appropriate to the object — a single host address, a subnet with its mask,
an address range, or a fully-qualified domain name — plus an optional free-text description.

```
object network <object-name>
  host <ip-address>
  subnet <ip-address> <mask>
  range <start-address> <end-address>
  fqdn [v4 | v6] <fully-qualified-domain-name>
  description <text>
```
(Set only the one address-type subcommand appropriate to this object — the block above lists every
observed variant, not one object's full field set.)

### Delete a network object

**Stop and confirm with the operator before proceeding.** Confirm the object isn't currently
referenced by an access-list entry or a NAT rule before removing it. Cisco's documentation available
for this pass specifically notes that for network-*service* objects/groups referenced by an ACL,
deleting the object clears its contents rather than fully removing its definition from the
configuration — that specific behavior was documented for network-service objects, not confirmed
equally for a plain network object of the host/subnet/range/fqdn kind above, so don't assume identical
behavior across both object kinds without checking the target ASA version's own documentation.

```
no object network <object-name>
```

### Add an extended access-list rule (access control entry)

Add an entry to a named extended access list, specifying permit or deny, the protocol, the source
address (and port where relevant), and the destination address (and port where relevant). An
optional `line <number>` places the entry at a specific position rather than appending it; `log`
enables logging for matches; `time-range` restricts the entry to a named time window; `inactive`
disables the entry without removing it.

```
access-list <acl-name> [line <line-number>] extended {deny | permit} {tcp | udp | icmp | ip} <source-address> [<source-port>] <destination-address> [<destination-port>] [log] [time-range <name>] [inactive]
```

Worked example (illustrative values, not a literal vendor quote): denying inbound HTTP from any
source to a specific host —
```
access-list ACL_INBOUND extended deny tcp any host 198.51.100.20 eq www
```

### Apply an access list to an interface

An access list has no effect on traffic until it is bound to an interface and a direction.

```
access-group <acl-name> {in | out} interface <interface-name>
```

### Remove an access-list entry

Cisco's documentation for this pass specifically states that the command used to remove an entry
must reproduce the exact same parameter string used to create it (or reference it by its `line`
number) — a partial or approximate match will not identify the entry to delete. Read the list first
(see Read below) to get the exact current parameter string or line number before attempting removal.

```
no access-list <acl-name> [line <line-number>] extended {deny | permit} {tcp | udp | icmp | ip} <source-address> [<source-port>] <destination-address> [<destination-port>] [log] [time-range <name>] [inactive]
```

**Stop and confirm with the operator before proceeding** — removing an access-list entry changes
what traffic that list permits or blocks, and can expose or block traffic that a different, now-first
-matching entry governs instead.

### Read (verify) access lists

```
show access-list [<acl-name>]
show running-config access-list [<acl-name>]
```
`show access-list` additionally reports each entry's line number and hit count, per Cisco's
documentation — useful both to confirm a new entry is in place and to get the exact current line
number/parameter string needed to remove a specific entry later.

### Configure static (auto) NAT on a network object

Static NAT for a given object is configured as a subcommand inside that object's own definition block
(this is what Cisco calls "network-object NAT" or "auto NAT"), not as a separate free-standing rule
table entry the way an ACL entry is. It translates the object's address to a specified mapped
address, optionally with port translation.

```
object network <object-name>
  nat [(<real-interface>,<mapped-interface>)] static <mapped-address> [service <real-port> <mapped-port>] [dns] [unidirectional] [inactive] [description <text>]
```
Field notes, per Cisco's documentation: `service` translates a specific port rather than the whole
address; `dns` rewrites DNS reply addresses to match the translation; `unidirectional` restricts
which side of the translation can initiate a new connection; `inactive` disables the NAT rule without
removing it; `description` is limited to 200 characters per the documentation for this pass.

### Remove static NAT from a network object

```
object network <object-name>
  no nat [(<real-interface>,<mapped-interface>)] static <mapped-address>
```

**Stop and confirm with the operator before proceeding**, and be aware of the caveat below: removing
or changing a NAT rule does not by itself clear translations already established under the old
mapping.

### Clear existing translations after a NAT change

Cisco's documentation for this pass specifically warns that changing a NAT configuration does not
clear currently active translations built under the previous mapping — they persist until they time
out on their own unless explicitly cleared. If the caller's intent requires the new NAT mapping to
take effect immediately for already-established connections, clear the translation table as its own
explicit step, called out to the operator before doing so since it can disrupt in-progress sessions:

```
clear xlate
```

## Patterns

- **NAT lives inside the object it translates, not in a separate rule list.** Unlike an ACL entry,
  which is an independent entry in a named list, static NAT for a given object is a subcommand nested
  inside that same `object network` block — read and modify it there, not via a separate NAT-specific
  top-level table.
- **Deleting an ACL entry requires reproducing it exactly (or its line number), not a partial
  description.** Always read the list first to get the authoritative current text or line number
  before attempting a removal.
- **A NAT change and its effect on already-open connections are two different things.** Changing or
  removing a NAT rule affects new connections going forward; existing translations persist until they
  time out or are explicitly cleared with `clear xlate`.

## Known limitations

- This procedure covers ASA, not Cisco's newer FTD/FMC platform — FMC's REST API documentation was
  not reachable from a public source during this pass. FTD/FMC needs its own research pass and its
  own reference file; don't apply this ASA procedure to an FTD/FMC-managed device.
- ASA's REST API was only confirmed for authentication basics and a single object-type example (see
  `endpoints.md`) — access-list and NAT REST resource paths were not found in the publicly reachable
  quick-start guide for this pass. Use the CLI operations above for access-list and NAT work until
  REST paths for those are independently confirmed.
- Whether ASA CLI configuration-mode commands apply to the running configuration immediately (before
  any save step) was not independently re-confirmed against a reachable page during this pass — this
  procedure assumes the common Cisco-platform pattern of immediate application to the running
  configuration, with a separate persist step (`write memory` / `copy running-config startup-config`)
  needed only to survive a reload; flagged here as not independently re-verified this pass rather than
  asserted as fully confirmed.
- Manual ("twice") NAT, address-group CRUD, and NAT on multiple objects/groups together are out of
  scope for this pass — only single-object static/auto NAT is covered.
- Cisco's product direction has been shifting new capability toward FTD/FMC; confirm ASA is genuinely
  the intended target platform, and that its REST/CLI surface for a specific ASA software version
  still matches what's described here, before relying on this procedure for a long-lived integration.

## Tools

| Operation | Description | Category |
|---|---|---|
| `object network` (host/subnet/range/fqdn, no object network) | Create, update, or delete a network object | Objects |
| `access-list ... extended` / `no access-list ...` | Add or remove an access-list rule | Access Rules |
| `access-group` | Bind an access list to an interface and direction | Access Rules |
| `show access-list` / `show running-config access-list` | Read access-list entries, including line numbers and hit counts | Access Rules |
| `object network` → `nat static` / `no nat static` | Configure or remove static (auto) NAT on an object | NAT |
| `clear xlate` | Clear existing address translations after a NAT change | NAT |

## Verification checklist

- [ ] The target platform was confirmed as ASA, not FTD/FMC, before following this procedure
- [ ] Delete of a network object or an access-list entry was preceded by a reference check and
      explicit operator confirmation
- [ ] An access-list entry's removal command reproduced its exact original parameter string, or used
      its current `line` number read fresh via `show access-list`, rather than an approximate match
- [ ] A new or modified access-list entry's effect on overall match order was considered, not just
      whether the entry itself was added correctly
- [ ] After a NAT change, whether `clear xlate` was needed for the caller's intent was explicitly
      considered and confirmed with the operator before running it
- [ ] `show access-list` / `show running-config` (or the equivalent object/NAT read) was used to
      confirm the resulting state after any write, not just the write command's own return status
