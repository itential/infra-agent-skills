# FortiAnalyzer 7.6.5 console bindings

Sources and version are cited in [procedure.md](procedure.md). This procedure uses an authenticated web console. No JSON-RPC, MCP or REST route is inferred from UI controls.

| Operation | UI binding |
|---|---|
| Select logs | Correct ADOM → `Log View` → `Logs` → `Fortinet Logs` → `FortiGate`; select log type in toolbar |
| Set time/devices | Toolbar device and time-period selectors |
| Select historical mode | `More` → `Historical Log` |
| Select columns | Table-header settings icon |
| Select case mode | `More` → case-sensitive or case-insensitive search |
| Add filter | `Filter Mode` → `Add Filter` → field/operator/value → `Apply` |
| Combine filters | Displayed `AND`/`OR` toggle |
| Enter expression | `Text Mode`; native log field/operator/value syntax |
| Inspect event | Double-click row; categorized details pane; optional UTM icon when present |

The documented Filter Mode operators are `=`, `!=`, `<`, `>`, `>=`, `<=`, `~`, `!~`. Text search supports `and`/space conjunction, `or`/comma alternatives, field negation, integer ranges, IP subnet/ranges and regular expressions. The UI help supplies the deployed expression syntax; this binding does not infer fields that are absent from the log record.

No task ID, cursor lifetime, full-result count or normalized wrapper outcome is documented by these console sources.
