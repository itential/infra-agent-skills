# FortiAnalyzer historical log query

Retrieve scoped historical FortiGate log messages and their details through the FortiAnalyzer 7.6.5 console.

Sources: Fortinet [log-list selection](https://docs.fortinet.com/document/fortianalyzer/7.6.5/administration-guide/551675/viewing-the-log-message-list-of-a-specific-log-type), [filtering](https://docs.fortinet.com/document/fortianalyzer/7.6.5/administration-guide/368629/filtering-messages), [message details](https://docs.fortinet.com/document/fortianalyzer/7.6.5/administration-guide/169649/viewing-message-details), [historical mode](https://docs.fortinet.com/document/fortianalyzer/7.6.5/administration-guide/294662/viewing-historical-and-real-time-logs), retrieved 2026-10-09. This procedure assumes an already authenticated web console; [endpoints.md](endpoints.md) identifies the UI bindings without inventing REST calls.

1. **Select log scope.** In the correct ADOM, Log View → Logs → Fortinet Logs → FortiGate selects the device family. The toolbar selects the requested log type, device set and time period. Historical Log mode is the default and can be selected from More. Success is the corresponding historical message list with its scope displayed.
2. **Select filterable columns and case behavior.** The table-header settings control displayed columns; only those columns appear in the filter selector. The More menu controls case sensitivity. Success is the requested columns and case mode; case-insensitive search is the documented default.
3. **Apply filters.** Filter Mode chooses a field, supported comparison operator and value, then Apply. Additional filters default to conjunction; the displayed operator can switch to disjunction. Text Mode accepts native field/operator/value expressions while preserving the criteria when modes change. Success is the filtered list with the intended expression visible. Integer range comparisons apply to integer fields. Object-name filtering for source/destination objects requires UUID logging on the FortiGate; absent prerequisite data is not proof of no traffic.
4. **Inspect selected message details.** Double-clicking a selected message opens categorized fields in the details pane. Success is the selected event's actual fields and scope, including device/VDOM/policy identifiers where the event records them. Available UTM logs can be opened from that message's UTM icon. A missing field remains unavailable rather than inferred from a manager's configuration.
5. **Report matching evidence.** Results retain the ADOM, devices, log type, time period, filter and displayed event fields. The Action column is a combined policy/UTM interpretation: acceptance means both permit traffic, and denial can come from either. A green acceptance icon can still accompany a threat classification when the configured UTM action allows it; acceptance is not a universal security verdict.

The cited console pages do not enumerate connection/authentication/search-failure codes or pagination completeness guarantees. A failed view or search remains failed; a visible subset is not presented as a complete API export. No matching records means none were returned under this scope, not that the rule was never used or the firewall is currently passing traffic.

## Patterns

- Free-text searches cover configured indexed fields; they are not guaranteed full-record searches.
- Smart Action-column filters combine policy and UTM handling, so they differ from filtering a raw action field alone.
- Historical log evidence and live firewall state are different observations.

## Known limitations

- This is an official console procedure; no NetClaw JSON-RPC task/cursor contract is claimed.
- The original source's single-use search-task assertion, rule-activity aggregation and managed-device inventory remain unverified/unconverted.
- No saved view, retention change, log export, archive download, PCAP retrieval or live-log subscription is included.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authenticated FortiAnalyzer web console | Select historical log scope, apply filters and inspect event details | Read |

## Verification checklist

- ADOM, devices, historical mode, log type and time interval match the request.
- Filter expression, operator relationships and case mode are visible.
- Selected event detail corresponds to the requested evidence.
- Missing fields, failed queries and visible-subset limitations remain explicit.
- No historical finding is presented as a current forwarding or universal security verdict.
