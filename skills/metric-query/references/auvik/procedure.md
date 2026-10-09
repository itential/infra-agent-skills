# Auvik statistics and poller-history query

Retrieve device, interface, service, component and SNMP measurements.

## Common Sequences

- Time series: **Establish tenant scope** → **Read time-series statistics** → **Complete the read or report its error**.
- Custom polling: **Establish tenant scope** → **Resolve poller** → **Read poller history or current OID** → **Complete the read or report its error**.

### Establish tenant scope

Credential verification establishes API access; tenant discovery supplies the client identities authorized for the account. The requested tenant is resolved from that result. Each tenant is queried separately so failures retain their scope. A regional redirect requires correction to the account's actual Auvik region, not unrestricted forwarding of credentials.

### Read time-series statistics

The selected resource class determines its statistic identifier and required entity filters. Device/availability/interface/service/component series require a starting timestamp and reporting interval; an omitted ending timestamp uses the API's current time. The result retains its native timestamps, units and missing values. Availability statistics remain distinct from CPU/bandwidth measurements. Not every component type supports every statistic; a rejected combination requires the platform's supported pairing rather than a substituted metric.

### Resolve poller

Poller settings resolve the internal setting IDs, type and associated devices. Tenant scope is required for the settings list and associated-device list. A friendly poller name is not substituted into an ID field.

### Read poller history or current OID

Numeric poller history requires tenant, starting time and interval. String history requires tenant and starting time; compact mode returns value changes, while non-compact queries have a documented maximum 24-hour span. The current-OID operation returns the latest recorded value and has no historical interval. It is not presented as a time series.

### Complete the read or report its error

A successful empty result is still HTTP 200. Cursor-based lists continue through their returned next links; an intentional stopping point is reported as partial. The result preserves native status, timestamps and missing values. A bad request requires corrected parameters, authentication/authorization failures require corrected access, and not-found requires checking the resource identity. These are not blindly retried. Rate-limit responses pause further requests; the publisher also documents rate-limit blocking that appears as forbidden. Internal service errors use exponential backoff, with persistent failures referred to platform support. No universal retry count is specified.

## Patterns

Time-series interval selection changes aggregation. Current OID data and historical poller data answer different questions; string change-only output does not represent every poll.

## Known limitations

Exact retention varies by statistic and reporting interval; this procedure does not promise arbitrary historic coverage or import wrapper page caps. Unknown or unsupported combinations remain errors.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Verify/resolve | Establish tenant scope | Monitoring read |
| Read series | Retrieve selected statistic family | Monitoring read |
| Resolve/read poller | Query settings, associated devices and history | Monitoring read |

## Verification checklist

- Metric family, statistic and entity scope match.
- Required timestamp/interval/tenant parameters are present.
- String compact and current-OID semantics are preserved.
- Units, native gaps and incomplete pagination are retained.

## Sources

- [Auvik OpenAPI v1 specification](https://auvikapi.us1.my.auvik.com/spec). Retrieved 2026-10-09.
- [Auvik integration guide](https://support.auvik.com/hc/en-us/articles/360031007111-Auvik-API-Integration-Guide). Retrieved 2026-10-09.
