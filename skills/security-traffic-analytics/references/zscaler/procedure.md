# Zscaler Z-Insights: retrieve a historical aggregate

Query web traffic or threat-category statistics for an explicit historical interval.

Sources: publisher [web-traffic tools](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zins/web_traffic.py) and [time/error contract](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zins/_common.py), master retrieved 2026-10-09. Bindings appear in [endpoints.md](endpoints.md).

## 1. Define the aggregate and interval

The query selects total traffic, traffic by location, protocol mix, threat super-categories, or threat classes. The measure is transactions or bytes. The documented connector requires a historical interval of seven or fourteen days and rejects a window ending less than one day ago; its documentation describes a 24–48-hour processing delay.

Success: explicit start and end values establish the intended interval. Start at/after end or a too-recent end is rejected. Relative windows can be automatically adjusted by this connector; exact requested windows use explicit timestamps so any adjustment cannot silently change the question.

## 2. Retrieve the aggregate

The selected operation receives the interval, units and applicable grouping/filter options. Total and location traffic can include a trend. The result is a set of aggregates, optionally with nested trend data.

Success: the operation returns the requested grouped totals or an empty successful result. SDK failures and GraphQL body errors remain failures even when the transport returned HTTP success. Bad-request errors require valid parameters and interval. Internal errors can indicate unavailable data or missing licensing according to the publisher's wrapper guidance; the exact cause remains unconfirmed without tenant-specific evidence.

## 3. Report scope and limits

The result identifies interval, unit, grouping, filters and row limit. An empty threat aggregate states that this query returned no detected categories; it does not establish an absence of all threats. A limited category/location result is not a complete event feed.

## Patterns

Absolute timestamps use milliseconds; this differs from ZDX's look-back hours. Aggregate trends and individual security events have different meanings and cannot be substituted. The connector's relative-window defaults are not an operator's chosen incident window.

## Known limitations

The source NetClaw skill lists generic threat-intelligence, sandbox, anomaly and compliance tools that are not these Z-Insights operations. They remain outside this procedure. No live last-hour security query or real-time feed is claimed.

## Tools

| Operation | Description | Category |
|---|---|---|
| Query historical aggregate | Retrieve the selected traffic/threat measure and grouping | MCP analytics query |

## Verification checklist

- Interval, units and grouping match the request.
- Any relative-window adjustment is disclosed.
- GraphQL errors were not hidden by HTTP success.
- Row limits and empty-result meaning remain explicit.
