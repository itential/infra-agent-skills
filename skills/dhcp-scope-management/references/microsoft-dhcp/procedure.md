# Microsoft Windows Server DHCP Server — Scope and Reservation Management Procedure

Manages IPv4 DHCP scope configuration and per-client lease reservations on Windows Server's DHCP
Server role, via the `DhcpServer` PowerShell module. This is a CLI/cmdlet-driven procedure, not a
REST API — per this repo's own convention for CLI-driven procedures, the literal cmdlet syntax is
kept inline below rather than split into a separate `endpoints.md`. Coverage here is IPv4-only
(the `*Dhcpv4*` cmdlet family); IPv6 scope management exists as a parallel `*Dhcpv6*` cmdlet family
that was not researched for this draft. Assumes a PowerShell session with the `DhcpServer` module
available and sufficient rights against the target DHCP server (local or via `-ComputerName`/CIM
session) is already in place. Citation: Microsoft Learn's `DhcpServer` PowerShell module reference
(`windowsserver2025-ps` moniker, Microsoft's own first-party documentation), retrieved 2026-09-17.
Older Windows Server versions (2016/2019/2022) have their own parallel doc pages; this procedure was
not independently diffed against those for behavioral differences — if targeting an older OS
version, spot-check the corresponding version-specific page before assuming identical behavior.

## Operational procedure

### Create a scope

1. Decide the scope's address range (start and end address) and its subnet mask — these three
   values are mandatory and together define the scope's boundaries; a name is also mandatory.
2. Run the scope-creation cmdlet with those mandatory values, plus `-ComputerName` if targeting a
   remote DHCP server (omitted targets the local server).
3. Decide whether the scope should come up active immediately or created inactive first — the
   default is active, meaning it starts responding to client requests as soon as it's created; set
   it inactive explicitly if that's not yet wanted (e.g. staging before a cutover).
4. Set an explicit lease duration if the platform default (8 days) isn't what's wanted for this
   scope.
5. If this scope is meant to belong to a superscope (a logical grouping of scopes, typically for a
   single physical subnet carrying more than one logical IP range), name that superscope as part of
   the same create call.
6. By default the cmdlet produces no output on success — request the created scope object back
   explicitly if the caller needs to inspect or chain off of it.
7. Confirm success: either the explicitly requested output object reflects the intended range/name/
   mask, or (if no output was requested) a separate lookup of the scope by its ID confirms the same.

```powershell
Add-DhcpServerv4Scope -ComputerName "dhcpserver.contoso.com" `
    -Name "Building3-VLAN20" -StartRange 10.20.20.10 -EndRange 10.20.20.240 `
    -SubnetMask 255.255.255.0 -LeaseDuration 4.00:00:00 -State Active -PassThru
```

### Update an existing scope

- Target the scope by its scope ID (the network address that identifies it, e.g. `10.20.20.0`) and
  supply only the fields being changed — this cmdlet changes named fields individually rather than
  requiring the full scope to be restated.
- Changing the scope's address range specifically requires supplying both the new start and end
  address together in the same call — the platform's own documentation notes that setting a new
  range this way discards the scope's previously configured range entirely, so confirm the full
  intended new range before issuing this form rather than assuming a partial range change is
  possible.

```powershell
Set-DhcpServerv4Scope -ComputerName "dhcpserver.contoso.com" -ScopeId 10.20.20.0 `
    -Name "Building3-VLAN20-renamed" -LeaseDuration 2.00:00:00
```

### Delete a scope

- **Stop and confirm with the operator before deleting a scope that may currently have active
  client leases.** By default, deleting a scope that is active or that has active leases is
  documented to be blocked/require confirmation; an explicit override flag exists specifically to
  force deletion through that state. The exact wording of the platform's own default (non-override)
  blocking behavior was not found spelled out verbatim in the fetched documentation — treat the
  presence of that override flag as confirmation that the default path is meant to protect against
  exactly this case, and always get explicit operator confirmation before using the override on a
  scope that might still be in active use, rather than assuming it's safe because the override
  exists.
- The delete cmdlet accepts more than one scope ID in a single call, and can be fed scopes
  pipelined from a lookup/filter of existing scopes (e.g. "every currently inactive scope") rather
  than only literal IDs typed by hand.

```powershell
# Confirm with the operator first if any of these scopes might have active leases.
Remove-DhcpServerv4Scope -ComputerName "dhcpserver.contoso.com" -ScopeId 10.20.20.0
```

### Read scope configuration

- Look up a specific scope by its ID, or omit the ID to retrieve every scope configured on the
  target server.

```powershell
Get-DhcpServerv4Scope -ComputerName "dhcpserver.contoso.com" -ScopeId 10.20.20.0
```

### Create a lease reservation for a specific client

1. Identify the target scope (by its scope ID) and the client identifier that will be reserved
   against — for a Windows client this is its MAC address; the platform accepts an arbitrary
   client-identifier string more generally.
2. Either supply a specific address to reserve, or first look up a currently-free address within
   the scope and reserve that address in a second, separate call — the platform's own examples show
   both patterns, including reserving directly against a value already known (a fixed address, or
   the address/identifier pulled from an existing active lease, effectively promoting that lease to
   a standing reservation). The free-address-then-reserve pattern is two separate calls, not one
   atomic operation — the platform's documentation does not itself call out a race between the two
   steps, but treat the possibility of another client claiming that same free address in between as
   a real risk worth checking for (e.g. re-verifying the address is still unused) rather than
   assuming the two-step sequence is safe by construction.
3. Confirm success: the reservation object reflects the intended scope, address, and client
   identifier — by default this cmdlet also produces no output, so request it explicitly if the
   caller needs to inspect the result inline.

```powershell
# Reserve a specific, already-known address.
Add-DhcpServerv4Reservation -ComputerName "dhcpserver.contoso.com" -ScopeId 10.20.20.0 `
    -IPAddress 10.20.20.15 -ClientId "F0-DE-F1-7A-00-5E" -Description "Reservation for printer"

# Reserve the next free address in the scope instead of a caller-chosen one.
$FreeIP = Get-DhcpServerv4FreeIPAddress -ComputerName "dhcpserver.contoso.com" -ScopeId 10.20.20.0
Add-DhcpServerv4Reservation -ComputerName "dhcpserver.contoso.com" -ScopeId 10.20.20.0 `
    -IPAddress $FreeIP -ClientId "F0-DE-F1-7A-00-5E" -Description "Reservation for printer"

# Promote an existing active lease to a standing reservation.
Get-DhcpServerv4Lease -ComputerName "dhcpserver.contoso.com" -IPAddress 10.20.20.31 |
    Add-DhcpServerv4Reservation -ComputerName "dhcpserver.contoso.com"
```

### Delete a reservation

- **Stop and confirm with the operator before deleting a reservation a live client currently
  depends on for its assigned address.** Target the removal either by the specific reserved
  address(es), by client identifier(s) within a named scope, or by scope alone — targeting by scope
  alone removes every reservation in that scope, not just one, so confirm that's actually the intent
  before using that form.
- Unlike scope deletion, no explicit force/override flag was found documented on the reservation
  deletion cmdlet — flag this asymmetry rather than assuming one exists by analogy to the scope
  cmdlet.

```powershell
# Delete one specific reservation by address — confirm with the operator first.
Remove-DhcpServerv4Reservation -ComputerName "dhcpserver.contoso.com" -IPAddress 10.20.20.15

# Delete every reservation in a scope — confirm with the operator first, since this is broader
# than deleting one reservation.
Remove-DhcpServerv4Reservation -ComputerName "dhcpserver.contoso.com" -ScopeId 10.20.20.0
```

## Patterns

- **Scope creation and scope update share almost the same field set, but update only changes what's
  explicitly supplied — it is not a full-replace the way ISC Kea's `subnet4-update` is (see
  `../isc-kea/procedure.md`).** Don't port a "full overwrite" assumption from the Kea procedure onto
  this platform.
- **Reserving the next free address is a look-up-then-reserve pattern, not an atomic allocate.**
  Treat the gap between the lookup and the reservation call as a real, if undocumented, race window
  — see the reservation-creation step above.
- **Most of these cmdlets produce no output by default.** Request `-PassThru` (or a separate `Get-`
  lookup) whenever the caller needs to confirm the resulting state rather than assuming success from
  the absence of an error alone.

## Known limitations

- IPv4-only in this draft — the parallel `*Dhcpv6*` cmdlet family for IPv6 scope/reservation
  management was not researched here.
- Does not cover DHCP failover-partner relationship configuration between two Windows DHCP servers,
  DHCP policies (the separate policy-based-assignment feature referenced only in passing via the
  `-ActivatePolicies` parameter), or server-level (as opposed to per-scope) options.
- The exact default (non-`-Force`) behavior of scope deletion when the scope is active or has active
  leases was not found spelled out as an explicit sentence in the fetched documentation — only
  inferred from the existence and description of the `-Force` override. Treat the operator
  confirmation gate above as required regardless of what the undocumented default actually does.
- One inconsistency was found directly in Microsoft's own reservation-cmdlet documentation: the
  `-Type` parameter's default value is described in one place as "None" and in another, on the same
  page, as "Both" — flagged here as a defect in the source rather than silently resolved; confirm
  actual default behavior empirically against a target server if the scope's client-type restriction
  matters for a given deployment, rather than trusting either stated default outright.
- This procedure was verified against the `windowsserver2025-ps` documentation moniker specifically;
  it was not independently cross-checked against the 2016/2019/2022 moniker pages for behavioral
  drift on an older OS version.

## Tools

Each operation above is a `DhcpServer` PowerShell cmdlet invoked directly (or via `-ComputerName`/
CIM session against a remote DHCP server) — there is no separate wire-level API surface to extract,
per this repo's convention for CLI-driven procedures (see this file's own cmdlet syntax above).

## Verification checklist

- [ ] Scope creation supplied all three mandatory range/mask values together and the intended
      lease duration/state explicitly, rather than relying on defaults without checking them
- [ ] A scope-range update supplied both the new start and end address together, aware that doing
      so discards the scope's prior range entirely
- [ ] Any scope or reservation deletion was confirmed with the operator first, regardless of
      whether `-Force` was going to be used
- [ ] A "reserve the next free address" flow re-checked the address was still free immediately
      before reserving it, given the two-step, non-atomic nature of that pattern
- [ ] Cmdlet output was explicitly requested (`-PassThru` or a follow-up `Get-` lookup) wherever the
      result needed to be confirmed, rather than assuming success from a lack of error alone
