# Micetro — IPAM Address Block and IP Allocation Procedure

Find a free address block inside an existing Micetro range, optionally claim it for a short time, create
the range, and find the next free IP address in a range. IPAM address space only: DNS zones and records
and DHCP scopes in the same product belong to `dns-record-management` and `dhcp-scope-management`
and are never merged into this file. Assumes an authenticated tool for the Micetro REST API (session
or bearer-token authentication) is available to the calling agent. Each named operation maps to a call in
`endpoints.md`.

Sources: Micetro documentation, "REST API" user-manual page (docs.menandmice.com, 25.1, retrieved
2026-10-19), which gives the base-URL pattern and authentication options, and the product's public API
reference search listing for the available-address-blocks parameters. The remainder was taken from
Micetro's generated OpenAPI definition (version 2.0) as copied into the Itential `assets` repository,
a secondary source; those details are marked *(unverified)*. The vendor's detailed API reference page
could not be fetched.

## Operational procedure

### Common Sequences

**Allocate a new subnet from a parent range:**
1. List Available Address Blocks — in the parent range, with the wanted size (mask or address count).
   Ask for a temporary claim so another caller cannot take the block meanwhile.
2. Create Range — for the chosen block *(unverified: request body fields not confirmed)*.
3. Report the range reference and CIDR.

**Reserve the next free IP in a range:**
1. Get Next Free Address — in the given range. Optionally ask for a temporary claim.
2. Report the address and whether it was claimed.

### List Available Address Blocks

Return free blocks inside a range. Parameters: minimum size as a mask or as an address count (the mask
defaults to 24 when neither is given), a result limit, a flag to ignore the subnet flag when sizing, and
a temporary-claim duration in seconds that holds the returned blocks. Whether a claim is released
automatically on expiry and how a claimed block appears to other callers are not stated *(unverified)*.

### Create Range

Create a range from a range definition object; the definition is the only required body field, with
optional discovery settings and a save comment. Required fields inside the definition are not confirmed
*(unverified)*. Created ranges are persistent.

### Get Next Free Address

Return the next free address in a range. Optional inputs: start address, ping check, random choice,
exclude-DHCP, temporary-claim duration *(unverified: schema parameters only)*. Confirm success by an
address in the response; the exact response shape is not confirmed *(unverified)*.

## Patterns

- Availability results are computed. Without a temporary claim nothing is held.
- Removing a range or address record has a force-removal option; use only with explicit operator
  confirmation.

## Known limitations

- Deleting or changing an existing range or IP address record is outside this skill. Before any delete,
  overwrite or forced removal, stop and confirm with the operator.
- Error codes and strings, rate limits, claim-expiry behavior and exhaustion responses are not documented
  in the sources used — unknown.
- Does not cover DNS, DHCP reservations, address pools, or cloud/AD site mappings.

## Tools

| Operation | Description | Category |
|---|---|---|
| List Available Address Blocks | Free blocks in a range, optional temporary claim | IPAM |
| Create Range | Create a persistent range | IPAM |
| Get Next Free Address | Next free IP in a range, optional temporary claim | IPAM |

## Verification checklist

- [ ] The parent range reference and requested size were supplied before calling
- [ ] A returned block or address was recorded together with whether it was temporarily claimed
- [ ] The created range's reference and CIDR are in the final report
- [ ] Any failure was reported as a failure, not retried blindly
