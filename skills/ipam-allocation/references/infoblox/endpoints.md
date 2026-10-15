# Endpoint Wiring — Infoblox NIOS IPAM Allocation

Literal WAPI calls behind each capability named in `procedure.md`. Base URL:
`https://<grid-master>/wapi/v2.13.7`. Auth: Basic auth or session cookie against the Grid Master.

## Resolve the Network Container

Tool hint: `GET /networkcontainer?_return_fields+=extattrs&<filter>`.

Filter by `network_view`, `network` (CIDR, supports `=`/`~=` operators), or an extensible attribute
(prefixed `*`, e.g. `*Country:=RED`). Response is an array; each element's `_ref` is the container
reference to use in the next step, e.g.
`networkcontainer/ZG5zLm5ldHdvcmtfY29udGFpbmVyJDEwLjAuMC4wLzE2LzQ1:10.0.0.0/16/Dell`.

## Allocate the Next Available Network

**Inline `func:` string form** (single call):
```
POST /network?_return_fields+=network,comment&_return_as_object=1
{
  "network": "func:nextavailablenetwork:172.16.0.0/16,Dell,24",
  "network_view": "Dell",
  "comment": "Used"
}
```
The three comma-separated arguments after `nextavailablenetwork:` are: the container reference or raw
CIDR, the network view, and the requested child CIDR prefix length. Response:
```json
{"result": {"_ref": "network/...:172.16.5.0/24/Dell", "comment": "Used", "network": "172.16.5.0/24", "network_view": "Dell"}}
```

**Atomic `/request` form** (resolve container + allocate in one call):
```
POST /request
[
  {
    "method": "GET",
    "object": "networkcontainer",
    "data": {"network_view": "Dell", "*Country": "RED"},
    "args": {"_return_fields+": "extattrs"},
    "assign_state": {"net_ref": "network", "net_view": "network_view"},
    "discard": true
  },
  {
    "method": "POST",
    "object": "network",
    "enable_substitution": true,
    "data": {
      "network": "func:nextavailablenetwork:##STATE:net_ref:##,##STATE:sif_view:##,24",
      "network_view": "##STATE:sif_view:##",
      "comment": "Used"
    }
  }
]
```
`assign_state` captures values from the first operation's result into named state variables
(`net_ref`, `net_view` here) for substitution (`##STATE:name:##`) in later operations within the same
`/request` array; `discard: true` on the first op means its own result isn't included in the final
response, only the state it produced. Response is an array of `_ref` strings, one per operation that
wasn't discarded — e.g. `["network/...:10.0.30.0/24/Dell"]`.

**Direct function parameters** (either form): `cidr` (required, integer), `num` (optional, default 1),
`exclude` (optional, array of networks to exclude).

## Allocate the Next Available IP

**Standalone reservation:**
```
POST /network/<network-ref>?_function=next_available_ip
{"num": 1, "exclude": ["10.102.0.1", "10.102.0.2"]}
```
or, per PowerShell/CLI-style tooling, the plain string form:
`"ipv4addr": "func:nextavailableip:10.10.10.0/24"`.

**Nested-object form** (newer, WAPI v2.8-era — reserve + assign in the same create call):
```
POST /fixedaddress
{
  "name": "host001",
  "mac": "AB:CD:00:11:22:33",
  "ipv4addr": {
    "_object_function": "next_available_ip",
    "_object": "network",
    "_object_parameters": {"network": "10.102.0.0/16"},
    "_result_field": "ips",
    "_parameters": {"exclude": ["10.102.0.1", "10.102.0.2", "10.102.0.3"]}
  }
}
```

**Nested-object form** (older, WAPI v1.2-era — different field names):
```
POST /record:host
{
  "name": "wapi.test.org",
  "ipv4addrs": [{
    "ipv4addr": {
      "_function": "next_available_ip",
      "_object_field": "value",
      "_object": "network",
      "_object_parameters": {"*Site": "Santa Clara"},
      "_parameters": {"num": 1, "exclude": ["45.0.1.1", "45.0.1.2"]}
    }
  }]
}
```

Confirm which field-name set (`_object_function`/`_result_field` vs. `_function`/`_object_field`) the
target Grid Master's WAPI version actually expects before relying on either verbatim.
