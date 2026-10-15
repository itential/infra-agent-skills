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

## Operational procedure

### Identify scope before any call

Every object and rule in PAN-OS is scoped to a location: a firewall's own vsys (`location=vsys`,
naming the vsys), a Panorama-managed shared scope (`location=shared`), or a Panorama device group
(`location=device-group`, naming the group). Confirm which scope the caller intends before issuing
any call — the same object name can exist independently at multiple scopes, and a call that omits or
misstates the scope parameter will operate on the wrong copy, or fail to find an object the caller
expected to see.

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

### Read / update / delete a security policy rule

Reads, updates, and deletes for security rules follow the same location+name addressing as address
objects above: a read can target a single named rule or list rules at a scope; an update resubmits
the rule's full field set at the same location and name; a delete removes the rule by location and
name. **Deleting a security rule is destructive to whatever traffic pattern it was permitting or
blocking — stop and confirm with the operator before proceeding**, and confirm the rule's current
position/precedence relative to other rules if order matters to the caller's intent, since removing
one rule can change which rule now matches traffic that used to hit the deleted one first.

### NAT rules — documented gap, do not assume a specific request shape

The PAN-OS documentation available for this research pass covered security policy rule and address
object REST endpoints directly, but did not surface a confirmed NAT-rule-specific REST resource path.
PAN-OS's general policy architecture (the same location/device-group/name scoping, and the same
pre-rule/post-rule split on Panorama) almost certainly extends to NAT rules as a parallel resource
family, but the literal path segment was not independently confirmed for this pass. Treat NAT rule
CRUD as an explicit unknown: consult the target PAN-OS/Panorama version's own current API reference
for the exact NAT resource path before making this call, rather than assuming it mirrors the security
rule path by name alone.

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

## Patterns

- **Nothing here takes effect until committed.** A caller reporting "the rule was created" based on
  a successful create-object response alone is describing the candidate configuration, not
  necessarily what the firewall is currently enforcing — always distinguish "written to candidate"
  from "committed and live" when reporting outcomes.
- **Scope (location/vsys/device-group) is part of an object's identity, not just a filter.** The same
  name can exist at multiple scopes simultaneously with different definitions; always carry the
  scope forward from read through update/delete rather than assuming a bare name is unambiguous.
- **A commit applies everything pending, not a single change.** Treat commit as a shared,
  scope-wide gate rather than a per-object action tied to the one change this procedure made.

## Known limitations

- NAT rule CRUD's exact REST resource path was not confirmed during this research pass — see the
  NAT rules section above. Confirm against the target version's current API reference before use.
- The literal commit request body, response job-ID field name, and exact job-status polling
  parameters were not confirmed during this research pass — the existence and two-stage nature of
  the commit step is confirmed; its exact wire details are not, for this pass.
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
| NAT rule CRUD | Not independently confirmed this pass — see Known limitations | Policies |
| Commit | Apply pending candidate changes to the running configuration; returns a pollable job | Commit |

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
- [ ] Any NAT rule request was preceded by confirming the current, version-specific NAT resource path
      rather than assuming it from the security-rule path's shape
