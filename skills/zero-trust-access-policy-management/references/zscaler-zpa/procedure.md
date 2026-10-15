# Zscaler Private Access (ZPA) — Access Policy Rule Procedure

Create, update, or delete an access policy rule in a Zscaler Private Access (ZPA) tenant — the rule
type that determines which users/groups/posture-qualified clients are permitted to reach which
application segments or segment groups. ZPA groups its various rule types (access, timeout, client
forwarding, inspection, isolation, and others) under one generic "policy set" object model
distinguished by a `policyType`; this procedure covers only the access-policy type. Does not cover
defining the application segments or segment groups themselves as standalone objects, or any other
ZPA policy type.

Sourced from Zscaler's own actively-maintained `zscaler-sdk-go` SDK
(github.com/zscaler/zscaler-sdk-go, package `zscaler/zpa/services/policysetcontroller`), which
encodes ZPA's REST endpoint paths, HTTP verbs, and the policy rule object's field-level structure
directly from Zscaler's own service definitions, retrieved 2026-09-29. Cross-checked against
Zscaler's own "Configuring Access Policies" and "Configuring Access Policies Using API" help-portal
page titles (help.zscaler.com/zpa/configuring-access-policies,
help.zscaler.com/zpa/configuring-access-policies-using-api) for the conceptual model (role-based
access, default-deny posture) — those pages did not render outside a browser session at retrieval
time, so the wire-level detail below is grounded in the SDK source, not page text.

Assumes an authenticated REST client already holding a valid OneAPI access token for the target ZPA
tenant, and the target customer's `customerId`, are available (see `endpoints.md`).

## Operational procedure

1. **Confirm this is an access-policy request.** ZPA's policy set model covers several distinct
   policy types under the same generic rule endpoint shape — access, timeout, client forwarding,
   inspection, isolation, and others. If the caller is actually describing one of those other policy
   types, stop: this procedure covers the access-policy type only.
2. **Resolve the access policy set's ID** for the target customer — the source models rule
   create/update/delete/reorder as operating on rules nested under a specific `policySetId`, so the
   access policy set's own ID must be looked up (by its known `policyType`) before any rule
   operation.
3. **Resolve every referenced object to an ID.** ZPA access policy rule scope is expressed as a list
   of `conditions`, each built from boolean operands referencing objects like application segments,
   segment groups, user groups, SAML/SCIM attributes, or posture profiles by ID — not by name. If the
   caller supplied names, resolve them via each object type's own list/lookup endpoint first. Do not
   guess an ID.
4. **Understand ZPA's default-deny posture before writing the rule.** Per Zscaler's own conceptual
   documentation, ZPA denies access to application segments and segment groups by default until an
   access policy rule explicitly permits it — creating an access-policy rule is therefore normally an
   allow action for specific scope, not a narrowing of an already-open default. Confirm with the
   caller whether the intent is "add another explicit allow" versus "this is meant to be the only
   path in," since the default-deny baseline means omission, not an explicit deny rule, already
   blocks everything not otherwise permitted.
5. **Build the `conditions` structure** per `endpoints.md` rather than flat scope fields — each
   condition is an operator (e.g. AND/OR semantics between operand groups) over a set of operands
   naming an object type and its resolved ID(s). Malformed or empty operands are a documented
   source of update failures (the SDK source normalizes/clears certain operand fields before
   submission as a workaround) — build conditions deliberately rather than passing through
   caller-supplied structures unchanged.
6. **Determine rule placement.** ZPA access rules evaluate in order; a new rule's position relative
   to existing ones is set at create time and can subsequently be changed with a dedicated reorder
   call (single-rule or bulk). If the caller has a required relative position, read the current rule
   order first (list rules by policy type) and compute the intended `ruleOrder`/reorder target rather
   than leaving placement to an unverified default. Note that the SDK source documents a bulk-reorder
   behavior that keeps any rule named as the default rule pinned at the end of the order — account
   for that when computing a bulk reorder that includes a default rule.
7. **Stop and confirm with the operator before submitting create, update, delete, or reorder** —
   every one of these changes live reachability for real users and application segments the moment
   it is applied (see Universal concepts in `SKILL.md`), and a reorder alone can change which rule
   matches first for existing traffic without changing any rule's own fields.
8. **Submit the call** — create under the policy set, update against the rule's `id`, delete against
   the rule's `id`, or reorder via the dedicated reorder call, per `endpoints.md`.
9. **Confirm the outcome.** A create/update returning the rule object (with a populated `id` for
   create) is the success signal; delete and reorder are confirmed by a success status. If the
   calling tool needs a separate confirmation read, fetch the rule by `id` (or re-list the policy
   set's rules for a reorder) and compare against what was submitted — report CREATED, UPDATED,
   DELETED, or REORDERED accordingly.
10. **Handle failures verbatim.** The source notes that ZPA enforces its own internal API
    restrictions preventing concurrent write operations on the same policy set (the SDK serializes
    create/update/delete/reorder calls with a mutex specifically because of this) — a failure that
    looks like a conflict/lock condition on a rapid sequence of writes is plausible and expected;
    report the underlying response's actual status and body rather than inferring an unstated cause.

## Patterns

- **Conditions, not flat fields, express scope.** Unlike a platform with flat "groups"/"users" list
  fields, ZPA's rule scope is a structured `conditions` tree of operator/operand pairs — treat this
  as the rule's actual match logic, not an implementation detail to flatten away.
- **Reorder is a separate concern from update.** Changing a rule's fields (update) and changing its
  position (reorder) are two different documented endpoints — do not assume updating the rule itself
  repositions it, or that a reorder call is also the place to change rule fields.
- **String-typed fields that look numeric/boolean.** The SDK source types `priority`, `ruleOrder`,
  and `disabled` as strings, not integers/booleans, in the wire format — pass them as strings, not
  native numeric/boolean JSON types, when building a request by hand.

## Known limitations

- Covers the access-policy type only — ZPA's other policy set types (timeout, client forwarding,
  inspection, isolation, and others) share this same generic rule endpoint shape but have different
  condition vocabularies and semantics not covered here.
- Does not cover creating the application segments or segment groups a rule references as standalone
  objects — this procedure assumes they already exist and are resolved to IDs in step 3.
- The conceptual "default-deny" framing in step 4 is drawn from Zscaler's own help-portal page
  *titles* and general product description, not page body text (the pages themselves did not render
  at retrieval time) — treat it as a well-established ZPA design principle worth flagging to the
  caller, not a word-for-word documented guarantee; verify against the target tenant's actual
  observed behavior if precision matters.
- Full authentication setup for OneAPI (registering a client ID/secret, enabling OneAPI access for
  the org) is an account-team-gated, non-self-service prerequisite — this procedure assumes that
  prerequisite and the resulting client credentials are already in place.

## Tools

| Operation | Description | Category |
|---|---|---|
| Get Policy Set by Type | Resolve the access policy set's ID for the customer | Policy Sets |
| List Rules by Policy Type | Read current rule order/scope before computing placement or checking conflicts | Policy Sets |
| Get Rule | Fetch a single rule by ID for confirmation reads | Policy Sets |
| Create Rule | Create a new access policy rule under the resolved policy set | Policy Sets |
| Update Rule | Update an existing rule by ID | Policy Sets |
| Delete Rule | Remove a rule by ID | Policy Sets |
| Reorder Rule (single) | Move one rule to a new position | Policy Sets |
| Reorder Rules (bulk) | Reposition multiple rules in one call | Policy Sets |
| Application Segment / Segment Group / user-attribute lookup | Resolve caller-supplied names to the IDs `conditions` operands require | Reference objects |

## Verification checklist

- [ ] Confirmed this is an access-policy request, not another ZPA policy set type
- [ ] The access policy set's ID was resolved for the target customer before any rule operation
- [ ] Every object referenced in `conditions` (application segments, segment groups, user
      attributes, posture profiles) was resolved to an ID — none left as a bare name
- [ ] Default-deny baseline discussed with the caller so the rule's intent (add an allow vs. sole
      path in) is unambiguous
- [ ] Rule placement (`ruleOrder`/reorder target) was explicitly computed against the current list
      for any placement-sensitive request
- [ ] Operator confirmed before create, update, delete, or reorder — all four affect live reachability
- [ ] Outcome confirmed via the response body or success status, not assumed
