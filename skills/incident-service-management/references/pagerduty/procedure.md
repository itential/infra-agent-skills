# PagerDuty incident services

PagerDuty REST v2 provides service discovery and core service configuration.

## Common Sequences

- Inspect: **Locate and inspect service**.
- Create: **Locate and inspect service → Resolve policy → Create service → Locate and inspect service**.
- Change: **Locate and inspect service → Resolve policy → Update service → Locate and inspect service**.

### Locate and inspect service

1. A service list uses the requested name/query or team filters and completes offset pagination. Detail retrieval returns the selected service, optionally including integration details.
2. Native active, warning, critical, maintenance and disabled values describe incident handling and open-incident state. They are not a substitute for infrastructure telemetry.
3. At every step, invalid input is corrected; unauthorized, forbidden or missing resources stop that operation; missing account capabilities are disclosed. Error bindings appear in [endpoints](endpoints.md). An unknown write outcome is reread before repetition.

### Resolve policy

1. Policy retrieval identifies the supplied escalation policy. Its existence and identifier are required for the requested service association; selection of the organization's appropriate policy remains an operator input.
2. Success is the selected policy object. A missing or unauthorized policy stops service creation or reassociation.

### Create service

1. The request contains the supplied service name and policy, plus explicit requested timeout or urgency settings. **Repository safeguard: stop and confirm with the operator before proceeding**, because the resulting service controls incident notifications.
2. Creation supports only active status. A requested different state requires a subsequent **Update service** operation. Success returns the new service; a detail read verifies its stored configuration.
3. PagerDuty documents a25000-service account limit. At100000 open incidents on a service, creation can change a disabled auto-resolve timeout. The source contradicts itself by calling84600 seconds one day; this procedure does not adopt that duration and instead reports the returned timeout for operator review.

### Update service

1. The selected service's requested core properties are changed only after **stop and confirm with the operator before proceeding**, explicitly stating any notification or automatic-resolution effect.
2. Success returns the updated service, followed by a detail read. At100000 open incidents, an attempt to disable automatic resolution is rejected; the prior timeout remains the relevant state until read back.
3. Deprecated grouping references can be ignored by the service API. Grouping changes require the separate vendor grouping API and are outside this scope.

## Patterns

- Creating a service does not provision its integrations; they are a separate operation.
- Returned timeouts matter more than an assumed platform default.
- Service teams in the representation are read-only associations, not a writable list for this procedure.

## Known limitations

No integrations, dependencies, deletion, alert grouping, or organizational naming policy is supplied. The source's84600-seconds/one-day discrepancy is explicitly unresolved.

## Tools

| Operation | Description | Category |
|---|---|---|
| List/get service | Inspect native service configuration | Read |
| Get escalation policy | Resolve the supplied association | Read |
| Create/update service | Maintain requested core properties | Write |

## Verification checklist

- Selected policy and service identifiers are verified.
- Stored status and timeouts are checked after creation/update.
- Errors and documented account limits are reported without invented workarounds.


Sources: [PagerDuty REST OpenAPI reference](https://github.com/PagerDuty/api-schema/blob/main/reference/REST/openapiv3.json), REST v2, retrieved 2026-10-09.
