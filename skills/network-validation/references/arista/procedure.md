# Arista ANTA: run network readiness tests

Execute an approved ANTA catalogue against an explicit EOS inventory.

Sources: [ANTA Getting Started](https://anta.arista.com/stable/getting-started/) and [NRFU CLI](https://anta.arista.com/stable/cli/nrfu/), stable documentation retrieved 2026-10-09.

## 1. Select the inventory and catalogue

ANTA receives a device inventory and a catalogue naming its test classes and inputs. The supplied inventory identifies the intended devices; EOS eAPI access and credentials must already be configured. Catalogue expectations, such as acceptable versions or uptime, come from the request, not this skill. Credentials use the documented environment inputs or the password prompt.

Success: both files parse and the requested inventory/test selection is available. File or catalogue parsing failures end the run before any claim about device health.

## 2. Preview the selected coverage

The documented dry-run stops before executing tests and assumes inventory devices are connected:

```sh
anta nrfu --inventory <inventory-file> --catalog <catalog-file> --username <username> --prompt --dry-run table
```

Optional repeated `--device <inventory-name>` and `--test <test-class>` flags narrow the selection. `--tags <tag-list>` selects tagged devices and tests.

Success: the preview identifies the intended test/device combinations. A dry-run is not evidence that a device is reachable or that a test passed.

## 3. Execute the selected catalogue

The same selection runs without the dry-run flag. **For any selected test that changes live state, stop and confirm with the operator before proceeding**; test-specific publisher safeguards also apply.

```sh
anta nrfu --inventory <inventory-file> --catalog <catalog-file> --username <username> --prompt json
```

Success: the JSON report contains the selected run's results with device, test, result, and messages. Native `success`, `failure`, `error`, and `skipped` values remain distinct. A connection or execution error is reported with its message; it is not a test success. Console tables and text reports are alternative renderings of the run.

## 4. Preserve the complete result

The report retains all result states and the executed selection. An optional `json --output <new-report-file>` writes the report to a file. **If that destination already exists, stop and confirm with the operator before proceeding with an overwrite.** The documented status-ignoring flags can force a successful exit status or omit errors from it; a process exit code alone is therefore not sufficient evidence of test success.

## Patterns

Filters affect test coverage. Hiding error or skipped rows changes presentation and can conceal incomplete coverage; the retained report includes those outcomes. A new run with different catalogue values is a different validation, not a correction of the earlier evidence.

## Known limitations

This procedure covers execution and reporting of a supplied catalogue. It does not guarantee a fixed count of built-in tests, turn arbitrary model-authored commands into validated tests, or prescribe a rollback on a failed test. Per-test input constraints and device support come from that installed ANTA test's documentation.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local ANTA CLI | Parses inventory/catalogue, connects to EOS and renders results | CLI execution |
| EOS eAPI session | Existing transport used by the selected tests | Device API transport |

## Verification checklist

- Inventory and catalogue match the requested devices and expectations.
- Dry-run output was not presented as a completed test run.
- The report includes failure, error, and skipped states with their messages.
- The reported coverage matches the actual device/test/tag selection.
