# Zscaler Internet Access (ZIA) — Cloud Firewall Filtering Rule Management Procedure

Manages cloud firewall filtering rules in a ZIA tenant through the ZIA REST API. Rules are stored
in the tenant's configuration and are enforced only after the tenant configuration is activated.
Assumes an authenticated client holding a valid OneAPI access token for the tenant is already
available. See `endpoints.md` for literal request shapes.

Scope note: this covers firewall filtering rules only. ZIA URL filtering, DLP, NAT control and
other rule families are separate objects with their own calls and are not covered. Address, service
and IP-group objects that a rule references are read-only inputs here; this procedure does not
create or edit them.

Sources: Zscaler's zscaler-sdk-go package for ZIA firewall filtering rules (github.com/zscaler),
retrieved 2026-10-26. Behavior not visible in the SDK is marked *(unverified)*: no Zscaler help-portal
page backs it. Wording is original.

## Common Sequences

- Inspect: List rules, then Read rule.
- Create: List rules, Read referenced objects, Create rule, Read rule, Activate configuration,
  Read activation status.
- Update or delete: Read rule, Update rule or Delete rule, Activate configuration, Read activation
  status.

## Operational procedure

### Identify scope before any call

Confirm the tenant and the rule's identifier. Rules are addressed by a numeric id; the name can be
used to find that id by listing, so resolve the name to an id before any change.

### List and read rules

List returns the tenant's rules in order, with optional filtering and paging (the SDK caps a page
at 5000). Read returns one rule by id. A rule may be flagged as predefined or as the default rule;
whether ZIA restricts changing or deleting those was not documented
*(unverified)*, so treat a flagged rule as protected and raise it with the operator before touching
it.

### Create a rule

A rule carries a name, an order (its position in evaluation), a separate administrative rank, a
state (enabled or disabled), an action, and match criteria. Criteria can be inline values (source
and destination addresses, countries, applications) or references to existing objects by id (IP
groups, services, locations, departments, groups, users, devices, time windows, labels). Resolve
every referenced object to its id first by reading it. Field value vocabularies (the action and
state strings) were not enumerated *(unverified)*; read an existing rule and
reuse its exact strings.

Order determines which rule matches first, so read the current list and choose the position
explicitly. What ZIA does when order is omitted *(unverified)*, so do not rely on a default.

**Stop and confirm with the operator before proceeding.** Success is a returned rule record with an
assigned id, confirmed by reading the rule back. The rule is stored but not yet enforced: see
"Activate configuration". If a create call fails ambiguously, list rules and check whether it
landed before retrying.

### Update a rule

The update call takes the complete rule definition for the id. Whether fields left out are kept or
cleared *(unverified)*; send the full intended definition, starting from a fresh read of the rule.

**Stop and confirm with the operator before proceeding.** A changed action, scope or order alters
which traffic is allowed or blocked once activated. Success is the returned record, confirmed by
reading the rule back.

### Delete a rule

**Stop and confirm with the operator before proceeding.** Deletion removes the rule's traffic
handling and changes which later rule matches. Success is a successful delete status; read the rule
or list rules to confirm it is gone. Deletion is also staged until activation.

### Activate configuration

ZIA saves each change to a staged configuration and applies it to live enforcement only when the
tenant configuration is activated; saving and activating are separate calls. Activation is
tenant-wide, not per rule, so it also publishes any other pending changes, including those made by
other administrators.

**Stop and confirm with the operator before proceeding**, naming that scope. Zscaler documents
that activation requests are queued and do not override concurrent edits by other administrators,
and advises activating once after a batch of changes *(Zscaler API getting-started guidance; unverified)*. A conflict reply that the edit lock is unavailable means another
administrator's session holds it: wait a few seconds and retry. A failed activation leaves the
saved rule change in place.

### Read activation status

Read the tenant's activation state and report the returned status string as is. The values are not
enumerated; do not match against a fixed list, and report an unfamiliar or
pending value as unresolved. Report the rule outcome and the activation status as two separate
results.

## Patterns

- **Saved is not enforced.** A successful rule write only means the staged configuration changed.
- **Order is not rank.** They are separate fields; order is evaluation position, rank is an
  administrative priority value. Their exact semantics *(unverified)*; copy from an existing rule
  when unsure.
- **Rate limits and retry behavior are not documented.** On HTTP 429, back off
  and honor any `Retry-After` header.

## Known limitations

- Other ZIA rule families (URL filtering, DLP, NAT control) and creation of referenced objects are
  not covered.
- Action and state vocabularies, update merge-versus-replace behavior, default placement, protected
  rule behavior and error bodies were not verified.
- Rate limits and quotas are not documented here; see Patterns for safe retry behavior.

## Tools

| Operation | Description | Category |
|---|---|---|
| List rules | Retrieve firewall filtering rules | Read |
| Read rule | Retrieve one rule by id | Read |
| Create rule | Stage a new rule | Write |
| Update rule | Stage a replacement of a rule | Write |
| Delete rule | Stage removal of a rule | Destructive |
| Activate configuration | Publish all pending tenant changes | Activation |
| Read activation status | Retrieve the tenant's activation state | Read |

## Verification checklist

- [ ] Rule id, action, state, scope and order match the approved request, read back after the write
- [ ] Every create, update, delete and activation had operator confirmation
- [ ] Activation scope (all pending tenant changes) was stated to the operator
- [ ] Rule write result and activation status reported separately; unresolved status left unresolved
