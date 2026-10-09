# Zscaler ZDX: query experience evidence

Read application score/trend evidence or an ongoing alert and its affected devices.

Sources: publisher [application list](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zdx/list_applications.py), [score/trend tools](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zdx/get_application_score.py), and [ongoing alerts](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zdx/list_alerts.py), master retrieved 2026-10-09. Bindings appear in [endpoints.md](endpoints.md).

## Common Sequences

- Application observation: Find application → Read score or trend → Report evidence.
- Alert observation: Find alert → Read alert and affected devices → Report evidence.

## Find application

The application list uses the requested location, department, geography and look-back interval. Returned identifiers select an application for the next read.

Success: the intended monitored application has a returned identifier. A failed query is not an empty application list. Multiple matching names remain distinct identities.

## Read score or trend

The application-score operation returns a headline score and regional impact detail; the trend operation returns score observations over the selected interval. The same scope and look-back are used for comparisons.

Success: the application response contains the requested evidence, or explicitly has no returned data. Input and SDK errors retain their native messages. A score decrease is an observation rather than a proven causal diagnosis.

## Find alert

The ongoing-alert list uses the requested scope and interval, with optional paging. Returned alert identifiers select one alert for detail.

Success: the returned records identify ongoing alerts in that scope. The interval is bounded by the publisher's documented alert maximum. No returned alerts describes this query and is not a statement about all historical incidents.

## Read alert and affected devices

Alert detail uses the selected identifier. Affected-device retrieval uses that identifier and any requested scope filters. Records remain associated with the selected alert.

Success: the alert detail and returned devices agree on that identifier. Missing IDs are input errors; upstream lookup failures remain failures.

## Report evidence

The report retains source IDs, look-back hours and all scope filters. It distinguishes application score, trend data, alert detail and affected-device records. Paging limits remain explicit: the current list wrapper unwraps rows and does not guarantee that upstream continuation metadata survives, so an unverifiable list is reported as a page.

## Patterns

ZDX look-back is measured in hours. Reusing an epoch timestamp or a Z-Insights day interval as the look-back silently changes the intended request and is invalid. This read procedure does not start or delete an analysis/capture.

## Known limitations

Full device/user experience, probe and deep-trace result APIs are outside this limited score/alert procedure. Native scores do not supply a universal business severity threshold. The source NetClaw generic event names are not assumed to exist in the current publisher MCP.

## Tools

| Operation | Description | Category |
|---|---|---|
| Find application | Retrieve monitored application identifiers | MCP query |
| Read score/trend | Retrieve scoped application evidence | MCP query |
| Find/read alert | Retrieve ongoing alert details | MCP query |
| Read affected devices | Retrieve devices associated with an alert | MCP query |

## Verification checklist

- Application/alert IDs came from the intended scoped list.
- Look-back hours and filters remain explicit.
- A successful empty response is separate from an error.
- Paging uncertainty and limited diagnostic scope are reported.
