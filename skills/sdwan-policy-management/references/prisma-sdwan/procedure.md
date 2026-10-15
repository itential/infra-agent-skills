# Palo Alto Networks Prisma SD-WAN — Stacked Path and QoS Policy Lifecycle

Manage stacked path (network) policy and QoS (priority) policy on Prisma SD-WAN: look up a stack or
site, create a policy set, add, edit, and delete its rules, build a stack from one to four ordered
sets, bind the stack to sites, confirm it, then unbind and delete. There is no separate activate
step: a stack takes effect for a site when it is bound to that site.

Written against the Prisma SD-WAN Unified APIs specification (OpenAPI 3.0, "Latest" version label) and
the Prisma SD-WAN Administrator's Guide edition copyrighted 2026, checked 2026-10-14. Each route is
pinned to the newest version the specification lists for it (see `endpoints.md`). Where the sources do
not say how the platform behaves, this file says so instead of filling the gap.

Assumes an authenticated API client for the target tenant is available. How a token is obtained is
described in `endpoints.md` for reference only.

## Scope

In scope: path policy sets, QoS policy sets, their rules, the path and QoS stacks built from them, and
binding those stacks to sites.

Out of scope (see Known limitations): security and NAT stacks, performance policy, the legacy
"original" policy model, and authoring the objects rules refer to (prefixes, network contexts,
applications, circuit categories, service and data-center groups, probe profiles).

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Stand up and apply a new path or QoS policy:** *Look up the target* → *Create a policy set* →
  *Add a rule to a set* (repeat) → *Build a stack* → *Bind a stack to sites* (gated) → *Confirm the
  outcome of a bind or unbind*.
- **Change a rule in a policy that is already live:** *Look up the target* (find which stacks use the
  set and which sites use those stacks) → *Add a rule*, *Edit a rule*, or *Delete a rule* (gated while
  the set is in use) → *Confirm the outcome of a bind or unbind* (status read of the set).
- **Take a policy out of use and remove it:** *Look up the target* → *Unbind a stack from sites*
  (gated; in practice a replacement stack, see that step) → *Confirm the outcome of a bind or unbind*
  → *Delete a stack* (gated) → *Edit a stack* (gated, for each other stack that contains the set) →
  *Delete a policy set* (gated).

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup matched or did not match |
| REJECTED_INVALID_ASSEMBLY | A pre-save check failed; nothing was created or changed |
| SAVED | A create or edit returned success and the read-back matches |
| BOUND / UNBOUND | The site update returned success, a re-read of the site shows the expected stack reference, and every set in the stack reads a completed state (see *Confirm the outcome of a bind or unbind*) |
| BIND_UNCONFIRMED / UNBIND_UNCONFIRMED | The site update succeeded but the site re-read or a set status read did not settle. Say what each read shows |
| DELETED | The delete returned success and a re-read no longer lists the object |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error or a failed status. Include status, and the error codes from the body |

When several sites are bound in one request, report one status per site; never roll them up into a
single BOUND.

## Model in brief

- A **policy set** holds **rules**. Path sets and QoS sets are separate object types with separate
  rule types.
- A **stack** holds one to four policy sets in priority order (first in the list is highest priority;
  the guide describes this as left to right, and the mapping of list position to that order is an
  assumption) plus one required default-rule set. Rules are evaluated by order number; rules with the
  same number fall back to more-specific-wins.
- A **site** carries one path stack reference and one QoS stack reference as fields on the site
  record, so a site can have at most one stack of each type. Binding is editing those fields.
- "Simple" and "advanced" stacks are views in the management console. The API has a single stack
  object; treat a simple stack as a stack with exactly one set (assumption). Whether the platform
  creates that one set for you is not stated, so create the set first.

## Operations

### Look up the target

Binds to: list_sites, read_site, list_policy_stacks, read_policy_stack, list_policy_sets,
read_policy_set, list_policy_rules.

- Resolve names to identifiers by listing; do not guess an identifier. Site listing can also be
  filtered with a query call, but its filter shape is not documented here (unverified), so filter
  client-side.
- For a site, read the record and note its current path stack and QoS stack references and its
  version number (needed for any later update).
- To learn what depends on a set: list stacks and find those whose set list contains it; then find
  which sites reference those stacks. The platform exposes no direct "where used" read in the
  sources, so this is a client-side join.
- Success: FOUND, with identifiers. NOT_FOUND blocks every later step that needs the object.

### Create a policy set

Binds to: create_policy_set, read_policy_set.

- Pick the type (path or QoS). Submit a name (up to 128 characters; the description up to 256), an
  optional description and tags (up to 10).
- **Default-rule sets.** A stack needs one set flagged as its default-rule set. Reuse an existing one
  found in *Look up the target* where possible. Whether creating a set with that flag yields the two
  standard default rules automatically is not stated (unverified); read the set's rules after create
  and report what is there rather than adding them yourself.
- **QoS sets** require business-priority names (at most four) and bandwidth allocation schemes (at
  most four) at create time. Their inner shape is not detailed in the sources beyond field names, so
  copy it from an existing QoS set read with *Look up the target* (assumption). If none exists, stop
  and tell the operator.
- Cloning from another set is offered by the console (from a stacked set or an original set, or from a
  Palo Alto Networks template for QoS). The API has a clone field whose source type is not stated
  (unverified); do not use it unless the caller supplies a verified identifier.
- Success: the call returns the new set; read it back; SAVED.
- Errors: report FAILED with the error codes (listed in `endpoints.md`).

### Edit a policy set's name or description

Binds to: read_policy_set, update_policy_set.

- Read the set, change only the name or description, and submit the whole object with its version
  number. The clone source and the default-rule flag are rejected as read-only on update.
- Success: SAVED once the read-back matches. Errors: FAILED.

### Add a rule to a set

Binds to: read_policy_set, create_policy_rule, read_policy_rule.

- **If the set is used by any stack bound to a site, stop and confirm with the operator before
  adding the rule.** Rules become effective through binding, so a rule added to a set already in use
  is treated as a live change (assumption: the sources do not say whether it is applied at once).
  If the operator declines, report DECLINED and make no call.
- Pre-checks for both types; on any failure report REJECTED_INVALID_ASSEMBLY naming the field:
  - A name is required (up to 128 characters).
  - Order is a number from 1 to 65535, where 1 is highest priority. Send it explicitly; the console
    default is 1024, and the API default when omitted is not stated. Equal numbers fall back to
    more-specific-wins.
  - At most 256 applications. An empty application list means all applications, so leave it empty only
    on purpose.
  - Source and destination prefix, network context, user, group, and device references must already
    exist; resolve each by identifier.
  - User and group matching works only on tenants that support it (the guide limits it to tenant
    service group compatible tenants); if it is refused, report FAILED as read.
  - The applications on offer differ by the site's software release (the guide filters by release
    bands); pick applications that match the release of the sites that will receive the stack.
- Extra pre-checks for a **path rule**:
  - An active path is mandatory; backup and layer-3-failure paths are optional (a layer-3-failure
    path may exist without a backup path).
  - A layer-3-failure path is considered only in the guide's listed conditions: all active and backup
    paths are down (not merely degraded); all of them are up but layer 3 is unreachable and a
    layer-3-failure path is up and reachable; or network asymmetry.
  - Under best-path selection it is used only when every active path is down.
  - If none is defined or available, the device falls back to one of the active paths.
  - A path is an overlay plus a circuit-category label; the same overlay and label pair cannot appear
    twice in one rule.
  - Path selection is either SLA-compliant (any mix of metrics) or best-path (exactly one metric,
    and no backup paths).
  - A "required" service or data-center group cannot be combined with a direct path.
- Extra pre-checks for a **QoS rule**: priority class 1 to 4, and an optional DSCP rewrite from 0 to
  63. Leaving DSCP absent means no marking change in the console; that equivalence in the API is an
  assumption.
- Default rules in a set are system-managed: the sources show errors that block deleting them and
  changing their match fields or enabled flag. Do not try to alter them; add a rule with a lower order
  number to override one. A stack has at least two: the Default Rule catches traffic bound for the Internet and
  the Enterprise Default Rule catches traffic bound for RFC1918 destinations, whenever no explicit rule
  matches.
- Success: the call returns the rule; read it back; SAVED.
- Errors: FAILED with the error codes. A rule rejected because one already exists for the same
  applications is reported as read; the sources do not define the exact overlap test.

### Edit a rule

Binds to: read_policy_rule, update_policy_rule.

- Read the rule, change only what was asked, and submit the whole rule with its version number
  (assumption: the update replaces the saved rule). Apply the same pre-checks as *Add a rule to a set*.
- **If the set is in use by a bound stack, stop and confirm with the operator before submitting.**
  Bulk editing in the console overwrites each rule's own values, so a multi-rule change is a bigger
  live change; confirm once per set and list the rules.
- If the operator declines, report DECLINED and make no call. Success: SAVED. Errors: FAILED.

### Delete a rule

Binds to: read_policy_rule, delete_policy_rule, list_policy_rules.

**Stop and confirm with the operator before deleting.** No restore is described in the sources
(assumption: none), and if the set is in use the removal changes live behavior. If the aim is only to
stop a rule applying, offer disabling it instead through *Edit a rule*, which is reversible; the guide
offers a disable-rule option and the rule carries an enabled flag, but that the flag is the same
switch is an assumption. Default rules cannot be disabled.

- If the operator declines, report DECLINED and make no call.
- Success: DELETED when the call succeeds and the rule is no longer listed. A default rule cannot be
  deleted; report FAILED as read.

### Build a stack

Binds to: list_policy_sets, create_policy_stack, read_policy_stack.

- Needs: a name, one to four existing sets of the matching type in priority order, and one default-rule
  set. For a simple stack use exactly one set.
- Pre-checks (REJECTED_INVALID_ASSEMBLY on failure): every set identifier resolves in the list for the
  matching type; no set appears twice; the count is within 1 to 4; the default-rule set is flagged as
  such. The platform also rejects a second default stack and sets in an invalid state, with codes
  in `endpoints.md`.
- Success: the call returns the stack; read it back and compare the set order; SAVED. Creating a stack
  does not affect any site until it is bound.
- Errors: FAILED with the error codes.

### Edit a stack

Binds to: read_policy_stack, update_policy_stack.

- Read the stack, change only the name, description, set list, or order, and submit the whole object
  with its version number (assumption: the update replaces the saved stack).
- **If any site is bound to the stack, stop and confirm with the operator before submitting.** Changing
  the membership or the order of sets changes which rule wins at every bound site.
- If the operator declines, report DECLINED and make no call. Success: SAVED. Errors: FAILED.

### Bind a stack to sites

Binds to: read_site, update_site.

**Stop and confirm with the operator before binding.** Show each site, the stack it has now (if any)
that will be replaced, and the stack it will receive. Binding changes live path or QoS behavior at the
site. A site holds one stack per type, so a bind replaces the existing reference of that type.

- Make one site update per site. The sources document a bulk site update only for two unrelated profile
  types, not for stack references, so there is no bulk bind here. The console can assign a stack to
  several sites at once; the API call behind it is not documented.
- For each site: re-read the record right before the update, change only the path or QoS stack
  reference, and submit the whole record with its current version number (assumption: the update
  replaces the site record, so omitting a field could clear it).
- When the site picks up the change is not stated for path and QoS stacks (unverified); assume no
  load time.
- If the operator declines, report DECLINED and make no call.
- Success: each update returns the site; continue with *Confirm the outcome of a bind or unbind* per
  site.
- Errors: FAILED with the error codes (invalid stack, missing default stack, policy not allowed on a
  hub site, version mismatch); the conditions behind each are not documented.
- If a later site in the list fails, stop, report each completed site as it is, and let the operator
  decide; do not roll the earlier ones back on your own.

### Unbind a stack from sites

Binds to: read_site, update_site.

**Stop and confirm with the operator before unbinding:** the site loses whatever the stack enforced
until another stack is bound.

- The sources show the stack reference fields and error codes that mention a missing default stack,
  but do not say whether a reference can be cleared. Prefer replacing it with a stack the operator
  names. Clearing the field is unverified: try it only if the operator asks for it explicitly, and
  report FAILED with the response if it is refused.
- If the operator declines, report DECLINED and make no call.
- Success: continue with *Confirm the outcome of a bind or unbind*; the expected reference is the
  replacement stack, or absent for a clear.

### Confirm the outcome of a bind or unbind

Binds to: read_site, read_policy_set_status, read_policy_stack.

The accepted site update only means the record was saved.

- Re-read the site and check the stack reference matches what was intended.
- Read the status of every policy set in the stack (path or QoS route as appropriate), including the
  default-rule set. Six values are documented: three in-progress, one failed, two completed (literals
  in `endpoints.md`). Which completed value means "applied to the site" is not stated, and whether a
  bind changes a set's status is unverified. Report each value as read.
- There is no status route for a stack or for a site's binding in the sources.
- Report BOUND or UNBOUND only when the site reference matches and no set shows the failed value or an
  in-progress value. If any set is still in progress, wait and re-read a few times with a back-off; if
  it never settles, report BIND_UNCONFIRMED or UNBIND_UNCONFIRMED with the values. A failed value is
  FAILED.
- How long to wait is not documented; agree a timeout with the operator.

### Delete a stack

Binds to: list_sites, delete_policy_stack, list_policy_stacks.

**Stop and confirm with the operator before deleting.** No restore is described (assumption: none).

- The stack must not be bound. The platform refuses deleting one in use; unbind from every site first
  (found via *Look up the target*). Its sets are not deleted with it (assumption).
- If the operator declines, report DECLINED and make no call.
- Success: DELETED when the call succeeds and the stack is no longer listed. Errors: FAILED.

### Delete a policy set

Binds to: list_policy_stacks, delete_policy_set, list_policy_sets.

**Stop and confirm with the operator before deleting.** The guide says deleting a security set removes
its rules; assume the same for path and QoS sets (assumption). No restore is described (assumption: none).

- The set must not be in any stack. The platform refuses deleting one in use or in an invalid state;
  remove it from each stack first with *Edit a stack* (gated).
- If the operator declines, report DECLINED and make no call.
- Success: DELETED when the call succeeds and the set is no longer listed. Errors: FAILED.

## Patterns

- **Effect comes from binding, not from saving.** Creating sets, rules, and stacks changes nothing on
  the network until a stack is bound; an edit to anything already bound should be treated as live.
- **Shared sets.** A set may sit in several stacks, so one rule change can reach many sites. Do the
  where-used join in *Look up the target* before editing.
- **Order decides the winner.** Lower rule number wins within a set, and an earlier set wins within a
  stack. Equal rule numbers fall back to the rule with the more specific attributes. For QoS rules the
  guide ranks attributes from highest precedence to lowest: network context, source prefix,
  application, destination prefix. It gives no such ranking for path rules. Re-read the order after any
  change.
- **Disable before delete.** Switching a rule off keeps its definition and can be undone; a delete
  cannot (see *Delete a rule*).
- **Return to the active path.** On devices at release 5.2.1 or later, by default flows move back to
  the active path as soon as it recovers; the sources do not say how to change that, so do not promise
  a different behavior.
- **Optimistic versioning.** Every update carries the object's version number; a mismatch means
  someone changed it. Re-read and redo rather than reusing the old number.
- **Tokens are short-lived.** The specification says tokens last about 15 minutes, so a long job can
  outlive its token; a rejected call after a long gap may be an expired token, so mint a new one.
- **First calls after a token.** The specification claims a profile read is needed right after minting
  a token, otherwise later calls fail with a forbidden error. That claim is not corroborated elsewhere
  in the sources (unverified). If a call is forbidden just after minting, read the profile once and
  retry; report that this happened.
- **Rates.** Rate limits are not documented in the sources (unknown). Back off on an HTTP 429 and
  honor any `Retry-After` header.

## Known limitations

- Covers path and QoS stacks only. Security stacks, NAT stacks, and performance stacks use the same
  stack-and-bind idea and the site record has matching fields, but they are not covered here.
- Does not cover the legacy "original" policy model (the specification's earlier policy-set routes),
  which the guide says must be converted to stacked policy before devices are upgraded to
  the 6.0.1 software line or beyond.
- Does not author prefixes, network contexts, applications, circuit categories, service and
  data-center groups, probes, DSCP or capacity settings; rules only reference them.
- Not stated in the sources: how a site update applies a stack reference, whether a reference can be
  cleared, what a stack-level or bind-level status looks like, which completed set status means the
  policy is applied, what generates the default rules for a new default-rule set, the clone source
  type, rate limits, and the API default order number.
- **A bound stack changes live behavior until it is unbound,** and deletes are treated as permanent.

## Tools

| Operation | Description | Category |
|---|---|---|
| authenticate | Obtain a bearer token for the tenant (reference only) | Auth |
| read_profile | Read the caller's profile (assumed warm-up call, unverified) | Read |
| list_sites / read_site | Find sites and read one with its stack references | Read |
| update_site | Replace a site record (used to bind or unbind) | Write (gated) |
| list_policy_sets / read_policy_set | List or read path or QoS sets | Read |
| read_policy_set_status | Read a set's processing status | Read |
| create_policy_set | Create a path or QoS set | Write |
| update_policy_set | Replace a set's name or description | Write |
| delete_policy_set | Delete an unused set | Write (gated) |
| list_policy_rules / read_policy_rule | List or read the rules in a set | Read |
| create_policy_rule | Add a rule to a set | Write (gated if set in use) |
| update_policy_rule | Replace a rule | Write (gated if set in use) |
| delete_policy_rule | Delete a rule | Write (gated) |
| list_policy_stacks / read_policy_stack | List or read path or QoS stacks | Read |
| create_policy_stack | Create a stack from ordered sets | Write |
| update_policy_stack | Replace a stack | Write (gated if bound) |
| delete_policy_stack | Delete an unbound stack | Write (gated) |

## Verification checklist

- [ ] Every referenced set, prefix, context, and application was read and exists
- [ ] Rule order is explicit and within 1 to 65535; the path and QoS pre-checks passed
- [ ] The stack has one to four distinct sets of the matching type and a default-rule set
- [ ] The where-used join was done before any edit or delete, and the operator confirmed every gated
      step
- [ ] The site was re-read before each bind or unbind and updated with its current version number
- [ ] After a bind or unbind, the site reference was re-read and every set status was read and reported
      as returned
- [ ] Each site in a multi-site bind has its own reported status
