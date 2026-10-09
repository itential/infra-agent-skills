# AOS-CX state-query bindings

Sources: [system](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_system), [interfaces](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_system-interfaces), [one interface](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_system-interfaces-interface-name), [VLANs](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_system-vlans), [query controls](https://developer.arubanetworks.com/aoscx/v10.13/docs/tips-and-tricks-with-aos-cx-rest), API v10.13, retrieved 2026-10-09.

Authenticated base: `https://<switch>/rest/v10.13`. The connection's session/CSRF handling is assumed already established.

| Read | Literal request | Relevant attributes |
|---|---|---|
| System | `GET /system` | `hostname`, `applied_hostname`, `platform_name`, `software_version`, `system_mac`, `vsf_status`. |
| Interface collection | `GET /system/interfaces` | Select returned identity/reference; expand only as needed. |
| One interface | `GET /system/interfaces/{Interface.name}` | `name`, `type`, `admin_state`, `link_state`, `link_speed`, `duplex`, `lldp_neighbors`. |
| VLAN collection | `GET /system/vlans` | `id`, `name`, `type`, `admin`, `oper_state`, `oper_state_reason`, `macs`. |
| Returned related resource | `GET <returned-same-target-resource-URI>` | The API's actual returned reference determines the resource path. |

`attributes` selects columns; `selector` accepts `configuration`, `status`, `statistics`, or `writable`; `depth` is a nonnegative integer and defaults to 1 in these API versions. `depth=2` expands the first collection references one level further. `filter` constrains records, and `count=true` requests count behavior. Interface path names containing slash characters require path-segment encoding, e.g. `1%2F1%2F1`.

Interface `link_speed` is bits per second. `admin_state` and `link_state` use `up`/`down`; `duplex` uses `half`/`full`. VSF `topology_type` uses `standalone`, `chain`, `ring`; split state uses `no_split`, `fragment_active`, `fragment_inactive`. These fields are observations, not a health score.

Documented responses: 200 JSON; 304 not modified; 400 bad request; 401 unauthorized; 403 forbidden; 404 not found; 500 internal error; 501 not implemented; 503 unavailable. The cited pages provide no stable per-error string catalogue or retry timing.

Security note: the full system response schema includes `snmp_communities`; it is not included in this procedure's selected reporting attributes.
