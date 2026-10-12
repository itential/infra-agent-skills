# Cisco pyATS — Job-Integrated Health Checks

Runs documented health processors around a test job and inspects their individual results.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Health Check Overview](https://pubhub.devnetcloud.com/media/genie-docs/docs/health/index.html).
- [Health Check Usage](https://pubhub.devnetcloud.com/media/genie-docs/docs/health/health_usage/usage.html).

## Common Sequences

- **Built-in checks:** Resolve checks → Run integrated job → Inspect health results.
- **Custom checks:** Resolve checks → Validate custom datafile → Run integrated job → Inspect health results.

## Resolve checks

The documented built-in names are cpu, memory, logging, core, and crashinfo. Success is a selection
supported by the target device's health APIs, with their arguments and thresholds resolved.
The exact check criterion is part of the datafile/API: it is not an organization-independent health
threshold. Missing API/platform coverage remains unsupported, not healthy.

## Validate custom datafile

`pyats validate datafile health.yaml` checks the expanded YAML. The processor class and example
structure are in [health-endpoints.md](health-endpoints.md). Success is a valid expanded definition;
this does not by itself prove the selected health API exists on every platform.

## Run integrated job

**Before any job action, connection initialization, log clearing, file copying to a remote system,
or crash-file deletion affects live state: stop and confirm with the operator before proceeding.**
The gate covers the full run, including processors. Cisco documents these alternatives:

```bash
pyats run job job.py --testbed-file testbed.yaml --health-checks cpu memory logging core crashinfo
```

```bash
pyats run job job.py --testbed-file testbed.yaml --health-file health.yaml
```

Success includes the selected health processors' recorded results alongside the test results.
Health errors, missing APIs, or failed criteria remain explicit results. The guide does not provide
a universal retry rule for every health API; any retry requires that selected API's documentation.

## Inspect health results

Logging distinguishes new messages across checks. Core detection and IOS XE crashinfo detection
are separate checks. The documented crashinfo sequence establishes a baseline after common setup,
then flags newly appearing crash files during testcases. Success includes the actual criterion,
observed result, and relevant processor evidence; a passing functional testcase alone is not a
passing health check.

## Patterns

- CPU criteria reside in the YAML inclusion expression; the CPU API has no threshold argument.
- The current memory API's threshold argument and the CPU YAML criterion are different bindings.
- Custom processor placement can select testcase groups or sections.

## Known limitations

- The cited usage guide supports integrated job mode; standalone monitoring is not documented there.
- **Crashinfo examples enable file deletion.** The API's `delete_files` default is false, but an
  example setting true changes that. Cisco also documents deletion when copying is disabled, so
  successful archival cannot be assumed from deletion. That choice requires explicit approval.
- `--health-clear-logging` clears the device log buffer; it is not a harmless display filter.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local pyATS CLI with device transport | Validate health YAML and execute job processors | Test harness |

## Verification checklist

- [ ] Check APIs and criteria match the target platform and requested run.
- [ ] Any copying, clearing, or deletion was included in the confirmation gate.
- [ ] Health processor results and functional test results were both inspected.
