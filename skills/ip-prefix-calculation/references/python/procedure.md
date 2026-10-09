# Python IP prefix calculation

Calculate prefix properties with the standard-library ipaddress API.

## Common Sequences

- Describe a prefix: **Parse** → **Describe**.
- Test overlap/membership: **Parse** both inputs → **Compare**.
- Split an existing prefix: **Parse** → **Subdivide**.

### Parse

A network input is parsed in strict mode. Host bits in a network input raise a value error; an interface-address input instead uses the interface parser and its network property. Masking host bits is an explicit requested normalization, never a silent correction. Invalid addresses/masks remain errors; mixed address families remain incompatible for network operations.

### Describe

The network object supplies its version, prefix length, network boundary, masks and total address count. IPv6’s final numeric address is reported as a range boundary, not as an operational broadcast destination. Host enumeration follows the library’s family-specific rules: IPv4 /31 includes both addresses and /32 the sole address; IPv6 /127 includes both and /128 the sole address. Larger-network host iterators follow the publisher’s exclusions rather than a universal subtract-two rule.

Address classification comes from the library properties. Private/global meanings are version-sensitive; shared IPv4 space can be neither private nor global according to the module. A classification flag does not establish Internet reachability.

### Compare

The library tests address membership, network overlap, subnet and supernet relationships. The result is a boolean for the parsed values. Family incompatibility is reported as a type error rather than compared by string sorting.

### Subdivide

The requested longer prefix determines the subnet iterator. Exactly one prefix-change form is selected. A shorter or invalid split prefix is a value error. Output preserves all emitted prefixes or explicitly labels any preview as a preview; it is not an IPAM allocation.

## Patterns

An interface address can legitimately contain host bits; a strict network cannot. Integer totals are exact and do not require enumerating every address.

## Known limitations

The library’s address classification changed across Python releases; the runtime version is retained. Prefix splitting is deterministic; business VLSM placement, address-pool availability, and SLAAC deployment recommendations are outside scope.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Parse | Validate a network or interface value | Local computation |
| Describe/compare | Read properties and containment relationships | Local computation |
| Subdivide | Generate equal-sized prefixes | Local computation |

## Verification checklist

- Original input and any explicit normalization are retained.
- Address family, network boundary and exact total are reported.
- Host iterator semantics remain family-specific.
- A preview is not reported as the entire prefix set.

## Sources

- [Python ipaddress API (Python 3.14 documentation at retrieval)](https://docs.python.org/3/library/ipaddress.html). Retrieved 2026-10-09.
