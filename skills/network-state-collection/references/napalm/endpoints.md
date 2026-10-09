# NAPALM normalized device reads: bindings

Python bindings:

- `from napalm import get_network_driver`; `driver = get_network_driver(driver_name)`.
- `device = driver(hostname=target, username=username, password=password, optional_args=verified_driver_options)`; `device.open()`; `device.close()` in cleanup.
- Selected reads: `device.get_facts()`, `get_interfaces()`, `get_interfaces_counters()`, `get_interfaces_ip()`, `get_environment()`, `get_lldp_neighbors()`, `get_lldp_neighbors_detail(interface='')`, `get_arp_table(vrf='')`, `get_bgp_neighbors()`, `get_route_to(destination='', protocol='', longer=False)`.

The support matrix selects the actual implemented subset. Driver construction or connection exceptions remain failures; `NotImplementedError` denotes missing method support. Credentials are supplied at runtime and are not embedded in fixtures. No call to `get_config()` or `get_bgp_config()` belongs to this read subset.

## Sources

- [NAPALM driver reference](https://napalm.readthedocs.io/en/latest/base.html). Retrieved 2026-10-09.
- [NAPALM support matrix](https://napalm.readthedocs.io/en/latest/support/index.html). Retrieved 2026-10-09.
- [NAPALM connection lifecycle example](https://napalm.readthedocs.io/en/latest/tutorials/changing_the_config.html). Retrieved 2026-10-09.
