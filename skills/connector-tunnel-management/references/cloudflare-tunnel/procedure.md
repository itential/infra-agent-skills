# Cloudflare Tunnel — Create, Publish, Route, Diagnose, and Retire a Remotely Managed Tunnel

Create a remotely managed Cloudflare Tunnel, publish an internal service on a hostname or route a
private network through it, read its health, and retire it. Source: Cloudflare Docs "Create a tunnel
(API)", "Add routes", "Virtual networks", "Tunnel availability and failover", "Protocols for published
applications", "Common errors", "Connectivity pre-checks", and the Zero Trust tunnel, route, and
virtual-network API reference pages (retrieved 2026-10-27). Bind each operation through
`endpoints.md`.

Scope: remotely managed tunnels, whose configuration lives at Cloudflare. A locally managed tunnel
(configuration kept in a file on the origin host), private hostname routes, Cloudflare Mesh nodes,
and the policy that governs who may use a published application or route are not covered. The
connector must be installed on a host inside the private network; that step runs on that host, not
through the API.

## Common Sequences

1. **Publish an internal application:** Create tunnel, Run the connector, Publish a hostname, Check
   health.
2. **Connect a private network:** Create tunnel, Run the connector, Add a route (optionally Create a
   virtual network first), Check health.
3. **Diagnose a tunnel:** Check health, then Diagnose.
4. **Retire a tunnel:** Check health, Remove routes, Clean up connectors, Delete tunnel.

## Create tunnel

1. Choose the tunnel name. Create the tunnel as remotely managed so its configuration is held at
   Cloudflare.
2. Success is a returned tunnel `id` with status `inactive`, meaning the tunnel exists but a connector
   has never run. The response also carries a connector token and a credentials object. These are
   secrets: whoever holds the token can run the tunnel, so keep them out of logs and reports, and hand
   the token only to the host that will run the connector. The token can be read again later through
   the token operation.
3. Report `CREATED` with the tunnel `id` and name only.

## Run the connector

The connector (`cloudflared`) is installed on a host inside the private network and started with the
tunnel token. This is a host-side step; the executing agent needs a way to run commands on that host.

1. Before installing, confirm the host can reach Cloudflare outbound on port 7844 over both TCP and
   UDP, and can resolve the tunnel region endpoints. Connector version 2026.5.2 and later runs these
   checks at start; `cloudflared tunnel diag` runs them on demand.
2. Run the service install with the token: `sudo cloudflared service install <TUNNEL_TOKEN>` on Linux
   and macOS, `cloudflared.exe service install <TUNNEL_TOKEN>` from an administrator prompt on
   Windows, or `docker run cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <TUNNEL_TOKEN>`
   for a container.
3. A machine runs at most one `cloudflared` service. If the install reports that a service is already
   installed, add routes to the existing tunnel instead. Removing that service with
   `sudo cloudflared service uninstall` stops whatever tunnel it carries: **stop and confirm with the
   operator before uninstalling it** (unless the operator's standing instructions pre-authorize it).
4. Success is the tunnel status leaving `inactive` (see Check health). Running the same tunnel on
   additional hosts adds replicas: each replica opens its own four connections and all serve the one
   tunnel. Replicas give failover, not load distribution or a choice of which replica serves a request.

## Publish a hostname

Precondition: the hostname's zone is on Cloudflare with its nameservers pointing to Cloudflare.

1. Read the tunnel's current configuration first. Updating the configuration replaces the whole
   configuration, ingress rules included, so a write built from only the new hostname silently drops
   every existing one. Carry the existing rules forward into the new list.
   **Stop and confirm with the operator before replacing a configuration that already contains
   ingress rules** (unless the operator's standing instructions pre-authorize it).
2. Write the ingress list: one rule per hostname giving the hostname and the internal service address,
   and a final catch-all rule with no hostname that returns a fixed status such as 404. The catch-all
   is required. The service value names the protocol and address of the internal service (see
   `endpoints.md` for the accepted service types); wrap an IPv6 literal in square brackets.
3. Create a DNS record for the hostname: a proxied CNAME pointing to the tunnel's identifier at the
   tunnel domain. If a record already exists for that name, choose another hostname, or **stop and
   confirm with the operator before deleting the existing record** (unless the operator's standing
   instructions pre-authorize it); never overwrite it silently.
4. A hostname with more than one subdomain level needs an Advanced Certificate for that hostname; the
   standard certificate does not cover it, and clients otherwise see a "can't provide a secure
   connection" error.
5. Success is the configuration read back showing the ingress rules and the DNS record resolving to the
   tunnel. Report `PUBLISHED`. The hostname is open to the whole Internet until an access policy is
   added; that policy is outside this skill.
6. A non-HTTP service type (TCP, SSH, RDP, SMB) additionally needs the connector client installed on
   the end user's machine.

## Create a virtual network

Needed only when two routes would otherwise use the same address range, for example two sites that both use
`192.0.2.0/24`. Every account has a default virtual network that routes
use when none is named.

1. Create one virtual network per isolated environment, with a name and optional comment.
2. Success is a returned virtual network `id`. Report `CREATED`.
3. Virtual networks apply to Cloudflare Tunnel routes. IPsec, GRE, and Network Interconnect
   connections use only the default virtual network.

## Add a route

1. Create a route that maps a CIDR (or single address) to the tunnel, with an optional comment and the
   virtual network identifier when overlap requires one. The range can be private or public.
2. A CIDR inside `100.96.0.0/12` is rejected because that range is reserved for client routing; the
   private network must be renumbered or routed another way.
3. Success is the route `id` returned and the route appearing when routes are listed for the tunnel.
   Report `ROUTED`. A route makes the network reachable through the tunnel; end-user traffic is not
   steered into it automatically. Client-side connectivity and policy are configured separately and are
   not covered here.
4. Pinging or tracing addresses behind the tunnel works only when the connector is set to allow ICMP.

## Check health

1. Read the tunnel and read its connections. Status is one of `inactive` (never run), `healthy`
   (serving through four connections), `degraded` (serving, but at least one connection has failed),
   or `down` (previously connected, now disconnected).
2. A `healthy` status together with user-facing errors points at the path from the connector to the
   internal service, which status does not measure; check that path separately.
3. Report the status value and the number of connections as read.

## Diagnose

| Observation | Meaning and next step |
|---|---|
| `inactive` | The connector never ran with this tunnel's token; run it (see Run the connector) |
| `down` | The connector process stopped or the host is unavailable; check the service on the host and its logs |
| `degraded` | Some connections failed; read the connector logs and re-run the outbound pre-checks |
| Error 1033 with an inactive or down tunnel | Cloudflare found no healthy connector; resolve the status first |
| Error 1033 with a healthy tunnel | The DNS record points at the wrong tunnel domain; confirm the CNAME target matches the tunnel identifier, using the federal tunnel domain on FedRAMP High accounts |
| 502 Bad Gateway | The tunnel is connected but the connector cannot reach the internal service; check the service is running and listening, the service URL's protocol and port match it, and certificate trust (below) |
| `x509: certificate signed by unknown authority` | The connector does not trust the origin's certificate or an inspecting proxy; add the CA to the host trust store or the connector's CA pool; disabling TLS verification is a temporary last resort that lowers security: confirm with the operator first and turn it off again once trust is fixed |
| Idle long-lived sessions drop | Add application-level keepalives; idle UDP can be dropped by network devices when the connector uses QUIC |

Not documented: a complete error-code catalogue for the tunnel API. Surface the
returned `errors` array unchanged.

## Remove routes

1. List the routes that reference the tunnel and show them to the operator.
2. **Stop and confirm with the operator before deleting a route**, since the network or hostname
   stops being reachable through the tunnel (unless the operator's standing instructions pre-authorize
   it). Delete each by its route identifier.
3. Success is the route absent from a fresh list. Report `UNROUTED`.

## Clean up connectors

Removes connectors from the tunnel regardless of their state; with no connector identifier given it
removes all of them. It is also the documented follow-up after the token is rotated.

1. **Stop and confirm with the operator before cleaning up connectors on a tunnel that is serving
   traffic**, because every removed connector stops serving at once (unless the operator's standing
   instructions pre-authorize it).
2. Success is the connection list empty or reduced to the connectors the operator kept.

## Delete tunnel

Deleting a tunnel is permanent, and the tunnel must have no active connections.

1. The documented precondition is that the tunnel has no active connections: stop the connector hosts or
   clean up connectors first. Assumption: routes referencing the tunnel and its DNS records are removed
   as part of retiring it; the delete call is not documented to remove them.
2. **Stop and confirm with the operator before deleting the tunnel** (unless the operator's standing
   instructions pre-authorize it).
3. Success is a successful delete response and the tunnel no longer appearing in a default list. Report `DELETED`.

## Patterns

- Updating the configuration replaces it, so always read before writing and carry existing ingress
  rules forward.
- Reading the tunnel status answers "is the connector linked," not "does the application work";
  check both before reporting success.
- For overlapping address ranges use one tunnel and one virtual network per isolated environment; a
  single tunnel can carry several non-overlapping routes.
- Replicas fail over but do not balance. When requests must be steered by health or geography, a
  separate load-balancing product is needed; a private hostname route is documented as not compatible
  with it, so use replicas there.
- Handle the whole tunnel creation response as secret: it carries the token and a credentials object.

## Known limitations

- Locally managed tunnels, private hostname routes, and Cloudflare Mesh are not covered.
- Unverified: the call that rotates a tunnel's token; the documented token operation only reads it, and
  connector cleanup is recommended after a rotation.
- Not documented: rate limits for these calls; on an HTTP 429, back off and honor any
  `Retry-After` header.
- Irreversible: tunnel deletion.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create tunnel | Create a remotely managed tunnel | Tunnel API |
| Read tunnel, Read connections, List tunnels | Status and connector state | Tunnel API |
| Read token | Retrieve the connector token (secret) | Tunnel API |
| Read configuration, Replace configuration | Ingress rules for published hostnames | Tunnel API |
| Clean up connectors | Remove connectors from a tunnel | Tunnel API |
| Delete tunnel | Permanently remove a tunnel | Tunnel API |
| Create DNS record | Point a hostname at the tunnel | DNS API |
| Create/List/Delete route | Private network routes | Networks API |
| Create virtual network | Routing isolation domain | Networks API |
| Host command session | Install and run the connector on the origin host | SSH/console session |

## Verification checklist

- [ ] The tunnel was created as remotely managed and the token and credentials were not echoed
- [ ] Outbound port 7844 (TCP and UDP) and region name resolution were checked before the connector ran
- [ ] The configuration was read before it was replaced, existing ingress rules were carried forward, and
      the final catch-all rule is present
- [ ] The hostname's DNS record exists and points at this tunnel, with a certificate covering multi-level
      names where used
- [ ] Routes avoid `100.96.0.0/12` and use a virtual network where ranges overlap
- [ ] Status and connection count were read, and the internal service was checked separately
- [ ] Before replacing a populated configuration, deleting a route, cleaning up connectors, or deleting
      the tunnel: confirmed with the operator
- [ ] Outcome reported with this procedure's status vocabulary (`CREATED`, `PUBLISHED`, `ROUTED`,
      `UNROUTED`, `DELETED`, `FAILED`)
