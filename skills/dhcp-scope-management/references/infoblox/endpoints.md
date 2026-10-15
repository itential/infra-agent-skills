# Endpoint Wiring — Infoblox NIOS DHCP Range/Reservation Management

Literal WAPI calls behind each capability named in `procedure.md`. Base URL:
`https://<grid-master>/wapi/v2.13.7` (adjust to the target Grid Master's actual supported version —
see `procedure.md`'s citation note on version drift). Auth: Basic auth or session cookie against the
Grid Master, the same as `ipam-allocation`'s Infoblox endpoints.

## Create a Range

```
POST /range
{
  "start_addr": "10.20.30.10",
  "end_addr": "10.20.30.200",
  "network": "10.20.30.0/24",
  "network_view": "default",
  "server_association_type": "MEMBER",
  "member": {"_struct": "dhcpmember", "ipv4addr": "10.20.30.2"},
  "comment": "Example range"
}
```
`server_association_type` accepts `MEMBER`, `MS_SERVER`, `FAILOVER`, `MS_FAILOVER`, or `NONE`
(default). Response echoes the created object's `_ref` and requested fields, e.g.:
```json
{"_ref": "range/ZG5zLmJpbmRfY25h:10.20.30.10/10.20.30.200/default", "start_addr": "10.20.30.10",
"end_addr": "10.20.30.200", "network": "10.20.30.0/24"}
```

**Set range-scoped options** (part of the same create or update call): add an `options` array of
option structs, e.g. `{"name": "dhcp-lease-time", "num": 51, "value": "43200", "use_option": true}`.

**Exclude specific addresses within the range** (part of the same create or update call):
```json
"exclude": [
  {"start_addr": "10.20.30.50", "end_addr": "10.20.30.55", "comment": "reserved for future use"}
]
```

## Update a Range

```
PUT /range/<range-ref>
{ "end_addr": "10.20.30.250" }
```
Only the fields included in the body are changed; omitted fields keep their prior value (unlike
Kea's subnet4-update, which is a full overwrite — see `../isc-kea/procedure.md`).

## Delete a Range

**Stop and confirm with the operator before issuing this call — see `procedure.md`'s Delete step.**
```
DELETE /range/<range-ref>
```

## Create a Fixed Address

By MAC address (default `match_client`):
```
POST /fixedaddress
{
  "ipv4addr": "10.20.30.15",
  "mac": "AB:CD:00:11:22:33",
  "network_view": "default",
  "name": "printer-3f-201"
}
```

By client identifier:
```
POST /fixedaddress
{
  "ipv4addr": "10.20.30.16",
  "match_client": "CLIENT_ID",
  "dhcp_client_identifier": "01:ab:cd:00:11:22:33",
  "network_view": "default"
}
```

Using the next-available address within a network instead of a literal `ipv4addr` (same
function-family as `ipam-allocation/references/infoblox/endpoints.md`'s next-available-IP calls —
confirm the field-name set for the target WAPI version there):
```json
{
  "mac": "AB:CD:00:11:22:33",
  "ipv4addr": {
    "_object_function": "next_available_ip",
    "_object": "network",
    "_object_parameters": {"network": "10.20.30.0/24"},
    "_result_field": "ips",
    "_parameters": {}
  }
}
```

Response reflects the resolved address, e.g.:
```json
{"_ref": "fixedaddress/ZG5zLmJpbmRfY25h:10.20.30.15/default", "ipv4addr": "10.20.30.15", "mac":
"ab:cd:00:11:22:33"}
```

## Update a Fixed Address

```
PUT /fixedaddress/<fixedaddress-ref>
{ "name": "printer-3f-201-relocated" }
```

## Delete a Fixed Address

**Stop and confirm with the operator before issuing this call — see `procedure.md`'s Delete step.**
```
DELETE /fixedaddress/<fixedaddress-ref>
```
