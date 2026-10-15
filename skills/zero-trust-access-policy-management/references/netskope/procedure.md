# Netskope — Private Access (NPA) Policy Rule Procedure

Create, update, or delete a Netskope Private Access (NPA) policy rule via Netskope's REST API v2 —
the rule type that determines which users/groups/organizational units, under which device-posture
conditions, may reach which private applications (published through Netskope publishers). Netskope's
REST API v2 also exposes other, separate policy-rule families (real-time/CASB inline rules,
internet-access rules, SaaS Posture Management policies) that share the general "policy" naming but
are distinct endpoints with different field shapes; this procedure covers the NPA family only.

Sourced from Netskope's own official documentation page "NPA Real-Time Policy REST API" at
docs.netskope.com/en/private-access-rest-apis/ (retrieved 2026-09-29), which documents the `/policy/
npa/rules` endpoint family directly. Netskope's REST API v2 overview page
(docs.netskope.com/en/rest-api-v2-overview-312207, retrieved the same date) was used only for the
shared authentication-header convention, since it does not itself describe NPA-specific fields.

Assumes an authenticated REST client already holding a valid Netskope API v2 token for the target
tenant is available (see `endpoints.md` for the header format).

## Operational procedure

1. **Confirm this is an NPA policy-rule request.** If the caller is actually describing a real-time
   (CASB inline) rule, an internet-access rule, or a SaaS Posture Management policy, stop: those are
   separate endpoint families under Netskope's REST API v2 and are not covered by this procedure.
2. **Resolve every referenced object to an ID/name reference the API expects**, before building the
   payload: private apps (`privateApps`), private-app tags (`privateAppTagIds`), publishers
   (`publishers`), users, user groups (`userGroups`), and organizational units
   (`organization_units`). If the caller supplied a value that isn't already the exact identifier the
   NPA rule endpoint expects, resolve it via that object type's own lookup endpoint first (private
   apps, publishers, and groups each have their own list endpoints elsewhere in the API) rather than
   guessing a name-to-ID mapping.
3. **Confirm the fixed/required fields are set correctly:** `policy_type` is a fixed value
   identifying this as a private-app policy — do not vary it. `rule_name` and `enabled` are required
   on create. `access_method` determines whether the rule applies to client-based or clientless
   (browser) access — confirm which the caller intends, since scope/action fields can behave
   differently depending on this choice per the documented access-method distinction.
4. **Build `rule_data`** as the structured object carrying the actual match/action configuration —
   source/access criteria (`users`, `userGroups`, `organization_units`,
   `device_classification_id`), destination criteria (`privateApps`, `privateAppTagIds`,
   `publishers`), and the rule's action fields (`match_criteria_action` for the primary allow/block
   decision, plus optional `dlp_actions`/`tss_actions` for data-loss-prevention and threat-scanning
   controls layered onto the same rule). Do not submit a rule with an empty `rule_data` — the
   documentation frames this object as the rule's actual policy content, not an optional extra.
5. **Determine rule placement.** Netskope's own documentation describes an optional `rule_order`
   directive taking a placement mode (top/bottom/before/after) rather than a bare numeric position —
   if the caller has a required relative position, resolve which existing rule (by ID) the new rule
   must sit before/after, and set `rule_order` accordingly rather than leaving placement to
   whatever the platform defaults to.
6. **Stop and confirm with the operator before submitting a create, update, or delete** — every one
   of these changes live private-app reachability the moment it is applied (see Universal concepts
   in `SKILL.md`).
7. **Submit the call** — create, partial update against the rule's `id`, or delete against the rule's
   `id`, per `endpoints.md`. Note that update is documented as a partial update, not a full replace —
   only the fields included in the request body are changed; omitted fields retain their current
   value, so do not assume an update payload needs to restate the entire rule.
8. **Confirm the outcome.** Treat a successful create/update response containing the rule object
   (with a populated `id` on create) as the success signal; treat a successful delete status as the
   success signal for delete. If the calling tool needs a separate confirmation read, fetch the rule
   by `id` and compare the fields just submitted against what was persisted.
9. **Handle failures verbatim.** The source page references Netskope's own Swagger/OpenAPI UI for the
   full payload and response shape but does not itself enumerate specific error codes or strings for
   this endpoint — report FAILED with the underlying response's actual status and body rather than
   inferring an undocumented cause.

## Patterns

- **`rule_data` carries the real policy content; top-level fields are metadata/placement.** Treat
  `rule_name`, `enabled`, `access_method`, `policy_type`, `group_id`/`group_name`, `description`, and
  `rule_order` as the rule's identity/placement/grouping metadata, and everything that actually
  determines who can reach what as living inside `rule_data`.
- **Update is partial, not a full replace.** Submitting only the changed fields is correct and
  expected — do not read the fields back and resend the entire object unless the caller specifically
  wants to confirm the full resulting state.
- **`rule_order` is directional, not a bare index.** Placement is expressed as a mode
  (top/bottom/before/after) plus, where applicable, a reference rule ID — not a raw integer position
  to compute independently.

## Known limitations

- Covers the NPA (Netskope Private Access) rule family only — Netskope's real-time/CASB inline
  rules, internet-access rules, and SaaS Posture Management policies are separate endpoint families
  (their literal routes are listed in `endpoints.md`) with their own field
  shapes, not covered here.
- Does not cover defining the private application, publisher, or private-app tag objects a rule
  references as their own standalone lifecycle — this procedure assumes they already exist and are
  resolved to the identifiers the rule body expects (step 2).
- The source page for this procedure documents the endpoint shape and field list but does not
  enumerate specific error codes/strings — step 9's "handle verbatim" guidance reflects that gap
  rather than an assumption that no such documentation exists elsewhere; if the calling tool
  surfaces Netskope's own Swagger UI for the target tenant, prefer whatever error detail it returns
  live over anything not stated here.
- Netskope's internet-access rule family (a separate, related policy type also under `/policy/`) is
  documented elsewhere as having an explicit separate "deploy" step after a rule create/update before
  it takes effect — the NPA family's own documentation does not describe an equivalent staged-deploy
  step, so this procedure treats NPA create/update/delete as immediately effective per the Universal
  concepts in `SKILL.md`. If a future check of Netskope's NPA documentation finds a staged-deploy step
  was added, that is a correction to make here, not a footnote.

## Tools

| Operation | Description | Category |
|---|---|---|
| List NPA Policy Rules | Read current rules/order before computing placement or resolving conflicts | Private Access (NPA) |
| Get NPA Policy Rule | Fetch a single rule by ID for confirmation reads | Private Access (NPA) |
| Create NPA Policy Rule | Create a new rule | Private Access (NPA) |
| Update NPA Policy Rule | Partially update an existing rule by ID | Private Access (NPA) |
| Delete NPA Policy Rule | Remove a rule by ID | Private Access (NPA) |
| Private App / Publisher / Tag / Group lookup | Resolve caller-supplied names to the identifiers `rule_data` expects | Reference objects |

## Verification checklist

- [ ] Confirmed this is an NPA policy-rule request, not real-time/internet-access/SPM
- [ ] Every referenced object (private apps, tags, publishers, users, user groups, organizational
      units) was resolved to the identifier the API expects — none left as an unresolved name
- [ ] `access_method` (client vs. clientless) confirmed with the caller
- [ ] `rule_data` built with the actual match/action content — not submitted empty
- [ ] `rule_order` set explicitly (mode + reference rule where applicable) for any placement-sensitive
      request
- [ ] Operator confirmed before create, update, or delete — all three affect live reachability
- [ ] Outcome confirmed via the response body or success status, not assumed
