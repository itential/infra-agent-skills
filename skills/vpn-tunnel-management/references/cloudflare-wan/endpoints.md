# Cloudflare WAN — GRE and IPsec Tunnel Endpoints

Wire-level binding for `procedure.md`. Source: Cloudflare Docs API reference for IPsec and GRE
tunnels under the Magic Transit resource, and "Configure tunnel endpoints" (retrieved 2026-10-26).
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

## Not covered

The tunnel health state call (Cloudflare documents a tunnel health API, but no route is recorded here: Unverified), static routes, BGP settings and filter profiles, and exact error strings: Not documented.
