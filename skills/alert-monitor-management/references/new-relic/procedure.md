# New Relic — Alert Condition Creation & Issue Acknowledge/Resolve Procedure

Creates an alerting condition on New Relic (an NRQL-based condition attached to an alert policy)
and manages the lifecycle of the issues it raises. Uses NerdGraph, New Relic's GraphQL API, which
is the platform's current, actively-developed interface for alert management — New Relic's own
end-of-life notice for its older REST API v2 (and the parallel `alerts_*` REST endpoints built on
it) confirms that surface is being phased out, with NerdGraph named as the replacement path for
alert configuration and several other alert-adjacent capabilities. Assumes an authenticated
GraphQL client against New Relic's NerdGraph endpoint (a personal API key or equivalent, sent as a
request header) is already available.

Sources (retrieved 2026-09-29): New Relic "REST API v2 and Deployments v0 API,
end-of-life" notice (https://docs.newrelic.com/eol/2026/07/eol-07-31-26-rest-api-v2/); New Relic
"NerdGraph tutorial: NRQL condition alerts" (https://docs.newrelic.com/docs/apis/nerdgraph/examples/nerdgraph-api-nrql-condition-alerts/);
New Relic "Intro to using alerts with our NerdGraph API"
(https://docs.newrelic.com/docs/alerts/scale-automate/nerdgraph/nerdgraph-api-examples/); New
Relic "NerdGraph tutorial: Alert policies" (https://docs.newrelic.com/docs/apis/nerdgraph/examples/nerdgraph-api-alerts-policies/);
New Relic "Acknowledge alert issues" (https://docs.newrelic.com/docs/alerts-applied-intelligence/new-relic-alerts/alert-incidents/acknowledge-alert-incidents/);
New Relic "How alert condition violations are closed" (https://docs.newrelic.co.jp/docs/alerts-applied-intelligence/new-relic-alerts/alert-violations/how-alert-condition-violations-are-closed);
New Relic's published REST API OpenAPI description, for how the older
`alerts_policies`/`alerts_nrql_conditions`/`alerts_violations` REST resources correspond to the
NerdGraph objects and mutations named below.

## Operational procedure — create a monitor (alert policy + NRQL condition)

1. **Confirm or create the containing alert policy.** Every alert condition in New Relic belongs
   to a policy, which also controls how the policy's conditions roll up into incidents
   (`incidentPreference`: per-condition, per-policy, or per-condition-and-target — confirm which
   the caller wants; default to per-condition if unspecified, since that's the narrowest grouping
   and avoids merging unrelated conditions into one incident). If no suitable policy exists yet,
   create one first via the alert-policy-create mutation.
2. **Choose the condition shape.** New Relic's NRQL-condition family includes at least a static
   type (fixed threshold values) and a baseline type (dynamic, deviation-from-trend thresholds).
   Confirm which the caller wants — do not default to baseline for what is actually a simple fixed
   threshold, or vice versa.
3. **Write the NRQL query** that the condition evaluates — this is a real NRQL `SELECT`-style
   query against the caller's data, not free text; confirm the query the caller wants monitored
   rather than inventing one.
4. **Build the condition's terms** — each term defines one threshold: `operator` (e.g. above,
   below, equals), `priority` (severity — critical or warning), `threshold` (the numeric trigger
   value), `thresholdDuration` (how long the condition must hold before it counts as a violation),
   and `thresholdOccurrences` (whether the signal must breach the threshold for the whole duration
   window, or just at least once within it). A condition needs at least one term; a caller who
   wants both a warning and a critical threshold on the same signal needs two terms.
5. **Set signal-processing options as needed** — `aggregationWindow` (how data points are
   batched for evaluation), `aggregationMethod`, and `aggregationDelay` control how New Relic
   processes the underlying data before applying the terms above; only set these if the caller's
   request depends on them (e.g. a known data-delay in their pipeline), otherwise leave New
   Relic's own defaults in place.
6. **Set `violationTimeLimitSeconds`** if the caller wants a cap on how long a single violation
   can stay open before New Relic force-closes it regardless of the signal — this is separate from
   the natural recovery-based auto-close described under "acknowledge/resolve" below.
7. **Submit the create mutation** for the chosen condition type (static or baseline), scoped to
   the target `accountId` and `policyId`. See `endpoints.md` for the literal mutation names and
   argument shape.
8. **Confirm creation** — a successful mutation response returns the created condition object
   including its `id`. Report `CREATED` with that id. On failure, report `FAILED` with the
   GraphQL response's `errors` array verbatim — do not guess at which field was rejected.

## Operational procedure — acknowledge or resolve an issue

1. **Confirm the target is an issue, not a raw violation.** New Relic's newer alerting pipeline
   groups related violations into issues, and acknowledgment/closing operate at the issue level,
   identified by an `issueId`.
2. **Acknowledge marks ownership, nothing else.** New Relic's own documentation is explicit that
   acknowledging an issue indicates the acknowledging user is taking ownership of it — it notifies
   collaborators that someone is handling it, and only one person can hold that acknowledgment at a
   time. It does not silence the underlying condition and does not close the issue. If the caller
   actually wants to stop the condition from generating more issues (rather than just claim this
   one), that's a different action — muting rules or disabling the condition — not covered by
   acknowledge/resolve and out of scope for this skill unless explicitly requested as monitor
   configuration.
3. **Acknowledging cannot be undone once performed**, per New Relic's own documentation — an
   acknowledged issue can later be unacknowledged or closed, but the acknowledgment action itself
   is not reversible as a no-op undo. **Stop and confirm with the operator before acknowledging** if
   there's any doubt about who should be taking ownership, since a second person cannot
   simultaneously acknowledge the same issue.
4. **Submit the acknowledge mutation** with the target `issueId`. See `endpoints.md`. A successful
   response includes `acknowledgedAt` and `acknowledgedBy`. Report `ACKNOWLEDGED`.
5. **Resolving/closing an issue** — New Relic documents both an automatic path and a manual one:
   - **Automatic:** an issue's violations auto-close once the underlying signal returns to a
     non-violating state and holds there for the condition's own recovery period (the same window
     configured via `thresholdDuration`/`thresholdOccurrences` on the term that opened it) — no
     action is required, and this is the expected, normal path to resolution.
   - **Manual:** an issue can be explicitly closed regardless of whether the signal has actually
     recovered. Because this can mask a still-ongoing problem, **stop and confirm with the operator
     before manually closing an issue** whose underlying condition may still be actively breaching.
6. **Submit the resolve/close mutation** with the target `issueId` if manual closure was confirmed.
   Report `RESOLVED` on success, `FAILED` with the GraphQL `errors` array otherwise.

## Patterns

- **NerdGraph mutation names are type-specific for conditions** (`...NrqlConditionStaticCreate` vs.
  `...NrqlConditionBaselineCreate`) — picking the wrong one produces a condition shaped for the
  wrong threshold model, not a validation error necessarily, so confirm the type before submitting.
- **Acknowledge and resolve are genuinely separate mutations on separate concerns** — acknowledging
  never implies resolving, and resolving does not require a prior acknowledgment.

## Known limitations

- The older REST Alerts API (endpoints like `alerts_policies.json`, `alerts_nrql_conditions.json`,
  `alerts_violations.json`) still exists in New Relic's published API surface as of the sources' retrieval date (2026-09-29),
  but New Relic's own end-of-life notice covers the REST API v2 family broadly — treat
  NerdGraph as the durable path for new integration work rather than building against the REST
  surface, even where a REST endpoint still technically responds today.
- Muting rules (suppressing future issues from a condition without closing the current one) are a
  distinct New Relic object from acknowledge/resolve and are out of scope for this skill unless
  requested as explicit monitor configuration — see `SKILL.md`'s "Known limitations."
- The sources do not document a fixed catalog of GraphQL error codes for
  these mutations — surface the `errors` array verbatim on failure rather than fabricating a
  specific cause.

## Tools

| Operation | Description | Category |
|---|---|---|
| `alertsPolicyCreate` | Create the containing alert policy, if one doesn't already exist | NerdGraph — Alerts Policies |
| `alertsNrqlConditionStaticCreate` | Create a fixed-threshold NRQL condition under a policy | NerdGraph — Alerts NRQL Conditions |
| `alertsNrqlConditionBaselineCreate` | Create a dynamic-baseline NRQL condition under a policy | NerdGraph — Alerts NRQL Conditions |
| `nrqlConditionsSearch` / `nrqlCondition` | Look up existing conditions/policies before creating | NerdGraph — Alerts NRQL Conditions |
| Acknowledge issue mutation | Claim ownership of an open issue | NerdGraph — AI Ops Issues |
| Resolve/close issue mutation | Manually close an issue (with confirmation) | NerdGraph — AI Ops Issues |

## Verification checklist

- [ ] Condition type (static vs. baseline) matched what the caller actually needs, not defaulted
- [ ] At least one term (threshold/operator/priority/duration/occurrences) was set deliberately,
      not left to an assumed default
- [ ] `incidentPreference` on the containing policy was confirmed rather than assumed
- [ ] Before acknowledging: confirmed with the operator if ownership is ambiguous (not reversible
      as a no-op)
- [ ] Before manually closing an issue: confirmed with the operator that the underlying condition
      has actually recovered, or that closing without recovery is intentional
- [ ] Outcome reported using this skill's status vocabulary (`CREATED`, `ACKNOWLEDGED`, `RESOLVED`,
      `FAILED`), with the GraphQL `errors` array on failure
