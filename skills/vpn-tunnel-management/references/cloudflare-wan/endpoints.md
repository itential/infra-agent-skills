# Cloudflare WAN — GRE and IPsec Tunnel Endpoints

Wire-level binding for `procedure.md`. Source: Cloudflare Docs API reference for IPsec and GRE
tunnels under the Magic Transit resource, "Configure tunnel endpoints", "Update tunnel health checks
frequency", and "Querying tunnel health check results with GraphQL" (retrieved 2026-10-26 and
2026-10-28).
Base URL: `https://api.cloudflare.com/client/v4`. All calls send `Authorization: Bearer <API_TOKEN>`.
`{account_id}`, `{ipsec_tunnel_id}`, and `{gre_tunnel_id}` are placeholders.

## Calls

| Procedure operation | Method and path | Token permission |
|---|---|---|
| List IPsec tunnels | `GET /accounts/{account_id}/magic/ipsec_tunnels` | `Magic WAN Read`/`Write` or `Magic Transit Read`/`Write` |
| Get IPsec tunnel | `GET /accounts/{account_id}/magic/ipsec_tunnels/{ipsec_tunnel_id}` | Read or Write |
| Create IPsec tunnel | `POST /accounts/{account_id}/magic/ipsec_tunnels` | `Magic WAN Write` or `Magic Transit Write` |
| Update IPsec tunnel | `PUT /accounts/{account_id}/magic/ipsec_tunnels/{ipsec_tunnel_id}` | Write |
| Delete IPsec tunnel | `DELETE /accounts/{account_id}/magic/ipsec_tunnels/{ipsec_tunnel_id}` | Write |
| Generate pre-shared key | `POST /accounts/{account_id}/magic/ipsec_tunnels/{ipsec_tunnel_id}/psk_generate` | Write |
| Set pre-shared keys | `POST /accounts/{account_id}/magic/ipsec_tunnels/psk` | Write; the response lists `successfully_applied_psks` and `unapplied_psks`. Unverified: request body shape |
| List GRE tunnels | `GET /accounts/{account_id}/magic/gre_tunnels` | Read or Write |
| Get GRE tunnel | `GET /accounts/{account_id}/magic/gre_tunnels/{gre_tunnel_id}` | Read or Write |
| Create GRE tunnel | `POST /accounts/{account_id}/magic/gre_tunnels` | Write |
| Update GRE tunnel | `PUT /accounts/{account_id}/magic/gre_tunnels/{gre_tunnel_id}` | Write |
| Delete GRE tunnel | `DELETE /accounts/{account_id}/magic/gre_tunnels/{gre_tunnel_id}` | Write |

Create, update, delete, and key generation accept the query parameter `validate_only=true`, which
runs validation without persisting changes. Delete is described as disabling and removing a static
tunnel. Create accepts an optional boolean header `x-magic-new-hc-target`; Unverified: its effect.

## Body fields (create and update)

Common optional fields: `description`; `health_check` (`enabled`, `direction`
`unidirectional`/`bidirectional`, `rate` `low`/`mid`/`high` with default `mid`, `type`
`reply`/`request` with default `reply`, `target` as a string or `{saved, effective}`; the target is
ignored for bidirectional checks); `bgp` (`customer_asn`, `export_filter_id`, `import_filter_id`,
`extra_prefixes` as CIDRs with no host bits, `md5_key`); `automatic_return_routing` (needs the
`coupler_integration` account flag; rejected otherwise).

GRE tunnel: required `name` (at most 15 characters, no spaces or special characters, unique among
GRE tunnels), `interface_address`, `cloudflare_gre_endpoint`, `customer_gre_endpoint`; optional
`mtu` (minimum 576) and `ttl` (hops).

IPsec tunnel: required `name` (unique), `interface_address`, `cloudflare_endpoint`; optional
`customer_endpoint`, `psk`, `replay_protection` (boolean), `custom_remote_identities` with `fqdn_id`
of the form `<label>.<account ID>.custom.ipsec.cloudflare.com`, and `interface_address6` (a /127
from the virtual subnet).

`interface_address`: described as a 31-bit prefix from `10.0.0.0/8`, `172.16.0.0/12`, or
`192.168.0.0/16`. The guide also allows `/30` and `169.254.240.0/20`; Unverified: which the API
accepts. The API rate names `mid` where the dashboard shows Medium.

## Response fields used

`id`, `name`, endpoints, `interface_address`, `description`, `health_check`, `bgp`, `bgp_status`
(`state` `BGP_DOWN`/`BGP_UP`/`BGP_ESTABLISHING`, `tcp_established`, `updated_at`), `created_on`,
`modified_on`, `automatic_return_routing`, `allow_null_cipher` (IPsec), `replay_protection` (IPsec),
and `psk_metadata.last_generated_on` (IPsec). A key is returned only by generation, once; other responses carry key metadata only. Unverified: whether a response ever echoes a key that was supplied. Envelope: `success`, `errors[]`, `messages[]`, `result`.

## Placeholder bodies

GRE tunnel:

```json
{"name": "<TUNNEL_NAME>", "description": "<TUNNEL_DESCRIPTION>", "interface_address": "<INTERFACE_ADDRESS>", "cloudflare_gre_endpoint": "<CLOUDFLARE_ENDPOINT>", "customer_gre_endpoint": "<CUSTOMER_ENDPOINT>"}
```

IPsec tunnel:

```json
{"name": "<TUNNEL_NAME>", "description": "<TUNNEL_DESCRIPTION>", "interface_address": "<INTERFACE_ADDRESS>", "cloudflare_endpoint": "<CLOUDFLARE_ENDPOINT>", "customer_endpoint": "<CUSTOMER_ENDPOINT>"}
```

## Tunnel health query

| Procedure operation | Method and path |
|---|---|
| Query tunnel health | `POST https://api.cloudflare.com/client/v4/graphql`, bearer token, JSON body with `query` and `variables` |

The query asks the account for the `magicTransitTunnelHealthChecksAdaptiveGroups` dataset, with a
`limit` (the example uses 100) and a filter of `datetime_geq` and `datetime_lt`, and requests
`avg { tunnelState }` with the dimensions `tunnelName` and `edgeColoName`. `tunnelState` is 1
healthy, 0.5 degraded, 0 down, as an average over the window per tunnel and data center. Not
documented: how a value between those three is to be read. The window reaches at most one week, and
its start no more than three months back. Assumption: the token needs analytics read access. Not
documented: its exact permission name, any filter by tunnel name, and what happens when more rows
exist than the limit; the executor narrows the window instead.

The documentation's example response is inconsistent with its query: it nests the results under a
different key and repeats `tunnelState` inside the dimensions. Read the rows under the dataset name
that was requested, and take the state from the averaged field.

The health-check rate is the `health_check.rate` field already listed above. The documentation's own
example of changing it sends only the `health_check` object, whereas the update call requires the
tunnel's name, interface address, and Cloudflare endpoint; follow Step 6 and send the full tunnel.

Placeholder variables:

```json
{"accountTag": "<ACCOUNT_ID>", "datetimeStart": "<START_ISO_8601>", "datetimeEnd": "<END_ISO_8601>"}
```

## Not covered

Static routes, BGP settings and filter profiles, tunnel health alerts, per-data-center traffic volume, and exact error strings: Not documented.
