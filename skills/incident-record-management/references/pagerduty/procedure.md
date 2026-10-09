# PagerDuty incident records

PagerDuty REST v2 maintains incidents, their alerts and notes, and explicit responder requests.

## Common Sequences

- Investigate: **Find incidents → Inspect evidence**.
- Create or update: **Find incidents → Create or change an incident → Inspect evidence**.
- Coordinate: **Find incidents → Request responders or add a note → Inspect evidence**; an explicitly requested consolidation uses **Merge incidents** after inspection.

### Find incidents

1. The list operation selects native status, urgency, service, team and a timestamp interval supplied by the request. The default interval is one month; the documented bounded interval cannot exceed six months. The all-dates option ignores interval filters. Pagination continues while the response indicates more records.
2. The detail operation accepts the selected incident identifier or number and returns its current state. An assigned-user filter cannot locate resolved incidents, because those incidents no longer have current assignees.
3. At this step and every subsequent operation, bad input is corrected, authentication or access failures stop execution, missing resources end that lookup, account-entitlement failures are disclosed, and throttling defers further calls. Documented bindings and operation-specific error sets are in [endpoints](endpoints.md). Unexpected failures preserve the error and incomplete outcome; uncertain writes are reconciled before repetition.

### Inspect evidence

1. The alert-list and single-alert operations retrieve the incident's alert evidence; paginated alert lists continue until complete. Notes are retrieved separately. Success yields the native objects, not a generated root-cause verdict.
2. The optional outlier, past-incident and related-incident operations return PagerDuty's own findings. Past incidents cover similar metadata on the same service within six months; related incidents return at most the twenty most recent relationships. These features have account-plan restrictions; refusal is not evidence that no similar incident exists.
3. Report native triggered, acknowledged or resolved state and each observation's time. Acknowledgement is a response action, not an infrastructure recovery check.

### Create or change an incident

1. Creation receives the supplied title and target service, with the actor identity required by PagerDuty. Optional assignment and escalation-policy selection are mutually exclusive. **Repository safeguard: stop and confirm with the operator before proceeding** because incident creation can notify responders. Success returns a newly created incident.
2. An update applies the approved native state or assignments to the selected incident. **Stop and confirm with the operator before proceeding**, especially for resolution or reopening. Success returns the updated incident; a detail read confirms the resulting state. Reopening to acknowledged assigns the current user; reopening to triggered follows explicit assignments/policy or the current escalation policy.
3. An explicit incident key rejects another open incident with that key on the same service; rejection is not a newly created incident. Input or account errors follow **Find incidents**.

### Request responders or add a note

1. A responder request includes the requesting user's identifier, message and explicit user or policy targets. **Stop and confirm with the operator before proceeding**; the request uses high-urgency notification rules until accepted or declined. Success is the returned request, not proof that the responder accepted. Missing coordinated-response entitlement stops the request.
2. A note attaches the supplied text to the incident. **Stop and confirm with the operator before proceeding** to publish it. Success returns the note; note retrieval confirms the stored text. PagerDuty limits an incident to 2000 notes; a rejected note remains unpublished.

### Merge incidents

1. The selected target must be open. Eligible sources have alerts or were manually created in the UI. The combined target cannot exceed 1000 alerts.
2. **Stop and confirm with the operator before proceeding**: merging moves source alerts and resolves the source incidents. The successful response identifies the target; detail reads confirm source resolution and target evidence. A rejected merge preserves the separate records; an uncertain result requires those reads before any repeat.

## Patterns

- Incident state, infrastructure health and responder acceptance are different observations.
- Related and outlier findings are vendor-generated evidence; this procedure adds no causal or severity judgment.
- Actor identity and account capability checks apply even when a connector exposes a write tool.

## Known limitations

This procedure does not select service owners, define emergency policy, create change requests, or execute remediation. Retrieval of historical incidents is constrained by native filters and entitlements.

## Tools

| Operation | Description | Category |
|---|---|---|
| Find and inspect incidents | Retrieve records, alerts, notes and optional relationships | Read |
| Create or change incident | Maintain the requested native incident state | Write |
| Request responders | Notify the explicit responder targets | Write |
| Add note | Publish supplied incident evidence | Write |
| Merge incidents | Consolidate alerts and resolve sources | Destructive |

## Verification checklist

- Scope, time window and pagination are recorded.
- Native states and feature restrictions remain visible.
- Each mutation had its inline gate and returned resource verified.
- Responder requests are not described as accepted unless that state is observed.


Sources: [PagerDuty REST OpenAPI reference](https://github.com/PagerDuty/api-schema/blob/main/reference/REST/openapiv3.json), REST v2, retrieved 2026-10-09.
