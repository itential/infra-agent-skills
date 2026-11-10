# AWS EC2 Security Groups — Audit

Read every security group in an AWS account, its rules, and the network interfaces that use it, then report exposure, breadth, unused groups, redundancy, and hygiene. Source: Amazon VPC User Guide ("Security groups", "Security group rules", "Default security groups", "Delete a security group", "Associate security groups with multiple VPCs") and the AWS CLI EC2 reference for the describe operations bound in `endpoints.md` (retrieved 2026-11-10).

Read-only and diagnostic: a decision list keyed by check, no confirmation gates. Nothing is revoked, deleted, or detached.

## Platform facts the checks rest on

- A group holds allow rules only; no deny rule exists. A new group has no inbound rules and one rule allowing all outbound traffic.
- A resource with several groups gets the union of all their rules, so a resource is exposed if any one of its groups exposes it.
- A rule's source is an IPv4 or IPv6 range, a prefix list, or another group. A rule that names another group adds none of that group's rules.
- Protocol `-1` means all protocols and allows every port whatever port range is recorded on the rule.
- The default group of a VPC cannot be deleted but its rules can be changed. A resource launched without a group falls back to it. Its stock rules are one inbound rule from itself (all protocols and ports) and outbound rules to all IPv4 (and IPv6, where the VPC has it) addresses.
- A group can be deleted only when no resource uses it, no rule in another group names it, and it is not a default group.
- A group can be associated with more than one VPC in the same Region, and the owner of either side can see the associations.
- Traffic to the VPC DNS resolver, DHCP, instance metadata, the time service, and the VPC router reserved addresses is not filtered by groups.

## Common Sequences

1. **Full account audit:** Scope → Read groups → Read rules → Read usage → run every check (Check C also reads VPC associations, Step 5) → Report.
2. **One group:** Read groups (filtered to the group) → Read rules → Read usage → run the checks → Report.
3. **Internet exposure only:** Read groups → Read rules → run "Open to the internet" → for each hit, Read usage to name what is exposed → Report.

## Step 1: Scope

Security groups are read per Region. List the Regions to audit (all enabled Regions unless the request limits them) and run steps 2–4 once per Region. Record a Region whose read fails or is denied as not read, with the error; continue with the others.

Success: a Region list is fixed, each Region ends as read or not read.

## Step 2: Read groups

List all security groups in the Region, following pages to the end. Keep for each: group ID, name, description, VPC ID, tags, and whether it is the VPC's default group (the group the platform names `default`).

Success: the last page returned no continuation token.

## Step 3: Read rules

For each group, list its inbound and outbound rules. Keep per rule: rule ID, direction, protocol, port range, source or destination (range, prefix list, or referenced group with its VPC and any peering status), and description. The group listing also carries the rules inline; either source works, but use one consistently.

## Step 4: Read usage

List network interfaces in the Region, including interfaces managed by AWS services, following pages to the end. Large accounts must be paged: an unpaged call can fail. For each interface keep its ID, type, status, attached instance if any, VPC, and its list of group IDs. Invert this into a map from group ID to the interfaces that use it.

Success: every interface returned a group list; the map covers the Region.

Gotcha: interfaces that AWS services own (load balancers, endpoints, functions, gateways) are hidden unless the managed-resource option is set. Skipping them makes a group used only by such a service look unused.

## Step 5: Read VPC associations

For each unused candidate from Check C, list the VPC associations of the group. Report an association to a VPC other than the group's own as use that this audit could not see inside, because that VPC's interfaces may belong to another account. If the call's output cannot be interpreted (its fields are unverified), report that associations were not read.

## Check A: Open to the internet

Report an inbound rule whose source is `0.0.0.0/0` or `::/0`. Classify each hit:

1. **Administrative port:** the range includes 22 (SSH) or 3389 (RDP). The platform's own guidance is to allow these only from specific address ranges.
2. **All protocols or a wide range:** protocol `-1`, or a port range spanning many ports. The platform's guidance is not to open large port ranges.
3. **Web port:** 80 or 443 only. This is a normal pattern for a public load balancer, so report it as "confirm intended" and name the resources using the group (Step 4); do not call it a defect.
4. **Other single port or small range:** report with the port and the resources using the group.

Not documented: which other ports count as administrative. Do not invent a list; report the open port and let the operator decide.

Success: every hit lists group ID, rule ID, protocol, port range, source, and the interfaces/instances using the group.

## Check B: All-protocol rules from any source

Heuristic, not a documented platform check; it rests on the stated guidance not to open large port ranges.

Report any inbound rule with protocol `-1`, including those whose source is a single address, a private range, or another group. State that the recorded port range is ignored for such a rule. Sources that are the group itself are the stock default-group rule (Check D), not a separate finding.

## Check C: Unused groups

Heuristic built on the platform's deletion requirements (the platform documents no unused-group check). A group is an unused candidate when all of these hold:
1. No interface in the Region lists it (Step 4).
2. No rule in any group the audit read names it as source or destination.
3. It is not a default group.
4. It has no VPC associations to other VPCs (Step 5).

Items 1–3 are the platform's own deletion requirements; item 4 is added because the platform also refuses to delete an associated group. Report the candidate with its VPC, name, description, and tags, and say it is a candidate: use outside what the read covered is not visible. Unverified: whether resources other than network interfaces (for example launch templates or configurations that name a group) are recorded anywhere this audit reads.

Gotcha: groups shared from another account, or associated to VPCs in another account, can be used by interfaces this account cannot read. Report that the usage read may be incomplete in that case.

## Check D: Default groups

Heuristic, not a documented platform check; it rests on the stated platform guidance to prefer purpose-made groups over the default group.

For each VPC's default group, report (a) any rule beyond the stock ones, (b) whether interfaces use it. Resources land there when no group was chosen at launch, so use by an interface is itself a finding. An unused default group with only stock rules is expected and not reported.

## Check E: Redundant and overlapping rules

Because rules combine additively, a rule adds nothing when another rule in the same group already allows a superset. Within each group and direction, report a rule as redundant when another rule has the same protocol (or protocol `-1`), a port range that contains it, and a source that contains it (a wider range, or the same source). Also report rules that duplicate each other exactly under a different description. Report the pair, naming which rule covers which.

This is derived from the additive evaluation above; the platform documents no redundancy check of its own. A rule that names a group is never judged redundant against a range rule, because group membership and address ranges select different traffic.

Across groups, when one interface lists several groups, report that its effective rule set is the union, and use it when judging exposure (Check A) for that interface.

## Check F: Hygiene

Observations, not documented platform checks. Descriptions and tags are optional features of the platform.

- Rules with no description (the field is optional).
- Groups with no tags.
- A rule naming a group that no longer exists or whose peering connection is gone is marked stale by the platform. Report any rule whose referenced group info lacks the referenced group or shows a peering status that is not an active one. Unverified: the exact peering status values; report the value seen.
- Outbound rule allowing all traffic to all addresses: this is the default on every new group; report it only as an observation and only when asked for hygiene detail.

## Patterns

- Read the exposure and usage together: the same open rule matters more on a group used by an instance than on one used by nothing.
- A group name containing "default" is not the VPC default group; the VPC's default group is the one named `default` that the platform created.
- Rule changes apply to existing resources at once, so findings reflect live exposure.

## Known limitations

- Read-only. No rule is revoked and no group is deleted.
- Network ACLs, route tables, and AWS Network Firewall are not read; a rule judged open here may still be filtered by one of them.
- Rate limits and throttling behavior: not documented; back off and retry on a throttling error, and report any Region that still fails.
- Which actions a read-only credential needs: not documented; report a permission error as not read.

## Tools

| Operation | Description | Category |
|---|---|---|
| List security groups | Groups with inline rules, VPC, tags | read |
| List security group rules | Rules by group, with IDs and referenced-group info | read |
| List network interfaces | Interfaces and their group lists, including AWS-managed ones | read |
| List security group VPC associations | VPCs a group is associated with | read |

## Verification checklist

- [ ] Every Region read to the last page, or recorded as not read with the error
- [ ] Managed interfaces were included in the usage read
- [ ] Each Check A hit names its group, rule, port range, source, and users of the group
- [ ] Each unused candidate was checked against interfaces, referencing rules, default status, and VPC associations
- [ ] Redundant rules were judged only within one group and direction
- [ ] No write call was made
