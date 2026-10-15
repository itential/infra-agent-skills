# Endpoints — New Relic Alert Condition Creation & Issue Acknowledge/Resolve

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever
GraphQL client/adapter is assumed available. All calls are POSTs to New Relic's single NerdGraph
endpoint, distinguished by the GraphQL `mutation`/`query` body sent, not by URL path.

## NerdGraph endpoint

```
POST https://api.newrelic.com/graphql
```

(EU-region accounts use New Relic's documented EU NerdGraph host instead.) Every request carries
the caller's New Relic API key in an `Api-Key` header. Body is a standard GraphQL request:
`{"query": "<mutation or query text>", "variables": {...}}`.

## Create an alert policy

**Mutation:** `alertsPolicyCreate`

**Arguments:**
- `accountId` (required) — target account.
- `policy` (required) — object with:
  - `name` (required)
  - `incidentPreference` — one of `PER_CONDITION`, `PER_POLICY`, `PER_CONDITION_AND_TARGET`.

**Returns:** the created policy object, e.g. requestable fields `id`, `name`,
`incidentPreference`.

## Create a static NRQL condition

**Mutation:** `alertsNrqlConditionStaticCreate`

**Arguments:**
- `accountId` (required)
- `policyId` (required)
- `condition` (required) — object with at minimum:
  - `name`
  - `enabled` (boolean)
  - `nrql` — object with `query` (the NRQL string) and optionally `dataAccountId` for
    cross-account queries.
  - `terms` — array of term objects, each with `threshold`, `operator` (e.g. `ABOVE`, `BELOW`,
    `EQUALS`), `priority` (`CRITICAL` or `WARNING`), `thresholdDuration` (seconds),
    `thresholdOccurrences` (`ALL` or `AT_LEAST_ONCE`).
  - `signal` — object with `aggregationWindow`, `aggregationMethod` (e.g. `EVENT_FLOW`),
    `aggregationDelay`.
  - `valueFunction` — e.g. `SINGLE_VALUE`, static-condition-specific.
  - `violationTimeLimitSeconds` — auto-close cap for a single open violation.

**Returns:** the created condition object including `id`.

## Create a baseline NRQL condition

**Mutation:** `alertsNrqlConditionBaselineCreate`

Same argument shape as the static-create mutation above, with `baselineDirection` (e.g.
`UPPER_ONLY`) in place of `valueFunction`.

## Look up existing policies/conditions

**Queries:** `nrqlConditionsSearch` (accepts a `searchCriteria` filter by name or policy ID),
`nrqlCondition` (single condition by ID). Policy lookup is documented as available through
NerdGraph's account/policy query fields (consult the NerdGraph GraphiQL explorer's schema browser
for the exact current field path against the target account, since New Relic does not publish a
fixed REST-style path for this).

## Acknowledge an issue

**Mutation:** `aiIssuesAckIssue`

**Arguments:** `issueId` (required).

**Returns:** issue fields including `acknowledgedAt`, `acknowledgedBy`.

**Note:** New Relic's AI Ops issue mutations require an experimental opt-in header on the request
(consult the current NerdGraph documentation/GraphiQL explorer for the exact header name and value
at call time, since experimental-API opt-in mechanics are the kind of detail that changes without
a corresponding doc-page rewrite).

## Unacknowledge an issue

**Mutation:** `aiIssuesUnackIssue`

**Arguments:** `issueId` (required).

## Resolve/close an issue

**Mutation:** `aiIssuesResolveIssue`

**Arguments:** `issueId` (required).

**Failure handling:** GraphQL responses return HTTP 200 even for query/mutation-level errors;
check the response body's `errors` array rather than relying on HTTP status alone. Surface that
array verbatim on failure.
