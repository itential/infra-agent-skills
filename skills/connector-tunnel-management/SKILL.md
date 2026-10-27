---
name: connector-tunnel-management
description: Create, expose, check, and retire an outbound-only connector tunnel that publishes an internal application or connects a private network to a cloud edge without opening inbound firewall ports — Cloudflare Tunnel (the cloudflared connector). Use when a tunnel needs to be created, a hostname or private network route attached to it, its health diagnosed, or the tunnel and its routes removed. Not for site-to-site IPsec or GRE tunnels (see vpn-tunnel-management). Assumes an authenticated Cloudflare API client with tunnel permissions is already available and that the operator can run the connector on a host inside the private network; this skill does not provision or authenticate that client.
argument-hint: "[platform] [action] [tunnel_name] [hostname|cidr...]"
---

# Connector Tunnel Management

Creates a connector tunnel, attaches a published hostname or a private network route to it, diagnoses
its health, and retires it, following the platform's own documented procedure
(`references/<vendor>/procedure.md`).

## When to use this skill

- An internal web or TCP service needs to be reachable from the Internet or from authorized users
  without an inbound firewall rule: create the tunnel and publish a hostname.
- A private IP range or private hostname needs to be reachable through a connector installed inside
  that network: create the tunnel and add a route.
- A tunnel shows as inactive, down, or degraded, or users get an error for a published application:
  diagnose it.
- A tunnel, its routes, or its connectors need to be rotated or removed.
- Not for site-to-site IPsec or GRE tunnels between routers (see `vpn-tunnel-management`), for the
  access policy that decides who may reach the application (see
  `zero-trust-access-policy-management`), or for the DNS records of a zone beyond the one the
  platform's procedure requires (see `dns-record-management`).

## Universal concepts (apply regardless of platform)

- **A connector tunnel is outbound-only.** The connector runs inside the private network and opens
  connections out to the provider, so exposing a service does not require an inbound rule. Where
  documented, the tunnel object and the connector process are separate: creating the tunnel does not
  make it carry traffic until a connector runs with the tunnel's credential.
- **The tunnel credential is a secret.** Anyone holding it can run the tunnel. Handle it as a secret
  and do not echo it into logs or reports.
- **Tunnel health reports the connector's link to the provider, not whether the internal service
  answers.** A tunnel can read healthy while the application behind it fails.
- **Routing is a separate record from the tunnel.** Reaching a service needs a route or published
  hostname attached to the tunnel, and removing the tunnel does not necessarily remove them first.
- Only one implementation is listed in `references/INDEX.md`; each claim above holds only where the
  platform documents it.

## Procedure

1. **Identify the target platform** from the request or the `platform` argument. If it is not in
   `references/INDEX.md`, stop: this skill does not cover it and does not improvise a procedure.
2. **Open `references/<platform>/procedure.md`** and follow it exactly, including its confirmation
   gates. It holds the full steps, error handling, patterns, limitations, tools, and verification
   checklist.
3. **Report the outcome** using that procedure's own status vocabulary, not a normalized one.

## Known limitations

- Platform coverage is exactly the platforms in `references/INDEX.md`.
- Does not cover the policy that governs who may use a published application or private route, the
  provider's load balancing, or the internal service's own configuration.
- Does not cover site-to-site IPsec or GRE tunnels; those are routed to `vpn-tunnel-management`.

## Contributing to this skill

**`SKILL.md` itself should only ever change for two reasons: a bug in the universal concepts or router
logic above, or adding a pointer to a newly supported platform.** Platform-specific changes — a new
error, a corrected field, a changed path — belong in that platform's own `references/<platform>/`
files, never here.

## Tools

Each platform assumes its own authenticated client; see `references/INDEX.md` for which, and that
platform's `procedure.md` for the operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md`
- [ ] That platform's `procedure.md` was followed, including its confirmation gates
- [ ] The tunnel credential was not written into any output
- [ ] Outcome reported using the platform procedure's own status vocabulary
