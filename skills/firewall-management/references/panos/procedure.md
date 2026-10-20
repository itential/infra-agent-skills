# Palo Alto Networks PAN-OS / Panorama — Firewall Policy Management Procedure

Manages security policy rules, address objects, and (where confirmed below) NAT rules on a PAN-OS
firewall or, for centrally-managed deployments, on Panorama. PAN-OS keeps two configuration layers:
a **candidate configuration** that every write below lands in, and a separately-applied **running
configuration** that a device actually enforces — nothing below takes effect on live traffic until
a commit is issued (see the Commit step). Assumes an authenticated REST client against the target
firewall or Panorama instance, holding an API key already generated for an account with rights to
edit the relevant vsys or device group, is already available. See `endpoints.md` for literal request
paths, methods, and payload shapes behind every operation named here.

Scope note: this procedure covers PAN-OS's newer REST API for object/rule CRUD, and separately notes
where PAN-OS documentation says the REST surface stops short and the older XML API is required
(commit is the main example — see below). Both APIs address the same underlying candidate
configuration, so a REST write and an XML-API commit are part of one coherent workflow, not two
unrelated systems.

## Common Sequences

- **Add a firewall rule on a standalone firewall:** identify scope, create the address objects the
  rule needs, create the security rule, move it to its intended position, commit, poll the commit
  job to a finished successful result.
- **Add a Panorama device-group rule:** identify scope, create address objects at the shared or
  device-group scope, create the pre- or post-rule, move it, commit on Panorama and confirm the job,
  then push to the device group and confirm that job.
- **Remove a rule:** read the rule and its neighbours, confirm with the operator, delete, commit
  (and push on Panorama).

Each step is a named section below; the sequences point into them rather than repeating them.

## Operational procedure

### Identify scope before any call

Every object and rule in PAN-OS is scoped to a location: a firewall's own vsys (`location=vsys`,
naming the vsys), a Panorama-managed shared scope (`location=shared`), or a Panorama device group
(`location=device-group`, naming the group). Confirm which scope the caller intends before issuing
any call — the same object name can exist independently at multiple scopes, and a call that omits or
misstates the scope parameter will operate on the wrong copy, or fail to find an object the caller
expected to see. The valid scope values differ by target: PAN-OS documents `shared`, a vsys, and two
read-only-style locations (predefined and panorama-pushed objects) for a firewall, but only `shared`
and a named device group for Panorama itself — a vsys scope is not addressable on a Panorama
instance. (Source: Palo Alto Networks, "Resource Methods and Query Parameters (REST API)", PAN-OS 11.1
doc set, retrieved 2026-10-19.)

### Create an address object

Submit a create request naming the object's location and name, along with the address type and
value — a network/mask pair, a single host address, an address range, or a fully-qualified domain
name (PAN-OS defines other address-type variants beyond these two; treat any type this procedure
doesn't explicitly cover as needing a documentation check before assuming its request shape matches).
Optional fields include a free-text description and one or more tags for organizing objects in the
PAN-OS UI. A successful create response indicates the command succeeded; PAN-OS does not appear (from
the documentation available for this pass) to distinguish "created new" from "matched existing" the
way some other platforms' identification engines do — treat a name collision at the same scope as
something to check for before creating, not something the API resolves for you silently.

### Read address objects

Read either a single named object or a filtered list at a given scope. A list read returns every
object visible at that scope along with its type-specific value (network/mask, host, etc.) and any
description or tags set on it.

### Update an address object

Submit the full object definition again at the same scope and name to replace it — the update call
uses the same request shape as create, so include every field that should remain, not just the
field being changed, unless the platform's actual replace-vs-merge semantics for this call are
separately confirmed for the field in question.

### Delete an address object

**Stop and confirm with the operator before proceeding.** Removing an address object that a security
rule or NAT rule still references is destructive to that rule's intended matching behavior; PAN-OS
documentation available for this pass did not describe a built-in reference check blocking deletion
of an in-use object, so confirm via a rule/object read that nothing currently depends on the object
before deleting it, and only then submit the delete request naming its scope and name.

### Rename an address object (PAN-OS-specific)

PAN-OS's REST API exposes a dedicated rename action, distinct from a normal update, for changing an
object's name while preserving its definition and location. Use this rather than delete-then-recreate
when only the name is changing, since delete-then-recreate would otherwise require re-pointing every
rule that references the object by its old name.

### Create a security policy rule

Submit a create request naming the rule's location (vsys, shared, or a Panorama device group) and
rule name, along with its match/action fields: source and destination zones, source and destination
addresses, application(s), service(s), user/HIP-profile criteria where used, and the rule's action
(e.g. allow or deny). Panorama deployments additionally support pre-rules and post-rules — rules
evaluated before or after a firewall's own locally-defined rules — as a distinct rule set from a
plain vsys-scoped rule; confirm with the caller which rule set is intended before creating, since
they occupy different positions in the effective policy evaluation order.

### Panorama pre-rules and post-rules

On Panorama the rulebase is split in two: pre-rules run ahead of a firewall's local rules and
post-rules run after them. Each has its own resource family and both are scoped to either `shared`
(applies to every managed device and device group) or one named device group. A rule created without
choosing pre or post lands in the wrong place in the effective order, so decide this per rule before
creation. Palo Alto's REST documentation confirms that Panorama resources cover both pre- and
post-rule variants; the post-rule security family name comes from a secondary source (a third-party
OpenAPI description) and matches that statement (see `endpoints.md`).

### Reorder a rule (Panorama and firewall)

Rules are evaluated in list order, so a newly created rule is only effective once it sits at the
intended position. PAN-OS exposes a dedicated move action on the policy families that places a rule
at the top, at the bottom, or directly before or after a named sibling rule in the same rulebase and
scope. Use it after create instead of delete-and-recreate. A before/after move needs the sibling's
name; a move that names a sibling in a different scope or rulebase is not meaningful, so read the
rulebase first and confirm the target exists. Moving a rule changes which traffic it and its
neighbours match: **stop and confirm with the operator before moving a rule in a rulebase that is
live**, and note that the change only takes effect after commit.

### Read / update / delete a security policy rule

Reads, updates, and deletes for security rules follow the same location+name addressing as address
objects above: a read can target a single named rule or list rules at a scope; an update resubmits
the rule's full field set at the same location and name; a delete removes the rule by location and
name. **Deleting a security rule is destructive to whatever traffic pattern it was permitting or
blocking — stop and confirm with the operator before proceeding**, and confirm the rule's current
position/precedence relative to other rules if order matters to the caller's intent, since removing
one rule can change which rule now matches traffic that used to hit the deleted one first.

### NAT rules

NAT rules follow the same location/name addressing, the same rename and move actions, and, on
Panorama, the same pre-rule/post-rule split as security rules. Palo Alto's REST documentation that
was reachable for this pass names only security rule families, so the NAT family names in
`endpoints.md` come from a secondary source (a third-party OpenAPI description) and are **unverified against
vendor docs**: check them in the target version's own API reference (served by the device itself)
before relying on them. Deleting or reordering a NAT rule changes address translation for live
traffic: **stop and confirm with the operator first.**

### Commit — required before any write takes effect

Every create/update/delete above lands only in the candidate configuration. To apply pending changes
to the running configuration, a commit must be issued; PAN-OS documentation confirms the commit
mechanism supports committing the full pending change set or a scoped/partial commit, but this
procedure's source material did not yield the literal request body or job-status field names for
this pass — those exact mechanics should be confirmed against the target PAN-OS version's own API
reference before an agent relies on a specific field name. What is confirmed and safe to rely on:
commit is a distinct, required step, separate from every object/rule write above, and a commit
returns a job that can be polled for completion using the platform's own operational job-status
query — check that the job finished successfully before reporting a change as fully applied, rather
than reporting success as soon as the commit request was merely accepted.

**Committing applies every pending candidate change at the target scope, not just the one this
procedure just made — stop and confirm with the operator before committing** if other pending,
unrelated changes might exist in the candidate configuration that shouldn't go live yet.

### Push to managed devices — Panorama only, after the Panorama commit

On Panorama, committing publishes the candidate configuration to Panorama's own running
configuration only; managed firewalls keep enforcing their previous policy. A separate push action
sends the committed device-group (shared policy) configuration to the firewalls in a chosen device
group, and returns its own pollable job. Run it only after the Panorama commit job has finished
successfully, and read both job results rather than inferring the second from the first. The push
reaches only firewalls directly attached to the named device group; PAN-OS documents that it does not
automatically cascade to firewalls in child device groups when a parent group changed, so push each
affected child group (the web interface can push to children). **Stop and confirm with the operator
before pushing**: a push changes enforcement on every firewall in the target group at once and
cannot be undone except by pushing a corrected configuration. A validate-only variant checks the
policy without pushing; prefer it first when the operator wants a dry check. Template and template
stack pushes are not covered here (see Known limitations). (Source: Palo Alto Networks, "Commit-All",
PAN-OS XML API request types, retrieved 2026-10-19.)

## Patterns

- **Nothing here takes effect until committed.** A caller reporting "the rule was created" based on
  a successful create-object response alone is describing the candidate configuration, not
  necessarily what the firewall is currently enforcing — always distinguish "written to candidate"
  from "committed and live" when reporting outcomes.
- **Scope (location/vsys/device-group) is part of an object's identity, not just a filter.** The same
  name can exist at multiple scopes simultaneously with different definitions; always carry the
  scope forward from read through update/delete rather than assuming a bare name is unambiguous.
- **Commit and push are two gates on Panorama.** "Committed" means Panorama's running config; devices
  enforce it only after the push job completes.
- **A commit applies everything pending, not a single change.** Treat commit as a shared,
  scope-wide gate rather than a per-object action tied to the one change this procedure made.

## Known limitations

- NAT rule resource family names are taken from a secondary source (a third-party OpenAPI description) and are not
  verified against Palo Alto's own reference — see the NAT rules section.
- Panorama device-group and template management (creating or editing device groups, templates, and
  template stacks) appears in a secondary source but was not verified against Palo Alto
  documentation, so this procedure does not cover it. Template and template-stack pushes, and the
  force-template-values and merge-with-candidate options of the push action, were not detailed in the
  documentation reached; consult the version's XML API reference.
- This procedure covers the newer PAN-OS REST API for object/rule CRUD. PAN-OS documentation states
  the REST API only covers a subset of configuration operations and that some operations (commit
  among them) require the older XML API — confirm which API surface a given PAN-OS/Panorama version
  actually exposes before assuming REST alone is sufficient for the full workflow.
- Address-type variants beyond network/mask, host, range, and FQDN were not independently confirmed
  during this pass — check the target version's documentation before assuming a specific type name
  or field shape for a type not named above.

## Tools

| Operation | Description | Category |
|---|---|---|
| Address object create/read/update/delete/rename | Manage address objects at a given scope | Objects |
| Security rule create/read/update/delete | Manage security policy rules at a given scope, including Panorama pre-/post-rules | Policies |
| Rule move | Reposition a security or NAT rule within its rulebase | Policies |
| NAT rule create/read/update/delete/rename | Same addressing as security rules; family names unverified (see NAT rules) | Policies |
| Commit | Apply pending candidate changes to the running configuration; returns a pollable job | Commit |
| Push to device group | Panorama only: send committed shared policy to a device group's firewalls; returns a pollable job | Commit |

## Verification checklist

- [ ] Target scope (vsys / shared / device-group, and pre-rule vs. post-rule where applicable) was
      confirmed before any create, read, update, or delete call
- [ ] A create response was checked for success rather than assumed; no built-in create-vs-update
      matching was assumed given no such mechanism was confirmed for this platform
- [ ] Delete of any address object or security rule was preceded by a check for existing references
      and by explicit operator confirmation
- [ ] Every write was understood as landing in the candidate configuration only, until a commit was
      issued and its resulting job confirmed successful
- [ ] Commit was not issued without confirming with the operator when unrelated pending changes might
      also be present in the candidate configuration
- [ ] Any NAT rule request was preceded by confirming the NAT resource family name against the target
      device's own API reference
- [ ] On Panorama, pre-rule vs. post-rule was chosen per rule and a new rule was moved to its
      intended position
- [ ] On Panorama, the push job to each affected device group finished successfully after the Panorama
      commit job, and child device groups were pushed separately where needed
