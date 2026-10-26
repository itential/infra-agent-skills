# Azure Network Inspection via the Azure CLI

Read Azure network inventory, effective NIC rules and routes, ExpressRoute and gateway state, and Application Gateway backend health with an authenticated Azure CLI session.

Sources: Microsoft Learn Azure CLI reference (azure-cli-latest) for `az account`, `az network vnet`, `nsg`, `nic`, `express-route`, `vnet-gateway`, `vpn-connection`, `lb`, `application-gateway`, `firewall`, `route-table`, `watcher`, `private-endpoint`, `dns`, and `private-dns`, retrieved 2026-10-26.

This procedure is diagnostic-shaped and read-only: every command below lists or shows state, so it has no confirmation gates. Commands run with an explicit subscription and `--output json`.

## Common Sequences

- Inventory: Select subscription, Read virtual networks, Read supporting services.
- NIC policy evidence: Select subscription, Read virtual networks, Read security groups, Read effective NIC state.
- Hybrid or application evidence: Select subscription, then Read hybrid connectivity or Read load-balancing evidence.

## Select subscription

`az account list --output json` returns the subscriptions the signed-in session can see. Confirm the requested one is present and pass `--subscription <subscription-id>` on every later command. One subscription is queried at a time. Authentication or authorization failure leaves its resources unobserved.

## Read virtual networks

`az network vnet list` (optionally `--resource-group <group>`), `az network vnet show --resource-group <group> --name <vnet>`, and `az network vnet peering list --resource-group <group> --vnet-name <vnet>` return networks and peerings. When `--max-items <n>` truncates a list, the output carries a token; pass it as `--next-token <token>` to continue until no token is returned. Success is the scoped list or the named object with its configuration and state values kept as returned.

## Read security groups

`az network nsg list` gives groups; `az network nsg show --resource-group <group> --name <nsg>` returns one group including its default rules, which a custom-rules-only read would omit. An NSG with no association is an observation, not a defect.

## Read effective NIC state

`az network nic show --resource-group <group> --name <nic>` returns the NIC. `az network nic list-effective-nsg --resource-group <group> --name <nic>` returns the effective security rules and `az network nic show-effective-route-table --resource-group <group> --name <nic>` the effective routes. Both run in their default waiting mode; the no-wait option is not used here. A failure does not show that no rule or route applies. Not documented in the CLI reference: the prerequisites for these two commands (for example whether the attached VM must be running); consult Microsoft's effective-security-rule and effective-route troubleshooting guidance.

## Read hybrid connectivity

- ExpressRoute: `az network express-route list`, `az network express-route show --resource-group <group> --name <circuit>`, and `az network express-route list-route-tables --resource-group <group> --name <circuit> --peering-name <peering> --path primary` (or `secondary`) for the peering's routing table. The route-table command is preview.
- VPN: `az network vnet-gateway list --resource-group <group>`, `az network vnet-gateway show --resource-group <group> --name <gateway>`, `az network vpn-connection list --resource-group <group>`, `az network vpn-connection show --resource-group <group> --name <connection>`.

These return configuration and reported status, not a live packet test. `az network vpn-connection shared-key show` retrieves the connection's shared secret, so it is excluded from this read-only inspection.

## Read load-balancing evidence

`az network lb list` and `az network lb show --resource-group <group> --name <lb>` return load balancer configuration, which does not establish backend health. `az network application-gateway show-backend-health --resource-group <group> --name <gateway>` returns backend health; the optional probe overrides are not used here. Keep native health values; an unknown value is not healthy. Per-member health for Azure Load Balancer is not covered.

## Read supporting services

| Concern | Read command |
|---|---|
| Azure Firewall (extension command) | `az network firewall list`, `az network firewall show --resource-group <group> --name <firewall>` |
| Firewall policy (extension) | `az network firewall policy show --resource-group <group> --name <policy>` |
| Rule collection groups (extension, preview) | `az network firewall policy rule-collection-group list --resource-group <group> --policy-name <policy>` |
| Route tables | `az network route-table list`, then `az network route-table show --resource-group <group> --name <table>` |
| Network Watchers | `az network watcher list` |
| Connection monitors | `az network watcher connection-monitor list --location <region>` |
| Flow-log configuration | `az network watcher flow-log list --location <region>` |
| Private endpoints | `az network private-endpoint list`, then `az network private-endpoint dns-zone-group list --resource-group <group> --endpoint-name <endpoint>` |
| Public DNS record sets | `az network dns record-set list --resource-group <group> --zone-name <zone>` |
| Private DNS record sets | `az network private-dns record-set list --resource-group <group> --zone-name <zone>` |

The flow-log list returns configuration only; reading the flow data itself is not covered.

## Patterns

- Configuration, effective state, circuit routing tables, and backend health answer different questions; label each.
- A configured backend pool says nothing about member health.
- A missing resource, missing permission, bad argument, or throttling response is an error to report, not an empty inventory.

## Known limitations

- Error strings, throttling quotas, and retry timing are not documented in the command references. On throttling, back off and honor any retry guidance the CLI returns.
- No resource modification, Front Door routing, subnet-utilization calculation, or compliance scoring. DNS reads need a known zone name; zone discovery is not covered.
- Azure Firewall commands require the Azure Firewall CLI extension; if it is not installed they are unavailable.

## Tools

| Mechanism | Purpose | Category |
|---|---|---|
| Authenticated Azure CLI session | Run the documented list and show commands in the chosen subscription | Read |

## Verification checklist

- Subscription, resource group, region, and resource name accompany each result.
- Pagination tokens were followed to the end where a list was truncated.
- Default NSG rules are included when security rules are reported.
- Effective state, routing tables, and backend health are labeled apart from configuration.
- No health or compliance conclusion beyond the returned values.
