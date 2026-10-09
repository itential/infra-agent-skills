# DefenseClaw security evidence

Cisco AI Defense's DefenseClaw CLI provides current posture, scan findings, and audit evidence without this procedure changing security policy.

## Common Sequences

- Inspect enforcement: **Read posture → Read tool policy → Read alerts**.
- Inspect a component: **Scan skill or Scan MCP → Read alerts**.
- Retrieve history: **Read alerts → Export audit**.

### Read posture

`defenseclaw guardrail status` reports the active connector roster and resolved posture. Success includes enabled state, effective mode, failure behavior, and related policy details. On a multi-connector installation, `--connector <connector>` narrows the view; the documented status selector is rejected on a single-connector installation. A CLI/configuration failure remains an unavailable observation.

### Read tool policy

`defenseclaw tool status <tool-name> --json` retrieves one tool's effective policy; `defenseclaw tool list --json` lists policy entries. The optional connector selector restricts scope where configured. Success returns the actual policy, not an inferred allow decision from the absence of a scan finding. The publisher documents that a source-scoped block is enforced without source separation because runtime hook payloads lack source identity; the source field is audit attribution, not an enforcement boundary.

### Scan skill

`defenseclaw skill scan --path <skill-directory> --json` scans the selected directory. A named installed skill can instead be selected with its configured connector. This sequence omits the action flag, installation, and remote fetching. Success returns scan severity, findings, and policy verdict; the native verdict is retained. A rejected verdict does not mean an already installed copy was automatically unloaded. A missing scanner SDK is a damaged-runtime condition requiring the publisher's supported repair path, not an improvised package replacement. Batch scanner failures can produce valid per-item results before a nonzero exit; successful findings are retained alongside failures. Telemetry-recording warnings do not invalidate a completed scan.

### Scan MCP

`defenseclaw mcp scan <configured-server-name> --json` scans the named configured MCP server. The publisher starts a local stdio server in a short-lived subprocess to inspect its advertised surface, and configured analyzers can use external services. Immediately before starting that configured process or submitting content to configured analyzers, **stop and confirm with the operator before proceeding**. Success emits a scan-result object for each scanned server; it is a stream of objects, unlike the skill batch array. Optional prompt/resource/instruction coverage is requested only when that scope is intended. A private-address target refused by the scanner is reported; this procedure does not bypass that safeguard. Scan failures remain failures rather than a clean result.

### Read alerts

`defenseclaw alerts --json` retrieves recent alerts; `--limit <count>` changes the requested window and `--connector <connector>` restricts event attribution. Success returns actual findings with target, decision, rule, scanner, and raw details. The default recent-alert limit is 25. An observe-mode would-block decision is not an enforced block. Reading alerts does not acknowledge or dismiss them.

### Export audit

`defenseclaw audit export --since <RFC3339-or-duration> --until <RFC3339-or-duration>` emits JSONL audit records in chronological order. The lower bound is inclusive and the upper bound exclusive. `--limit <count>` selects the earliest matching rows; `--newest` selects the most recent matching rows while still emitting chronological order. Success is the emitted audit stream. Saving it uses a new output file; immediately before replacing an existing file, **stop and confirm with the operator before proceeding**. A failed command or storage error is not an empty successful history.

## Patterns

Scanner verdicts, loaded-state labels, and enforcement modes are distinct. One-shot scan findings enter the platform's audit/observability surfaces. Configured scanner analyzers determine whether data stays local; this procedure makes no offline guarantee.

## Known limitations

No policy changes, manual exceptions, component installation/removal, quarantine, plugin scan, gateway restart, or observability configuration. The current publisher CLI differs from the NetClaw source's older alert-export and guardrail examples. Detailed stable error strings and all command exit codes are not documented in the selected reference; actual diagnostics remain authoritative.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authorized local shell | Run installed DefenseClaw inspection commands | CLI execution |

Primary sources: [CLI reference](https://github.com/cisco-ai-defense/defenseclaw/blob/95159fdb849d265f31e31a0ef92eff5e40ebbee0/docs-site/content/docs/reference/cli.mdx), [Skill scanner](https://github.com/cisco-ai-defense/defenseclaw/blob/95159fdb849d265f31e31a0ef92eff5e40ebbee0/docs-site/content/docs/scanning/skill-scanner.mdx), [MCP scanner](https://github.com/cisco-ai-defense/defenseclaw/blob/95159fdb849d265f31e31a0ef92eff5e40ebbee0/docs-site/content/docs/scanning/mcp-scanner.mdx), commit `95159fdb849d265f31e31a0ef92eff5e40ebbee0`, retrieved 2026-10-09. Literal CLI payloads are intentionally inline; there is no REST binding layer.

## Verification checklist

- Connector, component, tool name, and time window match the requested scope.
- Native verdict, runtime state, enforcement mode, and scan errors are distinguished.
- Skill arrays and MCP result streams are parsed according to their actual shape.
- Audit output order and time bounds remain explicit; no policy change was inferred from a read.
