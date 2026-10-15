# SolarWinds IPAM — Subnet and IP Allocation Procedure (SWIS)

Allocate subnets and IP addresses in SolarWinds IP Address Manager (IPAM) via the **SWIS API**
(SolarWinds Information Service) — a SOAP/verb-invocation API, not REST, unlike every other vendor in
this category. Calls are made as `Invoke-SwisVerb` (PowerShell) or the equivalent SWIS verb-invocation
call in another SDK language (C#, Go, Perl, Java, per the Orion SDK), not as REST HTTP calls. Assumes an
authenticated SWIS connection to the target Orion/SWIS server (`Connect-Swis` or equivalent, with
appropriate IPAM permissions) is already available to the calling agent.

## Operational procedure

### Common Sequences

**Get the next available IP in a subnet, no reservation needed yet:**
1. `GetFirstAvailableIp` against the subnet.

**Reserve a specific IP for external provisioning, then confirm it once provisioning succeeds:**
1. `StartIpReservation` — reserves the address for a bounded time window (default 10 minutes).
2. Do the external provisioning work (e.g. configure the address on a device) within that window.
3. `FinishIpReservation` — commits the reservation with a final status. **If this isn't called before
   the reservation window expires, the reservation lapses on its own** — there is no indefinite hold.
4. If provisioning fails before finishing, `CancelIpReservation` explicitly rather than letting it
   silently time out — an explicit cancel is cleaner to audit than a lapsed reservation.

**Create a new subnet, optionally under a hierarchy group:**
1. `CreateSubnet` (flat) or `CreateSubnetForGroup` (nested under a named hierarchy group) — decide
   which based on whether the target IPAM instance organizes subnets into hierarchy groups.

### Get the First Available IP

```powershell
Invoke-SwisVerb $swis IPAM.SubnetManagement GetFirstAvailableIp @("<subnet-address>", "<cidr>")
```
Works for both IPv4 and IPv6 — the subnet address determines the family (e.g.
`@("199.10.1.0", "24")` vs. `@("1212::3", "24")`). An alternative,
`GetFirstAvailableIpViaFriendlyName`, accepts the subnet's friendly name instead of its raw
address/CIDR — use whichever the calling tool already has on hand rather than doing an extra lookup to
convert one to the other.

**Documented error condition:** "Error will be returned if non-existing subnet will be specified" —
confirm the subnet actually exists (or handle the error explicitly) rather than assuming any
address/CIDR pair resolves.

This call does **not** reserve the address — it's a read-only lookup. If the caller needs the address
held while external work happens, use the reservation flow instead, not this call followed by a delayed
create.

### Reserve an IP Address (bounded-time hold)

```powershell
Invoke-SwisVerb $swis IPAM.SubnetManagement StartIpReservation @("<subnet-address>", "<cidr>", <reservation-minutes>, "<address-to-start>")
```
Full signature: `StartIpReservation(subnetAddress, subnetCidr, reservationTimeInMinutes = 10,
addressToStart = "")`. `reservationTimeInMinutes` defaults to 10 if omitted — **this reservation is not
indefinite; plan the external work that must happen before `FinishIpReservation` to fit inside this
window**, or pass a longer explicit value if the work genuinely needs more time. `addressToStart` is
optional — omit it to let IPAM pick the starting point within the subnet, or supply it to bias toward a
specific address.

Then, once the address is actually in use (e.g. configured on a device):
```powershell
Invoke-SwisVerb $swis IPAM.SubnetManagement FinishIpReservation @("<reserved-ip-address>", "<final-status>")
```
`finalIpStatus` should be one of the documented `IPNode` status values: `Used`, `Available`,
`Reserved`, `Transient`, `Blocked`. Setting it to `Used` is the common case for "this address is now
actually assigned to something."

If the external work fails and the address should not be committed:
```powershell
Invoke-SwisVerb $swis IPAM.SubnetManagement CancelIpReservation @("<reserved-ip-address>")
```
**Prefer an explicit cancel over letting the reservation time out** — a lapsed reservation and an
explicitly cancelled one may look identical in status but an explicit cancel leaves an intentional
record of why the address didn't get used.

### Create a Subnet

```powershell
Invoke-SwisVerb $swis IPAM.SubnetManagement CreateSubnet @("<subnet-address>", "<cidr>")
```
or, to create it nested under an existing hierarchy group:
```powershell
Invoke-SwisVerb $swis IPAM.SubnetManagement CreateSubnetForGroup @("<subnet-address>", "<cidr>", "<hierarchy-group-name>")
```
Additional subnet properties (FriendlyName, Comments, VLAN, Location — per the `IPAM.Subnet` entity)
are not part of this basic creation call in the extracted source; if these need to be set at creation
time rather than via a follow-up update, confirm the exact verb/entity-update call against the current
SDK docs before assuming they can be passed inline here.

## Patterns

- **This is SOAP-style verb invocation, not REST — don't reach for HTTP-method conventions.** There's
  no GET/POST/PUT/DELETE distinction the way the other vendors in this category have; every operation is
  `Invoke-SwisVerb <connection> <namespace> <method> <positional-args>`, and read vs. write is determined
  by the specific verb's own documented behavior, not by an HTTP verb.
- **The reservation flow has a built-in expiry — this is the platform's version of a confirmation/commit
  gate.** Unlike NetBox/Infoblox's immediate allocate-and-done model, SolarWinds' reservation flow forces
  a two-step allocate-then-confirm with a time box in between. Treat `FinishIpReservation` as the actual
  commit point, and don't assume `StartIpReservation` alone means the address is allocated.
- **`GetFirstAvailableIp` is read-only — pairing it with a delayed, unreserved `CreateSubnet`/direct
  write introduces the same race the Infoblox atomic `/request` pattern exists to avoid.** If the target
  address must survive until something else finishes using it, use the reservation flow, not a bare
  lookup.

## Known limitations

- Covers `GetFirstAvailableIp`/`GetFirstAvailableIpViaFriendlyName`, the
  `StartIpReservation`/`FinishIpReservation`/`CancelIpReservation` flow, and
  `CreateSubnet`/`CreateSubnetForGroup` only — does not cover DHCP scope management, DNS integration,
  IPAM's own hierarchy-group management beyond referencing it by name, or Orion-platform-wide
  concerns (node/interface monitoring) outside IPAM itself.
- The reservation window (default 10 minutes, or an explicit override) is a real time constraint on the
  calling agent's own workflow — a reservation that lapses before `FinishIpReservation` is called simply
  expires; there's no documented notification/callback when that happens, so the calling workflow is
  responsible for tracking its own elapsed time against the window it requested.
- No documented error conditions were found for the reservation methods themselves (only for
  `GetFirstAvailableIp`'s non-existent-subnet case) — handle unexpected verb-invocation failures as a
  generic error, don't assume a specific error taxonomy exists for reservation-flow failures.

## Tools

| Operation | Description | Category |
|---|---|---|
| `IPAM.SubnetManagement.GetFirstAvailableIp` (or `...ViaFriendlyName`) | Read-only lookup of the next available IP in a subnet | IPAM |
| `IPAM.SubnetManagement.StartIpReservation` | Reserve an IP for a bounded time window | IPAM |
| `IPAM.SubnetManagement.FinishIpReservation` | Commit a reservation with a final status | IPAM |
| `IPAM.SubnetManagement.CancelIpReservation` | Explicitly release a reservation before it's finished | IPAM |
| `IPAM.SubnetManagement.CreateSubnet` / `CreateSubnetForGroup` | Create a new subnet, optionally nested under a hierarchy group | IPAM |

## Verification checklist

- [ ] `GetFirstAvailableIp`'s non-existent-subnet error condition was handled explicitly, not assumed
      away
- [ ] Any reservation was either finished or explicitly cancelled — never left to lapse silently when
      the calling workflow knew the address wouldn't be used
- [ ] The reservation window (default 10 minutes) was confirmed adequate for the external work planned
      between `StartIpReservation` and `FinishIpReservation`, or an explicit longer value was passed
- [ ] `FinishIpReservation`'s final status was one of the documented `IPNode` values (`Used`,
      `Available`, `Reserved`, `Transient`, `Blocked`), not an arbitrary string
