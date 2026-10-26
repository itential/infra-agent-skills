# Cloudflare WAN — GRE and IPsec Tunnel Procedure

List, read, create, update, and delete the GRE and IPsec tunnels that connect a customer router to
Cloudflare WAN's anycast tunnel endpoints, including generating or setting an IPsec pre-shared key
and the per-tunnel health-check settings. Source: Cloudflare Docs "GRE and IPsec tunnels",
"Configure tunnel endpoints", "Tunnel health checks", "Troubleshoot tunnel health", and the API
reference for IPsec and GRE tunnels under the Magic Transit resource (retrieved 2026-10-26).

Scope: the tunnel objects only. BGP settings and filter profiles, static routes, Network
Interconnect, the Cloudflare One Appliance, tunnel health analytics, and the customer router's own
configuration are separate and not covered. Bind each operation through `endpoints.md`.

## Common Sequences

1. **Add an IPsec tunnel:** gather the endpoints and interface address → list tunnels (check name and
   endpoint uniqueness) → validate → create → generate or set the pre-shared key → configure the
   customer router → read the tunnel and confirm health.
2. **Add a GRE tunnel:** gather the endpoints and interface address → list tunnels → validate →
   create → configure the customer router → read the tunnel and confirm health.
3. **Change a tunnel:** read it → keep a copy → validate → update with the full desired tunnel →
   read back.
4. **Remove a tunnel:** read it → confirm → delete → confirm it no longer appears in the list.

## Step 0: Choose the tunnel type and collect inputs

| | GRE | IPsec |
|---|---|---|
| Encryption and authentication | None | Encrypted; pre-shared key |
| Setup | Simpler | Needs a key exchange with the router |
| Suited to | Trusted networks, Network Interconnect | Internet-facing links that need encryption |

- Cloudflare endpoint: an anycast address assigned to the account (the dashboard lists them under
  leased addresses). No call in this procedure lists them; ask the operator for the address.
- Customer endpoint: the router's public address, outside prefixes Cloudflare advertises for the
  account. Needed for GRE unless Network Interconnect supplies it. For IPsec it is optional: required
  only when the router uses an IKE ID of type `ID_IPV4_ADDR`, and useful for proactive traceroutes.
- Interface address: a `/31` (a `/30` is also described) from private space (`10.0.0.0/8`,
  `172.16.0.0/12`, `192.168.0.0/16`, or `169.254.240.0/20` per the guide). The API reference
  describes a 31-bit prefix from the first three private ranges only; Unverified: whether the API
  accepts `/30` or `169.254.240.0/20`. A prefix outside the allowed ranges leaves the tunnel
  non-functional.
- Name: unique among tunnels. A GRE name has at most 15 characters and no spaces or special
  characters; the dashboard applies the same no-spaces rule to IPsec names.
- For redundancy, use two tunnels from separate routers.

Success: type, endpoints, interface address, and name are fixed, and the name and endpoint pair are
not already in use.

## Step 1: List and read tunnels

List GRE tunnels and IPsec tunnels separately, or read one by ID. Note each tunnel's name,
endpoints, interface address, health-check settings, and (for IPsec) the key metadata, which shows
when the key was last generated but never the key itself.

Success: the tunnel set is in hand, with no tunnel of the same name and no IPsec tunnel with the
same Cloudflare and customer endpoint pair.

## Step 2: Validate

Create, update, delete, and key generation each accept a validate-only mode that runs validation
without saving anything. Run it before the real call.

Success: validation returns no error.

## Step 3: Create a GRE tunnel

Create the tunnel with its name, optional description, interface address, Cloudflare and customer
GRE endpoints, and any optional settings: MTU (minimum 576), TTL, health-check settings, BGP
settings, and automatic return routing. Read it back.

Success: the response returns a tunnel ID and the stored settings. Configure the customer router
with the matching endpoints and interface address, then confirm health (Step 8).

## Step 4: Create an IPsec tunnel

Create the tunnel with its name, optional description, interface address, Cloudflare endpoint,
optional customer endpoint, and any optional settings: health-check settings, replay protection,
BGP settings, a custom FQDN IKE ID, and automatic return routing. Read it back.

- An IPsec tunnel does not work without a pre-shared key. Create it without one and then generate a
  key (Step 5), or supply the operator's key at creation or through the key-set call. A supplied key is never printed, logged, or quoted either.
- Replay protection is off by default; turn it on only for routers that cannot disable it (the
  guide names Cisco Meraki, Velocloud, and AWS VPN Gateway).

Success: the response returns a tunnel ID and the stored settings; the tunnel is not functional
until it has a key.

## Step 5: Generate or set the pre-shared key

1. **Unless the operator's standing instructions pre-authorize it, stop and confirm with the
   operator before proceeding if the tunnel already has a key.** Replacing a key on a live tunnel
   drops it until the router carries the new key, and the old key cannot be retrieved afterwards.
   A first key on a tunnel without one needs no confirmation.
2. Generate a key, or set a key the operator supplied.
3. The generated key is returned once and cannot be retrieved later. Never print, log, quote, or
   include it in any report: hand it only to the operator's secret-handling channel and report
   metadata only (tunnel ID, time generated).

Success: the response returns the key once (generation) or lists the tunnels whose keys were applied
(set), and the key metadata shows a new generation time.

## Step 6: Update a tunnel

1. Read the tunnel first and keep a copy for rollback.
2. Send the update with the full desired tunnel: the call requires the name, interface address, and Cloudflare endpoint (for GRE, also the customer endpoint), and (assumption: the update replaces the stored tunnel; merge behavior is not stated) every optional setting that should survive. Unverified: whether an update that omits the pre-shared key keeps the stored key. The stored key cannot be read back, so after any update to an IPsec tunnel check that the key metadata still shows a generation time, and be prepared to generate or set a key again.
3. Read the tunnel back.

Changing an endpoint or interface address on a live tunnel interrupts it until the router matches.
Success: the read-back shows the intended settings and the health check recovers (Step 8).

## Step 7: Delete a tunnel

1. Read the tunnel and show the operator its name, type, endpoints, and interface address.
2. **Unless the operator's standing instructions pre-authorize it, stop and confirm with the operator
   before proceeding.** Deletion disables and removes the tunnel and stops traffic through it. For
   IPsec, recreating the tunnel needs a new key and a router update (assumption: the key is removed
   with the tunnel; the reference does not say).
   Whether routes or other objects that reference the tunnel block deletion or are left dangling is
   not documented: check them first.
3. Delete by ID, then confirm the tunnel is gone from the list.

## Step 8: Confirm the tunnel is working

A successful configuration call is not an established tunnel. Cloudflare probes each tunnel with
ICMP health checks and reports one of three states per data center: Healthy (more than 80% of
probes pass), Degraded (40% to 80%), or Down (under 40%). A failed probe is retried twice before it
counts. Expect at least five minutes in a degraded state before recovery registers, and up to 30 minutes to return to Healthy. A data center showing "100% degraded" means the tunnel entered the degraded state there; it does not measure loss, so judge by the data centers that carry the tunnel's traffic. These percentages are the dashboard's view; Cloudflare's health-check reference gives a different failure-rate rule that drives route steering. The call that returns health state is not bound here (Unverified): use the dashboard's Network health page or the tunnel health API, and if neither is available report the tunnel as configured with health not confirmed, never as up.

Success: the tunnel shows Healthy in the data centers that carry its traffic.

## Patterns

- **Anycast.** The Cloudflare end is an anycast address, so any data center can carry a tunnel. GRE
  is stateless; for IPsec one server negotiates and then shares the tunnel details across all data
  centers.
- **Cloudflare only responds.** The customer router starts the IKE negotiation; Cloudflare operates
  as the IKE responder.
- **Router requirements for IPsec.** IKEv2 only; pre-shared-key authentication; NAT traversal is
  supported from port 4500; Extended Sequence Numbers must be off. For replay protection, enable
  dead peer detection with the restart-session action. The supported IKE and Child SA algorithms are
  fixed by Cloudflare and chosen on the router, not in the tunnel object. Cloudflare recommends DH
  group 20 for the Child SA and a Child SA lifetime of 30 minutes to 8 hours; post-quantum hybrid
  key exchange needs RFC 9370 support on the router.
- **Size packets.** Encapsulation adds header bytes: set the router's MSS and MTU for the 1500-byte
  Internet MTU (typical values: 1476 for GRE, 1400 to 1450 for IPsec).
- **Keep health checks on.** With health checks disabled a working tunnel looks 100% down, and
  Cloudflare cannot detect or steer around a failure.
- **Health-check type and direction.** Reply style is the default; use Request style when a stateful
  firewall drops reply probes. The dashboard defaults to bidirectional; the API's default direction
  is not stated. IPsec tunnels need traffic selectors that accept the probes. If Cloudflare Network
  Firewall is on, allow ICMP from Cloudflare addresses or probes fail.
- **IKE ID.** The `ID_IPV4_ADDR` IKE ID works only if the customer endpoint is set and the
  Cloudflare and customer endpoint pair is unique among the account's IPsec tunnels; otherwise use
  one of the custom ID formats that carry the tunnel and account IDs.
- **Prefer route-based IPsec.** Policy-based VPNs allow one set of traffic selectors per Child SA,
  need the probes to match a policy, and cap a tunnel at roughly 100 Child SAs.
- **BGP MD5 is not a secret.** The MD5 key on a BGP session guards against misconfiguration only.
  Automatic return routing needs the `coupler_integration` account flag and Unified Routing.

## Known limitations

- Covers GRE and IPsec tunnel objects only. BGP settings, static routes, Network Interconnect, the
  Cloudflare One Appliance, health analytics, and Cloudflare Network Firewall rules are out of scope.
- Not documented: rate limits, error codes, whether update merges or replaces, what delete does to
  routes that reference a tunnel, and the default health-check direction through the API. On
  HTTP 429, back off and honor any `Retry-After` header.
- A tunnel change reaches live traffic with no draft or staged state, and no propagation time is
  stated.

## Tools

| Operation | Description | Category |
|---|---|---|
| List tunnels | Enumerate GRE or IPsec tunnels | Read |
| Get tunnel | Fetch one tunnel | Read |
| Create tunnel | Add a GRE or IPsec tunnel (validate-only available) | Write |
| Update tunnel | Replace a tunnel's settings (validate-only available) | Write |
| Delete tunnel | Remove a tunnel | Write (destructive) |
| Generate pre-shared key | Create and store an IPsec key, returned once | Write |
| Set pre-shared keys | Apply supplied keys to IPsec tunnels | Write |

## Verification checklist

- [ ] Tunnel type, endpoints, interface address, and name validated before creating
- [ ] Interface address inside the allowed private ranges
- [ ] IPsec tunnel has a key, and the key never appears in reported output
- [ ] A key replacement or a delete was confirmed with the operator, or pre-authorized by standing instructions
- [ ] Customer router configured with the matching endpoints, key, and supported parameters
- [ ] Health state read after creation and not reported as up before it shows Healthy
