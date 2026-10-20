# AWS Network Firewall — Firewall Policy Management Procedure

Manages the rule groups and firewall policies of an AWS Network Firewall, AWS's managed stateful
network firewall and intrusion detection/prevention service for VPCs. Assumes an authenticated
client for the AWS Network Firewall API (credentials with rights to manage rule groups and policies
in the target region) is already available. See `endpoints.md` for the literal calls.

Scope note: this platform's object model is **not** the rule-list-plus-address-object shape of the
other vendors here. There are no standalone address objects or NAT rules. Instead:

- A **rule group** is a reusable set of rules, either stateless (priority-ordered match/action
  rules) or stateful (Suricata-compatible rules, domain lists, or simple 5-tuple rules), with a
  fixed **capacity** chosen at creation.
- A **firewall policy** lists the rule groups to apply and sets default actions.
- A **firewall** attaches one policy to a VPC through subnets, one per Availability Zone.

Sources: AWS, "AWS Network Firewall Developer Guide" and "AWS Network Firewall API Reference"
(docs.aws.amazon.com/network-firewall), retrieved 2026-10-19. Wording is original.

## Operational procedure

### Identify scope before any call

Confirm the AWS region (and account) first. Rule groups and policies are regional resources; the
same name can exist independently in other regions. Names cannot be changed after creation.

### Create a rule group

1. Decide stateless vs. stateful and the rule-group **capacity**. Capacity is fixed at creation
   and can never be raised later, nor exceeded by an update, so size it with headroom. The API's
   dry-run mode on create can report the capacity a rule set would need without creating anything.
2. Submit the create call with the name, type, capacity, and rule definition. Use a dry run first
   when the platform offers it for the call.
3. Record the returned update token and ARN; policies reference the rule group by ARN.

### Read rule groups and policies

List by scope to find names/ARNs, then describe one to get its full definition plus the current
**update token**. A describe response is the only source of a valid token for the next update.

### Update a rule group or policy

Updates are optimistic-locked: pass the update token from the latest describe. If someone else
changed the resource since, the call fails with a stale-token error — re-describe and retry; do
not reuse the old token. An update replaces the definition, so send the complete intended content.

**A rule group update takes effect for every firewall policy that references it, and so for every
firewall using those policies. Stop and confirm with the operator before updating a rule group
that more than one policy references** (find referencing policies by reading policies first).

### Attach a rule group to a policy

Add the rule group's ARN (with a priority, for stateful-ordered or stateless groups) to the policy
via a policy update using the current token. This is the step that makes a new rule group
influence traffic; creating a rule group alone enforces nothing.

### Delete a rule group or policy

**Stop and confirm with the operator before proceeding.** Unlike most vendors in this skill, the
platform does enforce a reference check: deleting a rule group still used by a policy, or a policy
still associated with a firewall, is rejected as an invalid operation. Do not work around the
rejection by detaching without confirmation — detaching changes live traffic handling. A firewall
or policy may also have delete/change protection enabled; that must be turned off deliberately,
which is itself a step needing operator confirmation.

### Confirm the change is live

A write returns before it is enforced. Configuration propagates to each AZ's firewall endpoint
asynchronously. Describe the firewall and check its configuration sync state: pending means still
propagating, in-sync means applied everywhere, capacity-constrained means some endpoint couldn't
take the change. The firewall status itself is provisioning, deleting, ready, or failed, and ready
requires in-sync plus all endpoints ready. Report "applied" only when sync state is in-sync.

## Patterns

- **Writes are immediate, enforcement is eventually consistent.** There is no candidate/commit
  stage; poll sync state instead of assuming the call's success means live.
- **Token discipline.** Always describe immediately before updating; treat a stale-token error as
  a normal retry, not a failure.
- **Shared blast radius.** Rule groups are shared across policies; the unit of impact is every
  referrer, not the object edited.

## Known limitations

- No standalone address objects, service objects or NAT rules exist here; requests for those must
  be mapped to rule definitions (e.g. IP sets/variables inside a stateful rule group) or declined.
  Rule-variable and Suricata rule syntax details were not covered this pass; check the vendor
  guide for the rule string format.
- Capacity sizing numbers per rule type were not captured; use the dry-run capacity report.
- Firewall creation, subnet/endpoint management, logging and TLS inspection are out of scope.
- Cross-account sharing of rule groups (AWS RAM) was not verified.

## Tools

| Operation | Description | Category |
|---|---|---|
| Rule group create/read/update/delete | Manage stateless/stateful rule groups | Policies |
| Firewall policy create/read/update/delete | Manage policies and their rule-group references | Policies |
| Firewall describe | Read sync state and status | Verification |

## Verification checklist

- [ ] Region confirmed before any call
- [ ] Capacity sized (dry run where available) before creating a rule group
- [ ] Update token came from a describe made just before the update
- [ ] Operator confirmed before updating a shared rule group or deleting any rule group/policy
- [ ] Change reported live only after the firewall's sync state read in-sync
