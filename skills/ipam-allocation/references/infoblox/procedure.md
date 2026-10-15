# Infoblox NIOS — IPAM Network/Subnet and IP Allocation Procedure

Allocate network/subnet space and individual IP addresses in Infoblox NIOS IPAM via WAPI's
`next_available_network` (on `networkcontainer`) and `next_available_ip` (on `network`) functions.
This is a distinct capability from DNS record creation — see the separate `dns-record-management`
skill's Infoblox procedure for A/CNAME/PTR/NS/Fixed-Address record creation; this file covers only
network-container-to-network carve-out and IP reservation within an existing network. Assumes an
authenticated WAPI client against a NIOS Grid Master (network/networkcontainer create+read permission
on the target view) is already available. See `endpoints.md` for the literal request syntax behind
every operation named below.

## Operational procedure

### Common Sequences

**Carve a new subnet from an existing network container:**
1. Resolve the Network Container — locate it by network view / CIDR / extensible attribute filter.
2. Allocate the Next Available Network — pass the container's reference (or its raw CIDR) and the
   desired child CIDR size into the allocation function.
3. Confirm the returned network object's network/network view.

**Reserve the next available IP within an existing network (no fixed address/host record needed
yet):**
1. Allocate the Next Available IP directly against the known network's CIDR.

**Create a fixed address (or host record) using the next available IP, in one atomic call:**
1. Use the nested-function form (not the inline string-function shorthand) inside the
   fixed-address/host-record create body — see Allocate the Next Available IP below.

If a caller's ask doesn't match one of these shapes, use the individual capability sections directly.

### Resolve the Network Container

Look up the network container by network view, CIDR, or an extensible attribute filter. Confirm
success: the response is a non-empty result; each element's reference is what the next step needs to
target that specific container.

### Allocate the Next Available Network

Two equivalent mechanisms exist — use the inline string-function form for a single simple call, or the
atomic multi-operation form when the container lookup and the network creation need to happen
atomically (recommended — avoids a race where another allocation lands between the lookup and the
create).

**Inline string-function form**: pass the allocation function as the value of the new network's
`network` field, with three arguments — the container reference or raw CIDR, the network view, and the
requested child CIDR prefix length.

**Atomic multi-operation form** (resolve container + allocate in one call — use when avoiding a
lookup-then-allocate race matters): submit a multi-step request where the first step resolves the
container and captures its reference into a named state variable, and the second step's create
substitutes that state variable into the same string-function form used above. This closes the race
the two-call version has.

Direct function parameters (apply to either mechanism): a required CIDR (the child prefix length as
an integer), an optional quantity to return (default 1), and an optional list of networks to exclude
from consideration.

Confirm success: the response network object's network field shows a CIDR of the requested prefix
length, actually nested inside the container looked up in the first step.

### Allocate the Next Available IP

**Standalone reservation**: invoke the next-available-IP function against a known network, optionally
excluding specific addresses and/or requesting more than one.

**Nested-function form, for creating a fixed address or host record using the next available IP in
the same call** (use this when the goal is "reserve + assign" rather than "just reserve"): the target
object's address field is itself a nested function-call structure naming the source network and any
exclusions, resolved server-side into a real address as part of the same create call.

**Version note:** the exact field names used in the nested-function structure differ across WAPI
versions — confirm which your target Grid Master's WAPI version actually expects rather than assuming
one form works unmodified against every release.

Confirm success: the response's address field (or the containing object) reflects a real assigned
address, not the function-call structure echoed back unresolved.

## Patterns

- **Prefer the atomic multi-operation form when a lookup must inform the allocation.** A separate
  lookup-then-create is a real race condition — another allocation could land in the gap. The
  multi-operation request mechanism with state-variable substitution exists specifically to close that
  gap.
- **The nested-function form is for "allocate and use immediately," the plain inline string form is
  for "allocate now, decide what to do with it after."** Don't reach for the more complex nested form
  when the simple string form already does the job (e.g. a standalone reservation with no immediate
  fixed-address/host-record creation).
- **Field names for the nested function form are not stable across WAPI versions.** This is the kind of
  detail that silently breaks integration against an older Grid Master — always confirm against the
  target's actual WAPI version rather than copying an example verbatim from a different version's docs.

## Known limitations

- Covers the network container's next-available-network allocation and a network's next-available-IP
  allocation only — does not cover network *view* management, DHCP range/member configuration, network
  discovery, or deleting a network container (which has its own delete argument governing whether
  child objects are removed or reassigned — not detailed further here).
- Does not cover DNS record creation (A/CNAME/PTR/NS/Fixed-Address) — see the separate
  `dns-record-management` skill's Infoblox procedure for that capability; this file is IPAM-only.
- No documented atomic-allocation guarantee exists for the simple inline-function form used standalone
  (only the atomic multi-operation form closes the lookup-then-allocate race) — if concurrent
  allocation against the same container is a real risk in the target environment, prefer the
  multi-operation form.

## Tools

| Operation | Description | Category |
|---|---|---|
| Resolve Network Container | Look up a network container by view/CIDR/extensible attribute | IPAM |
| Allocate Next Available Network | Carve a child network of a given CIDR length from a container | IPAM |
| Atomic multi-operation allocation | Atomically resolve a container and allocate from it in one call | IPAM |
| Allocate Next Available IP | Reserve the next available IP within a network, optionally as part of creating a fixed address/host record | IPAM |

## Verification checklist

- [ ] The allocated network's CIDR was confirmed to actually nest inside the intended container, not
      just accepted on a success response
- [ ] Where a lookup informed the allocation, the atomic multi-operation form was used, or the race was
      otherwise deemed acceptable and documented
- [ ] The nested-function field names used were confirmed against the target Grid Master's actual WAPI
      version
- [ ] For a fixed-address/host-record allocation, the response's assigned IP was confirmed resolved to
      a real address, not the function-call structure echoed back unresolved
