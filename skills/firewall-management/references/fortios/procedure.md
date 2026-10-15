# Fortinet FortiOS (FortiGate) — Firewall Policy Management Procedure

Manages firewall policies (rules), address objects, and destination-NAT virtual IP (VIP) objects on
a FortiGate device running FortiOS, via its command-line interface. This procedure is deliberately
CLI-driven rather than REST-driven: FortiOS does expose a REST/CMDB API, but its dedicated API
reference is published on Fortinet's developer network behind an account login, and could not be
independently verified against a publicly reachable page during this research pass — so this
procedure covers the CLI surface, which is documented in Fortinet's public CLI reference, instead.
If a REST integration is required, confirm the current REST API contract directly from Fortinet's
developer portal rather than assuming it matches the CLI syntax below field-for-field. Per this
capability's own convention for CLI-driven platforms, commands are kept inline below rather than
split into a separate endpoints file. Assumes CLI access to the target FortiGate (console, SSH, or an
orchestration layer that executes CLI commands on your behalf) is already available.

Every block below follows FortiOS's standard configuration-table shape: enter the table with
`config <table>`, select or create an entry with `edit <id-or-name>`, set fields with one or more
`set <field> <value>` lines, then close the entry with `next` (if more entries follow) and the table
with `end`.

## Operational procedure

### Create or update a firewall address object

Enter the address table, select the object by name (creating it if it doesn't already exist), and
set its type along with the fields that type requires: a subnet (IP and netmask) for a plain
IP/netmask object, a start/end IP pair for a range object, or a fully-qualified domain name for an
FQDN-type object. FortiOS documents additional address types (geography-based, dynamic, MAC-based)
that this pass didn't verify field-by-field — confirm the exact required fields for those types
against the target FortiOS version before using them. Optional fields include a display color, a
free-text comment, and one or more tags.

```
config firewall address
    edit "<object-name>"
        set type {ipmask | iprange | fqdn | geography | dynamic | mac}
        set subnet <ip> <netmask>
        set start-ip <ip>
        set end-ip <ip>
        set fqdn <fully-qualified-domain-name>
        set comment "<free-text comment>"
    next
end
```
(Set only the fields relevant to the chosen `type` — the block above lists every field name observed
across types, not a single object's full field set.)

### Read a firewall address object

```
show firewall address
show firewall address "<object-name>"
```
Use the unnamed form to list every configured address object, or name a specific object to see only
its own configuration.

### Delete a firewall address object

**Stop and confirm with the operator before proceeding** — an address object still referenced by a
policy or a NAT (VIP) rule should not be removed without first confirming nothing depends on it,
since FortiOS documentation available for this pass did not describe the address table itself
blocking deletion of an in-use object.

```
config firewall address
    delete "<object-name>"
end
```

### Create or update a firewall policy (rule)

Enter the policy table, select the policy by its numeric ID (creating a new one if the ID doesn't
exist), and set the fields that define its match/action behavior: source and destination interfaces,
source and destination address objects, the action (e.g. accept or deny), the applicable schedule,
and the service/port definition to match.

```
config firewall policy
    edit <policy-id>
        set srcintf <interface-name>
        set dstintf <interface-name>
        set srcaddr <address-object-name>
        set dstaddr <address-object-name>
        set action {accept | deny}
        set schedule <schedule-name>
        set service <service-object-name>
    next
end
```

### Read a firewall policy

```
show firewall policy
show firewall policy <policy-id>
```
As with address objects, the unnamed form lists every configured policy; naming a policy ID returns
only that one.

### Delete a firewall policy

**Stop and confirm with the operator before proceeding** — removing a policy changes which traffic
is permitted or denied, and can expose traffic that a later, lower-priority policy would otherwise
have blocked (or vice versa). Confirm the intended effect on traffic flow with the operator, and
confirm the policy's position relative to other policies if match order matters, before deleting.

```
config firewall policy
    delete <policy-id>
end
```

### Create or update a destination-NAT virtual IP (VIP) object

FortiOS's VIP table covers destination NAT / inbound port-forwarding style rules specifically — it
is not the mechanism for source NAT, which FortiOS configures separately at the policy level (a
policy's own NAT setting plus an IP pool) and which this pass did not verify in CLI-syntax detail;
treat source-NAT syntax as a separate, unconfirmed topic rather than assuming it follows the VIP
shape below.

```
config firewall vip
    edit "<vip-name>"
        set extip <external-ip-address>
        set mappedip <internal-ip-address>
        set extintf <interface-name>
        set portforward {enable | disable}
        set extport <external-port>
        set mappedport <internal-port>
    next
end
```

### Read a VIP object

```
show firewall vip
show firewall vip "<vip-name>"
```

### Delete a VIP object

**Stop and confirm with the operator before proceeding** — removing a VIP removes the inbound
NAT/port-forwarding path it defines; confirm nothing (a policy referencing this VIP as a destination)
still depends on it first.

```
config firewall vip
    delete "<vip-name>"
end
```

## Patterns

- **Every block follows the same edit/set/next/end shape regardless of table.** Learning the address,
  policy, and VIP tables' specific field sets is the only real per-object-type variation; the
  surrounding CRUD mechanics (select-or-create, set fields, close the entry, close the table) are
  identical across all three.
- **`show` with no name lists everything in that table; naming an entry filters to just it.** This
  is consistent across address, policy, and VIP tables and is the simplest way to confirm a specific
  object's current state after a write.
- **Whether a config-mode write applies immediately to the running configuration, or requires a
  separate save/commit step, was not independently confirmed during this research pass** — do not
  assume either behavior without confirming against the target FortiOS version's own documentation
  or observed device behavior, since this procedure's source material did not state this explicitly
  where it was checked.

## Known limitations

- REST/CMDB API detail (authentication, base path, request/response shapes) was not independently
  verified from a publicly reachable source during this pass — Fortinet's dedicated API reference is
  gated behind a developer-network login. This procedure is CLI-only until that gap is closed with a
  verified public or otherwise properly-sourced reference.
- Source NAT (SNAT/IP-pool) CLI syntax was not covered in this pass — only destination NAT via the
  VIP table is documented above.
- Address-group (`config firewall addrgrp`) and VIP-group CRUD are adjacent but out of scope for this
  pass — only single address objects and single VIP objects are covered.
- Whether FortiOS applies config-mode writes immediately or requires a separate persist/commit step
  was not confirmed this pass — see Patterns above.

## Tools

| Operation | Description | Category |
|---|---|---|
| `config firewall address` (edit/set/next/end, delete) | Create, update, or delete an address object | Objects |
| `show firewall address` | Read one or all address objects | Objects |
| `config firewall policy` (edit/set/next/end, delete) | Create, update, or delete a firewall policy | Policies |
| `show firewall policy` | Read one or all firewall policies | Policies |
| `config firewall vip` (edit/set/next/end, delete) | Create, update, or delete a destination-NAT VIP object | NAT |
| `show firewall vip` | Read one or all VIP objects | NAT |

## Verification checklist

- [ ] Address-object `type` and its type-specific required fields were confirmed before issuing a
      create/update, rather than assumed from a different type's field set
- [ ] Delete of an address object, policy, or VIP object was preceded by a check for existing
      references and by explicit operator confirmation
- [ ] A policy's position/match-order relative to other policies was considered before deleting or
      substantially changing it
- [ ] Read (`show ...`) was used to confirm the resulting state after any write, naming the specific
      object/policy/VIP rather than relying only on the write command's own return status
- [ ] No assumption was made about immediate-apply vs. separate-persist behavior without checking the
      target device/version, per the flagged gap in Known limitations
