# Endpoint Wiring — ISC Kea subnet_cmds / host_cmds

Literal Control Agent JSON commands behind each capability named in `procedure.md`. Wire mechanism:
`POST /` (root path) against the Kea Control Agent's configured `http-host`:`http-port` (default
`127.0.0.1:8000`), `Content-Type: application/json`, body = the command JSON below. The Control
Agent wraps the daemon's response in a one-element JSON array; an auth/authz failure at the Control
Agent itself returns an unwrapped `{"result": 403, "text": "Forbidden"}`-shaped object instead. If
`clients` authentication is configured on the Control Agent, send HTTP Basic auth credentials; if
TLS is configured, use HTTPS. Requires `libdhcp_subnet_cmds.so` and `libdhcp_host_cmds.so` loaded on
the target `kea-dhcp4` process.

## List Subnets

```json
{"command": "subnet4-list"}
```
Response `arguments.subnets`: array of `{id, shared-network-name, subnet}`.

## Get Subnet

By ID: `{"command": "subnet4-get", "arguments": {"id": 10}}`
By CIDR: `{"command": "subnet4-get", "arguments": {"subnet": "10.0.0.0/8"}}`

## Add Subnet

```json
{
    "command": "subnet4-add",
    "arguments": {
        "subnet4": [{
            "id": 123,
            "subnet": "10.20.30.0/24",
            "pools": [{"pool": "10.20.30.100-10.20.30.200"}],
            "option-data": [
                {"name": "routers", "data": "10.20.30.1"}
            ]
        }]
    }
}
```
Response: `{"result": 0, "text": "IPv4 subnet added", "arguments": {"subnet4": [...]}}`.

## Update Subnet (full replace)

```json
{
    "command": "subnet4-update",
    "arguments": {
        "subnet4": [{"id": 123, "subnet": "10.20.30.0/24", "pools": [...], "option-data": [...]}]
    }
}
```
Any pool/option not present in this payload is removed from the subnet.

## Update Subnet (delta — add/overwrite part of a subnet)

```json
{
    "command": "subnet4-delta-add",
    "arguments": {
        "subnet4": [{
            "id": 123,
            "subnet": "10.20.30.0/24",
            "option-data": [
                {"name": "routers", "code": 3, "space": "dhcp4", "csv-format": true,
                 "data": "10.20.30.1", "always-send": false}
            ],
            "pools": [{"pool": "10.20.30.201-10.20.30.210"}]
        }]
    }
}
```

## Update Subnet (delta — remove part of a subnet)

```json
{
    "command": "subnet4-delta-del",
    "arguments": {
        "subnet4": [{
            "id": 123,
            "subnet": "10.20.30.0/24",
            "option-data": [{"name": "routers"}],
            "pools": [{"pool": "10.20.30.201-10.20.30.210"}]
        }]
    }
}
```
Identify pools by their own `pool` range string and options by `name`/`code` + `space`, not by
position.

## Delete Subnet

**Stop and confirm with the operator before issuing this call — see `procedure.md`'s Delete step.**
```json
{"command": "subnet4-del", "arguments": {"id": 123}}
```
Does not remove leases or reservations tied to this subnet ID.

## Add Shared Network (optionally with member subnets inline)

```json
{
    "command": "network4-add",
    "arguments": {
        "shared-networks": [{
            "name": "floor13",
            "subnet4": [
                {"id": 100, "subnet": "192.0.2.0/24", "pools": [{"pool": "192.0.2.2-192.0.2.99"}],
                 "option-data": [{"name": "routers", "data": "192.0.2.1"}]}
            ]
        }]
    }
}
```

## Attach an Existing Subnet to a Shared Network

```json
{"command": "network4-subnet-add", "arguments": {"name": "floor13", "id": 5}}
```

## Detach a Subnet from a Shared Network (demotes it to standalone, does not delete it)

```json
{"command": "network4-subnet-del", "arguments": {"name": "floor13", "id": 5}}
```

## Delete Shared Network

**If using `subnets-action: delete`, stop and confirm with the operator first — this deletes the
member subnets themselves, not just the network grouping.**
```json
{"command": "network4-del", "arguments": {"name": "floor13", "subnets-action": "keep"}}
```
`subnets-action` accepts `keep` (default — demotes member subnets to standalone) or `delete`.

## Add Reservation

```json
{
    "command": "reservation-add",
    "arguments": {
        "reservation": {
            "subnet-id": 1,
            "hw-address": "1a:1b:1c:1d:1e:1f",
            "ip-address": "192.0.2.202"
        }
    }
}
```
Success: `{"result": 0, "text": "Host added."}`. Requires a writable `hosts-databases` backend
configured on the target `kea-dhcp4`.

## Get Reservation

By address: `{"command": "reservation-get", "arguments": {"subnet-id": 1, "ip-address":
"192.0.2.202"}}`
By identifier: `{"command": "reservation-get", "arguments": {"subnet-id": 4, "identifier-type":
"hw-address", "identifier": "01:02:03:04:05:06"}}`
Not found: `{"result": 0, "text": "Host not found."}` — result 0 either way; check `text`.

List all in a subnet (prefer paginated form at scale):
```json
{"command": "reservation-get-all", "arguments": {"subnet-id": 1}}
```

Paginated:
```json
{"command": "reservation-get-page", "arguments": {"subnet-id": 1, "limit": 10}}
```
Response includes a `next` object (`from`, `source-index`) to pass into the following page's
request. End of results: empty `hosts`, count 0, `result: 3`.

By address only (no subnet needed):
```json
{"command": "reservation-get-by-address", "arguments": {"ip-address": "192.0.200.181"}}
```

By hostname:
```json
{"command": "reservation-get-by-hostname", "arguments": {"hostname": "foobar.example.org"}}
```

By identifier across all subnets (subnet-id forbidden here):
```json
{"command": "reservation-get-by-id", "arguments": {"identifier-type": "hw-address",
"identifier": "01:02:03:04:05:06"}}
```

## Update Reservation (full overwrite)

```json
{
    "command": "reservation-update",
    "arguments": {
        "reservation": {"subnet-id": 1, "hw-address": "1a:1b:1c:1d:1e:1f",
        "ip-address": "192.0.2.202"}
    }
}
```

## Delete Reservation

**Stop and confirm with the operator before issuing this call — see `procedure.md`'s Delete step.**
```json
{"command": "reservation-del", "arguments": {"subnet-id": 1, "ip-address": "192.0.2.202"}}
```
Success: `{"result": 0, "text": "Host deleted."}`.

## `operation-target` parameter (host_cmds commands)

Optional on host_cmds commands: `memory` (in-memory config only), `database` (backend only), `all`
(both), or `default` (command-specific — read commands effectively default to `all`, modification
commands to `database`).
