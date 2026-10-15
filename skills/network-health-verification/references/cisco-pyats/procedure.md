# Cisco pyATS — Job-Integrated Health Checks

Runs documented health processors alongside an existing pyATS job and reads their individual results.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Health Check Overview](https://pubhub.devnetcloud.com/media/genie-docs/docs/health/index.html).
- [Health Check Usage](https://pubhub.devnetcloud.com/media/genie-docs/docs/health/health_usage/usage.html).

## Common Sequences

- **Built-in checks:** Resolve checks → Run integrated job → Inspect health results.
- **Custom checks:** Resolve checks → Validate custom datafile → Run integrated job → Inspect health results.

## Resolve checks

Built-in checks: cpu, memory, logging, core, crashinfo. Success is a selection the target platform's
health APIs support, with arguments and thresholds resolved. Criteria come from the datafile or API,
not from a built-in operational standard. Missing API or platform coverage is unsupported, not healthy.

## Validate custom datafile

```bash
pyats validate datafile health.yaml
```

Success is a valid expanded definition. Processor structure is in [endpoints.md](endpoints.md).
Validity does not prove the health API exists on the platform.

## Run integrated job

Needs an existing pyATS job file and testbed; this procedure does not write the job.

**Before the job, connection initialization, log clearing, core-file copying to a remote server, or
crash-file deletion changes live state: stop and confirm with the operator before proceeding.** The
gate covers the whole run, including `--health-clear-logging` and the options listed in
[endpoints.md](endpoints.md). Cisco documents two forms:

```bash
pyats run job job.py --testbed-file testbed.yaml --health-checks cpu memory logging core crashinfo
```

```bash
pyats run job job.py --testbed-file testbed.yaml --health-file health.yaml
```

Success is health results recorded next to the test results. Errors, missing APIs, and failed
criteria are reported as such. The source gives no retry rule; a retry needs that API's documentation.

## Inspect health results

- Logging reports new messages between checks.
- Core and IOS XE crashinfo are separate checks.
- Crashinfo baselines after common setup, then flags crash files that appear during testcases.

Success is the criterion, observed result, and processor evidence per check. A passing functional
test is not a passing health check.

## Patterns

- CPU criteria sit in the YAML `include` expression; the CPU API has no threshold argument.
- The memory API takes a threshold argument; CPU and memory are bound differently.
- Custom processors can target testcase groups or sections.

## Known limitations

- Integrated job mode only; Cisco lists standalone mode as announced but not yet available.
- **Crashinfo examples enable file deletion.** `delete_files` defaults to false, but deletion also
  applies when `copy_files` is false, so successful archival cannot be assumed. Needs explicit approval.
- `--health-clear-logging` clears the device log buffer; it is not a display filter.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local pyATS CLI with device transport | Validate health YAML and run job processors | CLI |

## Verification checklist

- [ ] Check APIs and criteria match the platform and the request.
- [ ] Copying, clearing, remote copy, and deletion were inside the confirmation gate.
- [ ] Health results and functional test results were both inspected.
