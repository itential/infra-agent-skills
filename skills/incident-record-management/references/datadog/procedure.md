# Datadog incident records

Datadog Incident Management's public-beta V2 API lists, retrieves, creates and partially updates incidents.

## Common Sequences

- Inspect: **List incidents → Read incident**.
- Create: **Create incident → Read incident**.
- Modify: **Read incident → Update incident → Read incident**.

### List incidents

1. The list operation returns incidents for the authorized organization, with page size and offset. The returned next offset continues the collection; pagination ends when no further records are returned.
2. This list binding does not accept the NetClaw wrapper's status, tags or relative-time filters. Such filtering is performed over retrieved records, or through a separately documented search operation outside this scope.
3. At this step and every subsequent call: malformed input is corrected, unauthorized/forbidden requests stop for access correction, a missing resource ends that lookup, and throttling defers further calls. The returned errors are retained. An unexpected transport failure remains an unknown outcome rather than an empty incident list.

### Read incident

1. The detail operation receives the incident UUID, not its human-facing number. Success returns its native fields, state, timestamps and requested related objects.
2. The result distinguishes incident record state from actual service recovery. Missing impact times are not inferred from declaration or detection timestamps.

### Create incident

1. The payload receives the supplied title and explicit customer-impact boolean. A positive impact assertion also needs the supplied impact description. Optional commander, incident type, timeline cells and notification handles are included only as requested.
2. **Repository safeguard: stop and confirm with the operator before proceeding** with record creation and any notification audience. Success returns201 with the created incident UUID; **Read incident** verifies its stored attributes.
3. A create timeout does not prove the record was absent. Listing/inspection reconciles the outcome before another create; no native idempotency key is assumed by this binding.

### Update incident

1. The partial-update operation contains only intended changes to the selected UUID. State changes use the documented typed incident-field representation; an arbitrary top-level status string is not substituted.
2. **Stop and confirm with the operator before proceeding**, including any resolution and notification handles. Success returns200 with the incident representation; **Read incident** confirms the stored changes.
3. Invalid field choices require platform-specific field guidance. The source does not provide an exhaustive universal state-transition policy, so this procedure does not manufacture one.

## Patterns

- Resource UUID and public incident number are different identifiers.
- A partial update does not require resending unrelated current fields.
- An incident can have organizational custom fields; the correct field type and selection must be supplied.

## Known limitations

Public beta may change. No deletion, timeline mutation after creation, incident-search endpoint, service correlation, MTTR analysis or organization-specific severity policy is included.

## Tools

| Operation | Description | Category |
|---|---|---|
| List/read incident | Retrieve incident records and native attributes | Read |
| Create incident | Record explicit impact and incident data | Write |
| Update incident | Apply a supplied partial field change | Write |

## Verification checklist

- The selected organization and incident UUID are retained.
- All pages needed for filtering were retrieved or incompleteness is stated.
- Impact assertions came from supplied evidence.
- Mutations passed the inline gate and were read back.

Sources: Datadog APIv2 [list](https://docs.datadoghq.com/api/latest/incidents/get-a-list-of-incidents/), [read](https://docs.datadoghq.com/api/latest/incidents/get-the-details-of-an-incident/), [create](https://docs.datadoghq.com/api/latest/incidents/create-an-incident/), [update](https://docs.datadoghq.com/api/latest/incidents/update-an-existing-incident/), retrieved 2026-10-09.
