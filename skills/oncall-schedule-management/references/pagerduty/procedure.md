# PagerDuty legacy on-call schedules

PagerDuty's V2 schedule API maintains layered rotations and overrides, with separate queries for on-call entries and escalation policies.

## Common Sequences

- Inspect coverage: **Locate schedule and policy → Read interval coverage**.
- Maintain rotation: **Locate schedule and policy → Create or update schedule → Read interval coverage**.
- Cover an absence: **Locate schedule and policy → Create overrides → Read interval coverage**.

### Locate schedule and policy

1. Schedule and escalation-policy lists identify the explicitly selected resources. Paginated lists continue while more results remain. Detail reads return schedule layers and policy rules.
2. This procedure applies only to legacy layered schedules. PagerDuty documents V3 shift schedules as incompatible with V2 automation; a V3 target stops this path.
3. At every step, invalid input requires correction, invalid credentials or permissions stop the operation, a missing identifier ends that lookup, and throttling defers requests. The exact error sets and bindings are in [endpoints](endpoints.md). Uncertain writes require a read before repetition.

### Read interval coverage

1. The schedule detail read uses the requested start, end and time zone to obtain rendered layer entries and final coverage. Without an interval, rendered coverage may be absent; absence is not a coverage gap.
2. On-call entries identify users, policies, escalation levels and coverage times. The separate schedule-user query returns users on call during the interval. These results are observations for the requested interval, not a recommendation for who should be scheduled.
3. Success preserves the final schedule and any gaps as returned; list pagination is completed or disclosed.

### Create or update schedule

1. The requested rotation supplies a time zone, ordered users, layer start, effective rotation start and shift duration; restrictions and end are included only when requested. Existing layers are retrieved before replacement.
2. **Repository safeguard: stop and confirm with the operator before proceeding** with creation or updates, including order, times and any replaced layers. Success returns the created or updated schedule. **Read interval coverage** verifies the resulting rotation.
3. Validation errors stop the change. This procedure does not invent shift duration, timezone, restrictions or user order.

### Create overrides

1. Each override contains a user and start/end timestamps. An override created later takes precedence over an overlapping earlier one.
2. **Stop and confirm with the operator before proceeding**, including overlapping coverage that will change. The operation returns a result for each submitted override; each status/error is checked independently rather than assuming the whole batch succeeded.
3. **Read interval coverage** verifies the affected interval. Failed items remain failed; a partial result is reported per override.

## Patterns

- Schedule membership alone does not establish who is on call at a particular time.
- Layer order, user order and time zone influence rendered coverage.
- V3 schedule metadata cannot be substituted into the V2 layered request body.

## Known limitations

No V3 shifts, escalation-policy mutations, schedule deletion, handoff messaging, or organization-specific gap remediation are included.

## Tools

| Operation | Description | Category |
|---|---|---|
| Locate schedules and policies | Retrieve selected configuration | Read |
| Read coverage | Query rendered schedules and on-call users | Read |
| Create or update schedule | Save requested layered rotation | Write |
| Create overrides | Change users covering explicit periods | Write |

## Verification checklist

- The target is a legacy V2 schedule.
- Coverage queries use the requested interval and timezone.
- All override result statuses are checked separately.
- Changed coverage is verified by rendered schedule/on-call results.

Version boundary source: [PagerDuty V3 schedule creation](https://docs.pagerduty.com/developer/api/reference/rest/schedules_v3/create-schedule-v3), retrieved 2026-10-09.


Sources: [PagerDuty REST OpenAPI reference](https://github.com/PagerDuty/api-schema/blob/main/reference/REST/openapiv3.json), REST v2, retrieved 2026-10-09.
