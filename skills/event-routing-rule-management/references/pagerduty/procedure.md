# PagerDuty event orchestration routing

PagerDuty's event-orchestration router selects a destination service from an ordered rule set.

## Common Sequences

- Inspect: **Locate orchestration → Read rule paths**.
- Change routing: **Locate orchestration → Read rule paths → Replace router rules → Read rule paths**.

### Locate orchestration

1. The orchestration list identifies the selected object; pagination continues while more results exist. Detail retrieval confirms its identity.
2. At all steps, bad parameters require correction; missing authentication, permissions or resources stop the operation. Unsupported methods are a binding error. A conflict requires rereading current state before any replacement. These errors and exact bindings are in [endpoints](endpoints.md).

### Read rule paths

1. Global-path retrieval returns processing before service routing. Router retrieval returns the ordered routing rules and fallback. The service-path read is addressed by service identifier, not orchestration identifier.
2. The router evaluates rules in sequence and uses the first match. Events without a match use the configured fallback, or the unrouted path where none is specified.
3. Success returns each requested rule object. Missing paths or denied access remain separate incomplete observations.

### Replace router rules

1. The complete intended router is assembled from the current configuration and operator-supplied conditions and service targets. Appending a rule is an edit to that complete representation; the native API does not expose NetClaw's named append operation.
2. **Repository safeguard: stop and confirm with the operator before proceeding**: replacement deletes omitted rules and omitted rule details, changing live event routing. Approval covers the resulting rule order and fallback as well as the requested addition.
3. The replacement returns the saved router plus any warnings. Entitlement warnings can mean a stored rule is not evaluated. Such a result is reported as saved with warnings, not effective routing success. A subsequent rule-path read verifies the full saved configuration.
4. An uncertain write outcome requires a fresh router read before another replacement; no automatic replay of a stale rule set is implied.

## Patterns

- Order changes behavior even if the same rules remain present.
- Dynamic routing has separate entitlement and placement constraints; this scope accepts supplied ordinary service-target rules only.
- Service orchestration is keyed by service; using the orchestration identifier would inspect the wrong resource type.

## Known limitations

Global and service transformation/suppression writes, event injection tests, dynamic routing authoring, and business routing policy are excluded. Readback proves stored configuration; it does not prove an event reached a service.

## Tools

| Operation | Description | Category |
|---|---|---|
| List/get orchestration | Resolve selected orchestration | Read |
| Read global/router/service paths | Inspect event processing and routing | Read |
| Replace router | Save complete ordered router configuration | Destructive |

## Verification checklist

- Correct orchestration and service identifiers were used.
- Replacement preserves every intended existing rule and fallback.
- Inline confirmation covered deletion through omission.
- Returned warnings and readback are included in the outcome.


Sources: [PagerDuty REST OpenAPI reference](https://github.com/PagerDuty/api-schema/blob/main/reference/REST/openapiv3.json), REST v2, retrieved 2026-10-09.
