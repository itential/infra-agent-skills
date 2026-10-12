# Cisco pyATS — Execute Network Tests

Selects the documented test format and completes its preparation, execution, and result checks.

## 1. Select the requested execution mode

| Input / operation | Full procedure | Binding reference |
|---|---|---|
| Python AEtest script and Easypy job | [aetest.md](aetest.md) | [aetest-endpoints.md](aetest-endpoints.md) |
| Blitz YAML testcase | [blitz.md](blitz.md) | [blitz-endpoints.md](blitz-endpoints.md) |
| Robot Framework suite | [robot.md](robot.md) | [robot-endpoints.md](robot-endpoints.md) |
| Genie trigger/verification datafiles | [genie-harness.md](genie-harness.md) | [genie-harness-endpoints.md](genie-harness-endpoints.md) |
| Job-integrated Health Check | [health.md](health.md) | [health-endpoints.md](health-endpoints.md) |

These are alternative execution formats or an explicitly requested job processor. They do not
require a migration between authoring formats. Each mode contains its own source citations.

## 2. Execute the selected procedure

The selected reference contains the complete sequence, required inputs, and confirmation gates.
A passing result is meaningful only against the requested test assertions and the actual executed
sections. Unavailable tests or missing device coverage remain incomplete coverage.

## 3. Report results

AEtest/Genie expose Passed, Passx, Failed, Errored, Aborted, Blocked, and Skipped results. Robot
reports through its own result model. The selected procedure preserves those distinctions and
points to the evidence rather than reducing everything to an undifferentiated boolean.

## Patterns

The same testbed can serve different harnesses; the harness's own mapping and connection rules
still apply. Health checks execute alongside the job, not as a separate generic monitoring daemon.

## Known limitations

The supplied test code/data controls device effects, including setup and cleanup. Framework
execution does not authorize a destructive test or guarantee recovery after interruption.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local Python / harness CLI | Run the chosen script, datafile, or suite | Test execution |

## Verification checklist

- [ ] The input format was routed to its complete procedure.
- [ ] Requested sections actually executed and their results were inspected.
- [ ] Test and cleanup failures remain visible with supporting logs.
