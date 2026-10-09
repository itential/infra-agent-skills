# Infoblox NIOS address-service collections

Read a bounded collection of DNS, IPv4 address-inventory or DHCP configuration records through NIOS WAPI.

## Common Sequences

- Inspect DNS records: **Establish client context → Read DNS collection → Report bounded evidence**.
- Inspect address inventory: **Establish client context → Read network collection → Report bounded evidence**.
- Inspect DHCP configuration: **Establish client context → Read range collection → Read fixed-address collection → Report bounded evidence**.

### Establish client context

The existing authorized client selects the requested NIOS Grid and supported WAPI version. The verified generated API files identify protocol 2.13.6, while the publisher README also lists newer client releases for protocol 2.14; those version lines are not silently mixed. The exact bindings and publisher source are in [endpoints.md](endpoints.md). Success requires compatible version selection and authorized HTTPS access. The official SDK defaults to disabling certificate verification; this unsafe default is explicitly identified here, and the supported verification/CA configuration is required for this binding. A certificate or authorization failure stops the read instead of bypassing verification.

### Read DNS collection

The selected record-list operation returns the requested DNS type with a caller-supplied result bound. Success is a decoded collection with record identities and the returned values. A, AAAA, alias, reverse-pointer and text records remain separate types; no record is synthesized from another. A truncated collection is not used to assert that a conflicting or reverse record does not exist. Unknown record types are outside this binding.

### Read network collection

The network-list operation returns bounded IPv4 network objects. Success is a decoded collection preserving network identity, address/view and any requested returned metadata. A stored network is inventory evidence; this read does not reserve an address or activate DHCP service.

### Read range collection

The range-list operation returns bounded IPv4 DHCP-range objects. Success preserves the returned bounds, network/view, enablement, exclusions, service association and available utilization/status fields. The publisher's utilization prose is ambiguous about which population its percentage represents; this procedure reports the native value and scale without deriving an exhaustion diagnosis or a free-address total.

### Read fixed-address collection

The fixed-address-list operation returns bounded reservation/configuration objects. Success preserves their identities and supplied address/client-match metadata. A stored fixed address is not a live lease or proof that a client received it. No matching identifier, network view or allocation is changed.

At each collection read, client transport errors, unsuccessful HTTP responses and decode errors are reported as failures with sanitized details. The generated client exposes generic failures rather than a complete endpoint-specific status catalogue; no exact error-code meaning is invented. Access failures require the authorized client to be corrected; rate-limit responses honor an available retry delay. Empty successfully decoded collections remain scoped empty results, distinct from failures.

### Report bounded evidence

The result records the selected collection, configured Grid/version, bound, returned identities and native field values. Success means that bounded read completed. No complete inventory or absence claim follows from a capped page; the verified generated models do not provide a complete pagination completion contract. A failed operation does not invalidate independently completed collections, but its missing coverage remains explicit.

## Patterns

- DNS records, network inventory, ranges and fixed addresses are separate object classes even when their addresses overlap.
- Configured state, DNS query answers and DHCP lease state require different evidence.
- The SDK's generated protocol label and its release compatibility matrix need an explicit version decision.

## Known limitations

No DNS/DHCP/IPAM writes, next-available allocation, zones, host records, IPv6 network/range inventory, live lease lookup, complete pagination, free-address computation or NetBox/Nautobot reconciliation. This primary-grounded subset does not re-verify or adopt the repository's separate legacy mutation references derived from a secondary WAPI mirror.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read DNS collection | List one supported DNS record type | Read |
| Read network collection | List IPv4 network inventory | Read |
| Read range collection | List IPv4 DHCP range configuration | Read |
| Read fixed-address collection | List IPv4 client reservation/configuration records | Read |

## Verification checklist

- Grid identity, authenticated scope, TLS verification and WAPI version were established.
- Every returned collection was decoded successfully; error responses were not called empty data.
- Record classes, object identities and native values remain distinguishable.
- Result bounds and incomplete coverage are explicit.
- No allocation, service change or live-health claim was made.
