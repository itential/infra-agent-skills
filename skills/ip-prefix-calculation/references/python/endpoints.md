# Python IP prefix calculation: bindings

Bindings use Python 3’s standard library; `cidr`, `address`, `other_cidr`, and `prefix` are supplied inputs, not evaluated code.

| Operation | Python binding | Result/error |
|---|---|---|
| Network | `ipaddress.ip_network(cidr, strict=True)` | Network; `ValueError` on malformed input or host bits |
| Interface | `ipaddress.ip_interface(cidr).network` | Parent network preserving interface-input meaning |
| Explicit normalize | `ipaddress.ip_network(cidr, strict=False)` | Network with host bits masked |
| Describe | `net.version`, `net.prefixlen`, `net.network_address`, `net.broadcast_address`, `net.netmask`, `net.hostmask`, `net.num_addresses` | Properties; IPv6 final address is not an IPv4-style broadcast |
| Classify | `ipaddress.ip_address(address).is_private`, `.is_global`, `.is_link_local`, `.is_multicast`, `.is_loopback`, `.is_reserved` | Booleans under installed Python semantics |
| Hosts | `net.hosts()` | Iterator with family/prefix-specific exclusions |
| Compare | `ipaddress.ip_address(address) in net`; `net.overlaps(other)`; `net.subnet_of(other)`; `net.supernet_of(other)` | Boolean; incompatible network methods raise `TypeError` |
| Split | `net.subnets(new_prefix=prefix)` | Iterator; `ValueError` for invalid prefix |

Version-specific constructors distinguish `AddressValueError` from `NetmaskValueError`. The factory functions may give less-specific `ValueError` diagnostics.


## Sources

- [Python ipaddress API (Python 3.14 documentation at retrieval)](https://docs.python.org/3/library/ipaddress.html). Retrieved 2026-10-09.
