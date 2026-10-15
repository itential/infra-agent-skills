# Zscaler Internet Access (ZIA) — URL/Cloud App Filtering Rule Procedure

Create, update, or delete a URL Filtering rule in a Zscaler Internet Access (ZIA) tenant — the rule
type that governs whether a request to a given URL category, cloud application, protocol, or request
method is allowed, blocked, isolated, or subject to time/size quota for a given set of locations,
groups, departments, users, or time windows. Does not cover ZIA's separate firewall filtering, DLP,
or file-type-control rule families — those are distinct rule objects with their own endpoints and are
out of scope for this procedure.

Sourced from Zscaler's own actively-maintained `zscaler-sdk-go` SDK
(github.com/zscaler/zscaler-sdk-go, package `zscaler/zia/services/urlfilteringpolicies`), which
encodes ZIA's REST endpoint paths, HTTP verbs, and the URL Filtering Rule object's field-level
structure directly from Zscaler's own service definitions, retrieved 2026-09-29. Authentication
details cross-checked against Zscaler's own OneAPI/Zidentity help documentation
(help.zscaler.com/zidentity/understanding-oneapi-authentication), retrieved via search excerpt the
same date since the page itself did not render outside a browser session.

Assumes an authenticated REST client already holding a valid OneAPI access token for the target ZIA
tenant (see `endpoints.md` for how that token is obtained and applied) is available.

## Operational procedure

1. **Confirm the rule action and scope are within this procedure's coverage** — this procedure
   covers URL Filtering rules only (protocol/URL-category/cloud-app match criteria with an
   allow/block/caution/isolate/quota-style action). If the caller is actually describing a firewall
   (network-layer) rule, a DLP rule, or a file-type-control rule, stop: those are separate ZIA rule
   families not covered here.
2. **Resolve any named references to IDs.** Locations, groups, departments, users, time windows, and
   device groups are all referenced in the rule body as ID-bearing objects, not names — if the
   caller supplied names, look up the corresponding IDs via that object type's own list/lookup
   endpoint before building the rule payload. Do not guess an ID.
3. **Determine rule placement (`order`).** ZIA URL Filtering rules are evaluated top-to-bottom and
   stop at the first match — the rule's `order` value determines where it sits in that sequence
   relative to every other URL Filtering rule in the tenant. If the caller has a required relative
   position (e.g. "before the catch-all block rule"), read the current rule list first and compute
   the numeric `order` that achieves it; do not leave `order` unset and assume the platform will
   place it correctly for the caller's intent — an unset or wrong `order` can put a narrower rule
   below a broader one that already catches the same traffic, silently making the new rule
   unreachable.
4. **Build the rule payload** with the fields in `endpoints.md`'s field table. At minimum, a create
   needs `name`, `action`, and at least one match criterion (commonly `urlCategories` and/or
   `protocols`) — a rule with no match criteria at all is not a meaningful policy object and the
   source does not document what a create call does with one, so do not submit one; stop and ask
   for scope criteria instead.
5. **Apply the CIPA-compliance mutual-exclusion constraint**, if `enableCIPACompliance` is being set
   `true` on this rule: the SDK source documents this as incompatible with
   `enableNewlyRegisteredDomains`, `considerEmbeddedSites`, `enforceSafeSearch`, and
   `enableDynamicContentCat` being set on the same rule. If the caller wants CIPA compliance enabled
   alongside any of those, stop and report REJECTED_INVALID_FIELD_COMBINATION rather than submitting
   a call the platform is documented to reject.
6. **Flag isolation actions as requiring a Cloud Browser Isolation (CBI) profile.** If `action` is
   set to the isolate action, a `cbiProfile`/`cbiProfileId` reference is required for the rule to be
   meaningful — the source does not state ZIA enforces this at the API layer, so do not assume a
   missing profile reference will be rejected outright, but flag it to the caller as likely
   non-functional if omitted.
7. **Stop and confirm with the operator before submitting create, update, or delete** — every one of
   these operations changes live enforcement for real user traffic the moment it is applied (see
   Universal concepts in `SKILL.md`). This applies equally to a rule reorder, since reordering can
   change which rule matches first for existing traffic without changing either rule's own fields.
8. **Submit the call** — create, update against the rule's `id`, or delete against the rule's `id`,
   per `endpoints.md`.
9. **Confirm the outcome.** A create/update returning the rule object (with a populated `id` for
   create) is the success signal; a delete returning a success status with no body is the success
   signal for delete. If the calling tool needs a separate confirmation read, fetch the rule by `id`
   and compare the fields just submitted against what was persisted — report CREATED, UPDATED, or
   DELETED accordingly.
10. **Handle failures verbatim.** The source does not document specific error codes/strings for this
    endpoint family beyond the general shape of the SDK returning the HTTP status and response body
    on a non-2xx result. Report FAILED with the underlying response's actual status and body rather
    than inferring a cause not stated in the source.

## Patterns

- **`order` is relative, not absolute-safe.** Because rules stop-on-first-match, the same rule body
  placed at a different `order` value can produce entirely different enforcement outcomes for
  identical traffic. Always treat `order` as a first-class field to reason about, not a value to
  default and forget.
- **Scope fields are ID-object lists, not names.** Every scope dimension (`locations`, `groups`,
  `departments`, `users`, `timeWindows`, `deviceGroups`) is expressed as a list of ID-bearing
  reference objects (commonly an id/name/extensions shape) rather than flat strings — resolve names
  to IDs before building the payload (step 2).
- **`rank` is a distinct concept from `order`.** The source describes `rank` as an administrative
  authority/priority level on the rule, separate from its position in the evaluation sequence — do
  not conflate the two when a caller says "priority."

## Known limitations

- Covers URL Filtering rules only — ZIA's firewall filtering, DLP, and file-type-control rule
  families are separate objects with their own endpoints, not covered here.
- The source used for field-level grounding (Zscaler's own `zscaler-sdk-go` service package) is the
  SDK's typed Go representation of the wire format, not narrative admin-guide prose — where the SDK
  source itself notes a workaround for platform behavior (e.g. a documented gap where reading a
  single rule by its `id` omits the CBI profile for isolate-action rules, requiring a list-all
  fallback to recover
  it), that gap is treated as a real, current platform limitation, not an SDK bug to route around
  silently — surface it if the caller's flow depends on reading `cbiProfile` back immediately after
  create/update.
- Full authentication setup for OneAPI (registering a client ID/secret, enabling OneAPI access for
  the org) is an account-team-gated, non-self-service prerequisite per Zscaler's own OneAPI
  documentation — this procedure assumes that prerequisite and the resulting client credentials are
  already in place; it does not walk through obtaining them.
- This procedure does not cover ZIA's separate Cloud App Control rule family (a related but distinct
  rule object for SaaS/cloud-application-specific actions beyond URL-category matching) — only the
  URL Filtering rule endpoint is in scope.

## Tools

| Operation | Description | Category |
|---|---|---|
| List URL Filtering Rules | Read the current rule order/scope before computing a new `order` or checking for conflicts | URL Filtering |
| Get URL Filtering Rule | Fetch a single rule by ID for confirmation reads | URL Filtering |
| Create URL Filtering Rule | Create a new rule | URL Filtering |
| Update URL Filtering Rule | Update an existing rule by ID | URL Filtering |
| Delete URL Filtering Rule | Remove a rule by ID | URL Filtering |
| Locations / Groups / Departments / Users / Time Windows lookup | Resolve caller-supplied names to the ID-object references the rule body requires | Reference objects |

## Verification checklist

- [ ] Confirmed this is a URL Filtering rule request, not firewall/DLP/file-type-control
- [ ] Every named scope reference (locations, groups, departments, users, time windows, device
      groups) was resolved to an ID before building the payload — none left as a bare name
- [ ] `order` was explicitly computed against the current rule list for any placement-sensitive
      request, not left unset
- [ ] CIPA-compliance mutual-exclusion checked before enabling `enableCIPACompliance` alongside any
      of the four conflicting fields
- [ ] Operator confirmed before create, update, delete, or reorder — all four affect live enforcement
- [ ] Outcome confirmed via the response body (create/update) or success status (delete), not assumed
