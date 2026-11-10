# Azure Network Security Groups — Audit

Read every network security group (NSG) in the subscriptions in scope, its rules, and where it is associated, then report exposure, breadth, unassociated groups, shadowed rules, and hygiene. Source: Microsoft Learn "Azure network security groups overview", the Network Security Groups REST reference, and the `az network nsg` reference bound in `endpoints.md` (retrieved 2026-11-10).

Read-only and diagnostic: a decision list keyed by check, no confirmation gates. Nothing is changed or deleted.

## Platform facts the checks rest on

- A rule has a name, a priority from 100 to 4096, a source and destination, a protocol (TCP, UDP, ICMP, ESP, AH, or any), a direction, a port range, and an action of allow or deny. Lower numbers are evaluated first and evaluation stops at the first match, so a later rule that matches the same traffic never applies.
- No two rules in the same direction can share a priority.
- Sources and destinations can be any address, one address, a CIDR range, a service tag, or an application security group. Augmented rules hold several addresses, ranges, and ports in one rule. `VirtualNetwork`, `AzureLoadBalancer`, and `Internet` are service tags, not address ranges. The platform treats `*`, `Any`, and `0.0.0.0/0` as all addresses.
- Every NSG carries default rules at priorities 65000–65500: allow traffic inside the virtual network, allow the Azure load balancer inbound, deny all other inbound, allow outbound to the virtual network and the internet, deny all other outbound. They cannot be removed, only overridden by a rule with a lower number.
- NSGs are stateful. Removing a rule affects new connections only.
- Security admin rules from Azure Virtual Network Manager are evaluated before NSG rules; an "always allow" or "deny" admin rule ends evaluation without the NSG rules being consulted.
- The NSG resource lists its associated network interfaces and subnets.

## Common Sequences

1. **Full audit:** Scope → Read NSGs → run every check → Report.
2. **One NSG:** Read the NSG → run the checks → Report.
3. **Internet exposure only:** Read NSGs → run "Open to the internet" → Report.

## Step 1: Scope

List the subscriptions the credentials can read, limited to the request. Run step 2 once per subscription. A subscription whose read fails or is denied is recorded as not read with the error.

Success: each subscription ends as read or not read.

## Step 2: Read NSGs

List all NSGs in the subscription, following the continuation link to the end. Keep per NSG: name, resource group, location, tags, custom rules, default rules, associated network interfaces, and associated subnets. Rule fields kept: name, priority, direction, access, protocol, source prefix(es), source application security groups, source port range(s), destination prefix(es), destination application security groups, destination port range(s), and description.

Success: the last page carried no continuation link.

## Check A: Open to the internet

For each inbound rule with access allow whose source is all addresses (`*`, `Any`, `0.0.0.0/0`) or the `Internet` service tag:
1. Look at every inbound rule with a lower priority number and access deny in the same NSG. If one matches the same protocol, ports, and destination, the allow never applies; do not report it as exposure, report it under Check D instead.
2. Otherwise classify: administrative port (22 or 3389 in the range); any protocol or a wide port range; other port. Not documented: a list of administrative ports beyond the ones the platform's own samples name; do not invent one, report the port.
3. Name what the exposure reaches: the NSG's associated interfaces and subnets. An NSG with neither reaches nothing through its own association (Check B).

State separately that NSG rules alone do not include security admin rules from Virtual Network Manager; a deny admin rule can block traffic an NSG allows, and an always-allow admin rule can permit traffic an NSG denies. Reading effective rules for an interface is the route to the combined result; no binding is listed for it here, so report that effective exposure was not computed.

## Check B: Unassociated NSGs

Heuristic: the platform documents the association lists on the NSG but no unassociated-NSG check.

Report an NSG whose associated interfaces list and associated subnets list are both empty. It filters nothing today. Report its name, resource group, rule count, and tags. This is a candidate for review, not proof it is unneeded: it may be about to be attached.

## Check C: Broad rules

Heuristic, not a documented platform check.

Report any inbound allow rule with protocol any and a port range of all ports, from any source that is not the `VirtualNetwork` tag, and any allow rule with a very wide port range. Report the same for outbound allow rules to `Internet` with protocol any only when hygiene detail is requested; the default outbound-to-internet rule is not a finding.

## Check D: Shadowed and redundant rules

Within one NSG and one direction, report a rule as shadowed when a rule with a lower priority number covers it: same or broader protocol, a port range that contains it, and a source and destination that contain it. Distinguish:
- same action: the shadowed rule is redundant;
- opposite action: the shadowed rule never takes effect, which is worth an explicit note because the author likely expected it to.

Containment involving service tags or application security groups cannot be judged from the rule alone (their members change); report as "cannot be judged" and give the tag or group. Duplicate priorities cannot occur in one direction.

## Check E: Hygiene

Observations, not documented platform checks.

- Rules with no description.
- NSGs with no tags.
- Rules left over for services that no longer exist cannot be detected from the NSG alone: not documented.

## Patterns

- Default rules are never findings. Do not report `AllowVnetInBound`, `AllowInternetOutBound`, or other priority 65000+ rules.
- An NSG can be associated both to a subnet and to interfaces in it; Check A should name both.
- A rule whose source is the `VirtualNetwork` tag covers the whole virtual network and peered networks, not the internet.

## Known limitations

- Read-only. No rule is edited and no NSG is deleted.
- Azure Firewall, route tables, and Virtual Network Manager configuration are not read.
- How subnet-level and interface-level NSGs combine for one flow: not documented; report both NSGs for the flow.
- Rate limits and throttling behavior: not documented; back off on a throttling response and report any subscription that still fails.
- NSG flow logs retire on 2027-09-30 in favor of virtual network flow logs and new ones can no longer be created, so a missing NSG flow log is not a finding.

## Tools

| Operation | Description | Category |
|---|---|---|
| List network security groups | Subscription-wide list with rules and associations | read |
| Get a network security group | One NSG with rules, default rules, associations | read |
| List network security group rules | Custom rules of one NSG | read |

## Verification checklist

- [ ] Every subscription read to the last page, or recorded as not read with the error
- [ ] Default rules excluded from findings
- [ ] Each exposure hit checked against lower-numbered deny rules in the same NSG and direction
- [ ] Each Check B hit confirmed to have both association lists empty
- [ ] Shadow judgments made only within one NSG and one direction
- [ ] No write call was made
