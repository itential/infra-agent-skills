# Azure network configuration and observed state

Read Azure network inventory, configuration, effective NIC rules/routes, ExpressRoute routing tables and Application Gateway backend health with an authenticated Azure CLI.

## Common Sequences

- Network inventory: **Select subscription** → **Read virtual networks** → **Read supporting services**.
- NIC policy evidence: **Select subscription** → **Read virtual networks** → **Read security groups** → **Read effective NIC state**.
- Hybrid or application connectivity evidence: **Select subscription** → **Read hybrid connectivity** or **Read load-balancing evidence**, for the named resource.

### Select subscription

`az account list --output json` returns the subscriptions accessible to the existing session. Every following command carries `--subscription <subscription-id> --output json`; placeholders identify selected resources rather than implicit local defaults. Success is the requested subscription in the accessible account collection. Authentication/authorization failures leave its resources unobserved.

### Read virtual networks

`az network vnet list` returns virtual networks; `az network vnet show --resource-group <group> --name <vnet>` returns the selected network. `az network vnet peering list --resource-group <group> --vnet-name <vnet>` returns its peerings. Success is the scoped inventory or named network/peering collection with the platform's configuration and state values retained. Where `--max-items` truncates a supported list, `--next-token <returned-token>` continues that same list until no token remains.

### Read security groups

`az network nsg list` supplies the security groups. `az network nsg show --resource-group <group> --name <nsg>` reads one group's configuration, including default rules; selecting only custom rules would omit part of the evidence. Success is the matching group and its rule collections. Association absence is reported as an observed configuration fact, not automatically as a compliance defect.

### Read effective NIC state

`az network nic list-effective-nsg --resource-group <group> --name <nic>` reads effective security-group evidence. `az network nic show-effective-route-table --resource-group <group> --name <nic>` reads the effective route table. Success is the completed result for that NIC; this sequence does not use the asynchronous no-wait option. A failed operation does not establish that no security group or route applies. Platform prerequisites or failure details not explained by these command references require the linked Microsoft troubleshooting guidance.

### Read hybrid connectivity

`az network express-route list` identifies circuits; `az network express-route show --resource-group <group> --name <circuit>` returns circuit configuration. `az network express-route list-route-tables --resource-group <group> --name <circuit> --peering-name <peering> --path primary` reads the requested peering's primary path; `secondary` selects the other path. Success is that path's returned routing table. The route-table command is documented as preview.

`az network vnet-gateway list --resource-group <group>` and `az network vnet-gateway show --resource-group <group> --name <gateway>` read gateways. `az network vpn-connection list --resource-group <group>` and `az network vpn-connection show --resource-group <group> --name <connection>` read VPN connections. Success is the named configuration/status evidence, not a separate live packet test.

### Read load-balancing evidence

`az network lb list` and `az network lb show --resource-group <group> --name <load-balancer>` return load-balancer configuration. Their success does not establish backend health. `az network application-gateway show-backend-health --resource-group <group> --name <application-gateway>` returns Application Gateway backend-health evidence. This procedure uses no custom on-demand probe arguments. Native health values are retained; an unknown result is not converted to healthy.

### Read supporting services

Each selected command returns the named resource or a scoped collection. Resource and region selection remain part of the reported result.

| Concern | Read command |
|---|---|
| Azure Firewall | `az network firewall list` |
| Firewall policy | `az network firewall policy show --resource-group <group> --name <policy>` |
| Policy rule groups (preview) | `az network firewall policy rule-collection-group list --resource-group <group> --policy-name <policy>` |
| Route tables | `az network route-table list --resource-group <group>` then `az network route-table show --resource-group <group> --name <table>` |
| Network Watchers | `az network watcher list` |
| Connection monitors | `az network watcher connection-monitor list --location <region>` |
| Flow-log configuration | `az network watcher flow-log list --location <region>` |
| Private endpoints | `az network private-endpoint list` then `az network private-endpoint dns-zone-group list --resource-group <group> --endpoint-name <endpoint>` |
| Public DNS records | `az network dns record-set list --resource-group <group> --zone-name <zone>` |
| Private DNS records | `az network private-dns record-set list --resource-group <group> --zone-name <zone>` |

These references do not define one fixed error-string set for all commands. A command failure retains its native error and requested scope. Missing permissions, resources, invalid arguments and throttling do not become empty successful inventories. Retry timing and tenant-wide quota values are unverified here; a throttling response retains any provided retry guidance.

## Patterns

Configuration, effective NIC state, circuit routing tables and backend-health observations answer different questions. A configured backend pool is not evidence that all members are healthy. Each subscription is queried separately; one selected subscription does not enumerate all accessible subscriptions.

## Known limitations

No resource mutation, Front Door routing, Load Balancer per-member health, subnet-utilization calculation or compliance scoring is included. DNS record reads require known zones; zone discovery is not covered here. The NetClaw benchmark identifiers, severities, blanket rate limit and retention threshold were not established by these Microsoft command references and are not carried forward.

Sources: Microsoft's current [network CLI catalog](https://learn.microsoft.com/en-us/cli/azure/network?view=azure-cli-latest), [account](https://learn.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest), [VNet](https://learn.microsoft.com/en-us/cli/azure/network/vnet?view=azure-cli-latest), [NSG](https://learn.microsoft.com/en-us/cli/azure/network/nsg?view=azure-cli-latest), [NIC](https://learn.microsoft.com/en-us/cli/azure/network/nic?view=azure-cli-latest), [ExpressRoute](https://learn.microsoft.com/en-us/cli/azure/network/express-route?view=azure-cli-latest), [VPN connection](https://learn.microsoft.com/en-us/cli/azure/network/vpn-connection?view=azure-cli-latest), [Application Gateway](https://learn.microsoft.com/en-us/cli/azure/network/application-gateway?view=azure-cli-latest), and the catalog's linked command-family references, retrieved 2026-10-09.

## Tools

| Mechanism | Purpose | Category |
|---|---|---|
| Authenticated Azure CLI | Execute the documented read commands in the selected subscription | Read |

## Verification checklist

- Subscription, resource group, region and resource identity accompany each result.
- Continuation tokens were consumed where a bounded list returned them.
- Default NSG rules remain represented when rule evidence is requested.
- Effective state and backend health are distinguished from configuration.
- Unsupported health or compliance conclusions are not inferred.
