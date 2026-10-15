# Infoblox NIOS — DHCP Range and Reservation Management Procedure

Configures the DHCP service itself in Infoblox NIOS: creating/adjusting the address range a Grid
member (or Microsoft DHCP server under Grid management) actually leases from, and creating a
per-client fixed address so a specific device always gets the same lease. This is distinct from the
`ipam-allocation` skill's Infoblox procedure, which only reserves network/IP space as inventory —
carving a `network` object doesn't by itself make any address in it leasable; a `range` object (or a
`fixedaddress`) is what turns address-space inventory into something DHCP will actually hand out.
Assumes an authenticated WAPI client against a NIOS Grid Master (range/fixedaddress create+read
permission on the target view) is already available. See `endpoints.md` for literal WAPI request
syntax. Citation: NIOS WAPI object reference for `network`, `range`, and `fixedaddress`, retrieved via
a third-party WAPI-doc mirror (ipam.illinois.edu/wapidoc) on 2026-09-17, since Infoblox's own hosted
copy sits behind an authenticated Grid Master session — flagged as a secondary source per this
repo's sourcing rule; re-verify field names against the target Grid Master's actual WAPI version
before relying on them, since NIOS has changed nested-function field names across major WAPI
versions before (see `ipam-allocation/references/infoblox/procedure.md`'s own version note).

## Operational procedure

### Create a DHCP range (a "scope" in this skill's vocabulary) within an existing network

1. Confirm the target `network` object already exists (see `ipam-allocation` if it doesn't — a
   `range` must sit inside a network that's already been carved out).
2. Create the `range` object, supplying at minimum a start address, an end address, and the parent
   network. A range is enabled by default; nothing extra is required to make it live unless the
   deployment intentionally wants it created disabled first.
3. Decide which device actually serves the range: a Grid member, a Microsoft DHCP server under Grid
   management, or a failover association — set the association type and the matching member/server
   reference accordingly. Leaving this unset (or set to no-association) means the range exists as
   configuration but nothing is actively serving leases from it — confirm this is intentional before
   treating scope creation as "done."
4. Set any range-scoped DHCP options needed (lease time, boot server/file, DNS update behavior) —
   these override the parent network's own option values for addresses inside this specific range.
   If nothing is set, the range inherits the network's option values.
5. Confirm success: the created range's own start/end addresses and network reflect what was
   requested, and its assigned member/failover association is what was intended — a range with no
   real serving member attached is a common silent misconfiguration, not something the create
   response alone will flag as wrong.

### Exclude specific addresses from a range

- Addresses that fall inside a range's start/end bounds but must never be leased (e.g. addresses
  already fixed-address-assigned, or reserved for future static use) go in the range's exclusion
  list, not by shrinking the range's bounds — shrinking the bounds affects every address past the
  cut point, not just the ones meant to be excluded.

### Create a lease reservation for a specific client (fixed address)

1. Identify how the target client will be matched: by MAC address (the default and most common
   case), by a DHCP client identifier, or by relay-supplied circuit/remote ID — this choice
   determines which identifying field is required on the request.
2. Create the fixed-address object with the chosen identifying field, the network view, and either
   an explicit address or a request for the next available address within a named network (see
   `ipam-allocation`'s Infoblox procedure for the next-available-address mechanism itself — the
   underlying function is the same one used there, just invoked as part of creating this object
   instead of a bare reservation).
3. Confirm success: the response reflects a real assigned address tied to the identifying field
   submitted, not an unresolved function-call structure — the same caution as `ipam-allocation`'s
   Infoblox procedure documents for its own next-available-IP usage.

### Update a range or reservation

- Both objects support standard field updates against their own reference — change lease time,
  option values, exclusion list, or (for a range) its serving member/failover association by
  updating the relevant field(s) directly; there is no separate "modify" verb distinct from a normal
  update-by-reference call.

### Delete a range or reservation

- **Stop and confirm with the operator before deleting a range or fixed address that may be actively
  serving clients.** Deleting a range removes the scope configuration; any device currently leasing
  from within its bounds loses that lease's authoritative source going forward. Deleting a fixed
  address returns that address to the general pool the next time DHCP considers it, meaning another
  client could subsequently be leased the address the deleted reservation used to guarantee to one
  specific device.
- The Infoblox WAPI object reference used for this procedure did not spell out, for either object,
  whether an in-use range or fixed address can be deleted without an explicit override flag the way
  some other DHCP platforms require (see the Microsoft DHCP Server procedure's `-Force` requirement,
  by contrast) — treat this as an explicit unknown rather than assuming NIOS either blocks or allows
  it silently; confirm current behavior against the target Grid Master before relying on either
  assumption in an automated flow.

## Patterns

- **A `network`/`networkcontainer` object (address-space inventory) and a `range`/`fixedaddress`
  object (DHCP service configuration) are separate objects that happen to reference the same
  address space.** Allocating a network via `ipam-allocation`'s Infoblox procedure does not create
  any DHCP service for it — a `range` or `fixedaddress` object must be created separately before NIOS
  will actually lease anything from that network. Don't treat "the network exists" as "DHCP is
  configured for it."
- **Range-scoped options override network-scoped options for addresses inside that range only.**
  Set the option at whichever level actually needs the override, not both, to avoid values silently
  drifting apart during a future edit at just one level.
- **Excluding an address is not the same as shrinking a range.** Use the exclusion list for
  addresses that must never be leased from within an otherwise-intact range.

## Known limitations

- DHCP failover-pair configuration mechanics beyond the plain `server_association_type` enum
  (MEMBER, MS_SERVER, FAILOVER, MS_FAILOVER, NONE) were not researched in enough depth for this
  draft to describe failover-specific setup steps — consult platform-specific NIOS failover guidance
  before relying on this procedure for a failover deployment.
- Does not cover network *view* management, DHCP member/Grid topology configuration, or the
  network/networkcontainer allocation that must exist before a range can be created — see
  `ipam-allocation`'s Infoblox procedure for that.
- Whether NIOS permits deleting an in-use range/fixed address without an explicit override was not
  confirmed against current documentation — see the "Delete" step above; treat as an open question
  to verify against the target Grid Master rather than an assumed yes/no.
- Sourced from a third-party mirror of the WAPI object reference rather than Infoblox's own
  authenticated documentation portal — re-verify field names against the target Grid Master's actual
  WAPI version before automating against them, per the same caution `ipam-allocation`'s Infoblox
  procedure already gives for its own nested-function fields.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create Range | Create a DHCP address range (scope) inside an existing network, optionally with a serving member/failover association | DHCP |
| Update Range | Change a range's bounds, exclusions, options, or serving association | DHCP |
| Delete Range | Remove a DHCP range — confirm with the operator first (see Known limitations) | DHCP |
| Create Fixed Address | Create a per-client lease reservation, matched by MAC/client-ID/circuit-ID/remote-ID | DHCP |
| Update Fixed Address | Change a reservation's address, options, or matching identifier | DHCP |
| Delete Fixed Address | Remove a per-client reservation — confirm with the operator first (see Known limitations) | DHCP |

## Verification checklist

- [ ] The parent network for a new range was confirmed to already exist as address-space inventory
      before creating the range (see Patterns)
- [ ] A newly created range's serving member/failover association was confirmed set as intended, not
      left unassociated
- [ ] Exclusions were used for "never lease this address," not a shrunk range boundary, when only
      specific addresses needed to be withheld
- [ ] The matching identifier type used for a new fixed address (MAC/client-ID/circuit-ID/remote-ID)
      was confirmed to match what the actual client will present
- [ ] Any range or fixed-address deletion was confirmed with the operator first, given the unclear
      override behavior noted in Known limitations
- [ ] Field names used were checked against the target Grid Master's actual WAPI version rather than
      assumed from this procedure's citation alone
