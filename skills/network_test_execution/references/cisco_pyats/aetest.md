# Cisco pyATS — AEtest Job Execution

Builds an AEtest script/job pair and reports section and job results.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Script Structure](https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html).
- [Steps](https://pubhub.devnetcloud.com/media/pyats/docs/aetest/steps.html).
- [Jobfiles and Tasks](https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html).
- [Result Rollups](https://pubhub.devnetcloud.com/media/pyats/docs/results/rollup.html).

## 1. Define the script

The script has testcases with test sections; optional common setup and common cleanup surround
those testcases. Each testcase may also have its own setup/cleanup. Named steps provide individual
results within a section. [aetest-endpoints.md](aetest-endpoints.md) contains an original example.
Success is a discoverable script with the requested assertions and cleanup, not empty passing
sections. A failed testcase setup blocks its test sections; cleanup remains a separate result.

## 2. Define the job

An Easypy job has a main entry point and launches the script as a task. The example includes its
required import and resolves the script relative to the job file. Success is a job referencing the
intended script and its explicit inputs. An empty job or absent main entry point raises an error.

## 3. Run the job

**Before any setup, test, cleanup, or connection initialization changes a live device: stop and
confirm with the operator before proceeding.** Approval covers those resolved actions, including
cleanup changes, before the automated run begins.

```bash
pyats run job job.py --testbed-file testbed.yaml
```

Success means the intended sections ran and their results were recorded. Failed assertions, blocked
sections, errors, skips, and aborts remain their actual outcomes. A task crash can leave the testbed
changed even when tasks are sequential; subsequent tasks do not prove cleanup succeeded.

## 4. Inspect the results

The job aggregates task logs/results. Completion includes inspection of test and cleanup results.
The result rollup is Cisco's table, not a guessed numeric severity ordering: for example Passed
combined with Skipped is Passed, while Errored combined with Failed is Errored. A skipped test is
not independent evidence that its assertion passed.

## Patterns

- Common setup/cleanup have fixed reporting identifiers regardless of class names.
- Explicit step results retain a reason in the report; exceptions must not be hidden as passes.

## Known limitations

- Expected network state is a required test input; this framework does not supply it.
- The job invocation loads the testbed. A bare Python script does not gain that CLI loading behavior
  without a corresponding entry point/argument implementation.
- Common cleanup is a harness section, not an unconditional recovery guarantee after process loss.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Python / Easypy CLI | Execute scripts and aggregate task evidence | Local test harness |

## Verification checklist

- [ ] The job resolves the intended script and inputs.
- [ ] Named assertions ran; skips/blocks are distinguished from passes.
- [ ] Cleanup and aggregate results were inspected with the task log.
