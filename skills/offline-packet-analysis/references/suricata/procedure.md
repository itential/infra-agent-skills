# Suricata offline signature review

Analyze a capture with an existing Suricata 8.0.6 configuration and rule set.

### 1. Verify configuration and rules

`suricata -V` identifies the engine. `suricata -T -c <config-file> -S <rules-file> --init-errors-fatal` validates the supplied configuration with the explicit rule set. `-S` selects those rules exclusively; `-s` would add to configured rules and is a different scope. Signature-loading errors cause failure with the fatal-init flag. Missing or unverified rules cannot support a no-detection conclusion.

The configuration must already enable the intended EVE output. This procedure does not modify or reload a running sensor, install rules, or assume a particular default signature count.

### 2. Analyze the selected file

`suricata -c <config-file> -S <rules-file> --init-errors-fatal -r <capture-file> -l <new-output-directory>` reads the existing capture and writes run artifacts. Before overwriting an existing output location, stop and confirm with the operator before proceeding. Initialization/read errors remain failed processing. The input-deleting option is outside this sequence; the original capture remains the evidence source.

The documented checksum selector is `-k all` or `-k none`. Any explicit choice is reported rather than silently changed to increase detections. No live interface, inline queue or simulated blocking mode is selected.

### 3. Inspect alerts and related flow events

`jq 'select(.event_type == "alert")' <output-directory>/eve.json` selects signature matches. Each finding retains timestamp, available endpoints, signature ID/revision, category, severity and native action. The EVE flow identifier correlates related records: `jq --argjson flow_id '<numeric-flow-id>' 'select(.flow_id == $flow_id)' <output-directory>/eve.json`.

PCAP packet number and source filename, when present, support a pivot back to the capture. The publisher omits these fields on internally generated pseudo-packets; their absence is not a corrupt-event verdict. JSON/read errors are incomplete analysis.

### 4. Report detection evidence

The report states engine version, selected configuration/rule scope, processing outcome, checksum choice and matches. No matching alert means only no match observed under that completed run’s rules. An alert is a signature match, not proof of compromise. An alert’s `allowed` action can differ from a packet’s final verdict; neither is described as a live enforcement action from this offline run.

## Patterns

Rule selection and successful initialization are prerequisites for interpreting empty alert output. EVE flow IDs and Zeek connection UIDs are different identifier systems; they are not directly joined as if equal.

## Known limitations

No empirical NetClaw rule count, ARMED/INERT/UNKNOWN wrapper enum or fixed severity threshold is retained. This procedure does not update rules or block traffic. The configured output/rules determine available evidence.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local CLI and JSON reader | Run Suricata in file mode and inspect EVE | Offline analysis |

## Verification checklist

- Configuration test and processing completed with the intended rule set.
- Rule-load failures do not become zero-alert successes.
- Native signature/action and flow identifiers are retained.
- Offline findings are not reported as production blocks.

## Sources

- [Suricata 8.0.6 CLI](https://docs.suricata.io/en/suricata-8.0.6/command-line-options.html). Retrieved 2026-10-09.
- [Suricata 8.0.6 quick start](https://docs.suricata.io/en/suricata-8.0.6/quickstart.html). Retrieved 2026-10-09.
- [Suricata 8.0.6 EVE event format](https://docs.suricata.io/en/suricata-8.0.6/output/eve/eve-json-format.html). Retrieved 2026-10-09.
