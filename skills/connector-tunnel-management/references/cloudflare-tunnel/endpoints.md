# Cloudflare Tunnel — Endpoint Wiring

Wire-level binding for `procedure.md`. Source: Cloudflare Docs "Create a tunnel (API)", "Protocols for
published applications", and the Zero Trust tunnel, route, and virtual-network API reference pages
(retrieved 2026-10-27). Base URL: `https://api.cloudflare.com/client/v4`. All calls send
`Authorization: Bearer <API_TOKEN>`. `{account_id}`, `{zone_id}`, `{tunnel_id}`, `{route_id}` are
placeholders. Responses use the standard `success`, `errors[]`, `messages[]`, `result` envelope.

## Calls

| Procedure operation | Method and path | Notes |
|---|---|---|
| Create tunnel | `POST /accounts/{account_id}/cfd_tunnel` | Body `name`, `config_src` (`cloudflare` = remotely managed, `local`). Result carries `id`, `status`, `token`, `credentials_file` (secrets) |
| List tunnels | `GET /accounts/{account_id}/cfd_tunnel` | Filters: `name`, `status`, `is_deleted`, `uuid`, `include_prefix`, `exclude_prefix`, `existed_at`, `was_active_at`, `was_inactive_at`, `page`, `per_page` |
| Read tunnel | `GET /accounts/{account_id}/cfd_tunnel/{tunnel_id}` | `status`: `inactive`, `degraded`, `healthy`, `down`. The `connections` array on the tunnel object is deprecated; use the connections call |
| Read connections | `GET /accounts/{account_id}/cfd_tunnel/{tunnel_id}/connections` | Connector ids, versions, locations. A healthy tunnel shows four |
| Read token | `GET /accounts/{account_id}/cfd_tunnel/{tunnel_id}/token` | `result` is the token string (secret) |
| Read configuration | `GET /accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations` | Same path as the write call |
| Replace configuration | `PUT /accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations` | Replaces the whole configuration. Body `config.ingress[]` (each `hostname`, `service`, optional `path`, `originRequest`) and optional `config.originRequest` |
| Clean up connectors | `DELETE /accounts/{account_id}/cfd_tunnel/{tunnel_id}/connections` | Optional connector id (`client_id`); omitted removes all connectors |
| Delete tunnel | `DELETE /accounts/{account_id}/cfd_tunnel/{tunnel_id}` | Permanent; requires no active connections |
| Create DNS record | `POST /zones/{zone_id}/dns_records` | `type` `CNAME`, `name` the hostname, `content` `<tunnel_id>.cfargotunnel.com`, `proxied` true. Federal accounts use `<tunnel_id>.fed-cfargotunnel.com` |
| Create virtual network | `POST /accounts/{account_id}/teamnet/virtual_networks` | Body `name`, optional `comment`. The `is_default` field is deprecated in favor of `is_default_network` |
| Create route | `POST /accounts/{account_id}/teamnet/routes` | Body `network` (CIDR), `tunnel_id`, optional `comment`, `virtual_network_id` |
| List routes | `GET /accounts/{account_id}/teamnet/routes` | Filters include `tunnel_id`, `virtual_network_id`, `network_subset`, `network_superset`, `route_id`, `is_deleted`, `tun_types` |
| Delete route | `DELETE /accounts/{account_id}/teamnet/routes/{route_id}` | Returns the removed route |

Token permissions: tunnel create, configuration, connection, token, and delete calls accept any of
`Cloudflare One Connectors Write`, `Cloudflare One Connector: cloudflared Write`, or `Cloudflare Tunnel
Write`; the tunnel and connection reads also accept the matching Read permissions, but the token read accepts
only the Write ones. Route and virtual-network writes accept `Cloudflare One Networks Write` or
`Cloudflare Tunnel Write`; the route list also accepts `Cloudflare One Networks Read` and
`Cloudflare Tunnel Read`. The DNS record needs `DNS Write`. Unverified: the permission names for the
virtual-network and configuration reads.

## Ingress service types

`http://host:port`, `https://host:port`, `unix:/path`, `unix+tls:/path`, `tcp://host:port`,
`ssh://host:port`, `rdp://host:port`, `smb://host:port`, `http_status:<code>`, `bastion`, and
`hello_world` (locally managed tunnels only). IPv6 literals are written `http://[2001:db8::1]:8000`.
The last ingress rule has no `hostname` and, for example, `service` `http_status:404`.

## Placeholder bodies

```json
{"name": "example-tunnel", "config_src": "cloudflare"}
```

```json
{"config": {"ingress": [
  {"hostname": "app.example.com", "service": "http://localhost:8001", "originRequest": {}},
  {"service": "http_status:404"}]}}
```

```json
{"network": "172.16.0.0/16", "tunnel_id": "<TUNNEL_ID>", "comment": "Example route", "virtual_network_id": "<VNET_ID>"}
```

## Error text worth recognizing

- `This route's network is inside an existing subnet's network at "100.96.0.0/12"`: the CIDR falls in
  the range reserved for client routing.
- `An A, AAAA, or CNAME record with that host already exists`: the hostname already has a record.
- Error 1033 (browser-facing): no healthy connector, or the DNS record targets the wrong tunnel domain.
- 502 `Unable to reach the origin service`: the tunnel is connected but the internal service is not
  reachable from the connector.
