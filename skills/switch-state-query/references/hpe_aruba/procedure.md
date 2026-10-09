# AOS-CX 10.13: collect switch state

Read selected switch, interface and VLAN records through the AOS-CX REST API.

Sources: HPE [system reference](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_system), [interface reference](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_system-interfaces-interface-name), [VLAN reference](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_system-vlans), and [REST query controls](https://developer.arubanetworks.com/aoscx/v10.13/docs/tips-and-tricks-with-aos-cx-rest), API 10.13 retrieved 2026-10-09. Bindings appear in [endpoints.md](endpoints.md).

## Common Sequences

- Switch identity: Read system → Report records.
- Interface/VLAN inspection: Read system → List requested resources → Read selected record → Report records.

## Read system

The query targets the authenticated switch using the supported API version and selects only the required attributes. Identity/software observations include configured and applied hostnames, platform, system MAC and running software version. The VSF status object, where returned, identifies topology and split state.

Success: the returned attributes describe the selected switch. Authentication/permission errors end the attempt. The full system schema includes SNMP community strings; indiscriminate full-response reporting can expose secrets. This procedure requests only the required state attributes.

## List requested resources

The interface or VLAN collection identifies actual resources. Query depth controls whether related records appear as references or expanded objects. The selector distinguishes configuration, status, statistics and writable attributes; selecting a category does not itself mutate it.

Success: collection records or their resource references are available. A body containing references is not a complete record inventory. Any filter/count-only selection is retained in the outcome.

## Read selected record

The resource returned by discovery is read with the requested attributes. Interface administrative state, physical link state, negotiated speed and duplex are reported separately. VLAN records distinguish administrative state, operational state and VLAN type. Related LLDP or MAC references can be followed using the URI actually returned by the switch, within the same approved target; a missing relationship is not an invented endpoint.

Success: the resource identity and expected attributes match the request. Not-found, unsupported-operation or invalid-request responses remain errors. A not-modified response contains no new body and is useful only with the corresponding validated cached record. Server/service errors leave state unknown; the selected reference provides no fixed retry interval.

## Report records

The report includes switch identity, API version, selected attributes, selector and expansion scope. Link speed uses the documented units. A down administrative setting differs from a failed observed link, and neither automatically establishes a root cause.

## Patterns

AOS-CX manages physical ports through interface resources. Physical interfaces are populated by the system and cannot be created or removed as ordinary configuration objects. Configured and applied hostnames can differ because an applied hostname may come from DHCP.

## Known limitations

Firmware image inventory, ISSU readiness/progress, optical diagnostics and VSF member-role details require their specific release/platform procedures. Generic NetClaw wrapper field names, error codes and fabricated upgrade-state examples are not API guarantees. This procedure performs no live changes.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read switch system | Retrieve selected identity/status attributes | REST query |
| List interfaces/VLANs | Discover resource identities and references | REST query |
| Read selected resource | Retrieve its state or documented related references | REST query |

## Verification checklist

- Target switch and API version match the request.
- Only requested attributes are reported; secrets remain excluded.
- References and expanded records are distinguished.
- Administrative and operational states retain their separate meanings.
- Native errors and cache/paging limits remain explicit.
