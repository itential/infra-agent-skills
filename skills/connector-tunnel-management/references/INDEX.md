# Connector Tunnel Management — Vendor Index

One row per supported platform. Each directory holds its own procedure file, plus a wire-level
endpoints file for REST-driven platforms.

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| Cloudflare Tunnel (`cloudflared`) | `cloudflare-tunnel/` | Create a remotely managed tunnel, publish a hostname, add or remove a private network route (optionally in a virtual network), read status and connections, clean up connectors, delete a tunnel | REST plus a host-side connector install. Locally managed tunnels (configuration file on the origin host) are not covered. Only one implementation is documented. WAN IPsec/GRE tunnels are a separate vendor under `vpn-tunnel-management`. |
