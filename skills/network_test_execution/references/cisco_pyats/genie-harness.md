# Cisco Genie — Trigger and Verification Run

Runs explicitly selected reusable triggers with their documented verification datafiles.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Harness Getting Started](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/harness/user/gettingstarted.html).
- [Harness Datafiles](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/harness/user/datafile.html).

## 1. Resolve the mapping

The mapping associates testbed device names/aliases, a context, a unit-under-test label, and
connection names. Success is a mapping to the requested devices and actual connection definitions.
The `uut` role is a mapping label, not a requirement to rename every physical device to that name.
[genie-harness-endpoints.md](genie-harness-endpoints.md) provides the binding.

## 2. Select documented triggers and verifications

The input datafiles identify implementations and their arguments; extending the installed defaults
can supply those definitions. Each requested trigger has an explicit device selection. Local
verification names must exist in the verification datafile. Success is a fully resolved ordered
selection, with each trigger's effects and each verification's comparison understood from its
platform implementation. Missing implementation or mapping information prevents execution.

The verification `iteration` fields specify an attempt count and fixed interval in seconds.
They do not describe exponential backoff. Exclusions omit selected changing fields from the
comparison; no universal exclusion list or convergence threshold is imposed here.

## 3. Run the job

**Before a trigger, setup, cleanup, configuration load, or connection initialization changes live
state: stop and confirm with the operator before proceeding.** The selected job binding passes
mapping, trigger, and verification datafiles to the harness:

```bash
pyats run job job.py --testbed-file testbed.yaml
```

Success requires the selected triggers and verifications to execute with their own reported
results. A verification that exhausts its configured attempts remains failed. Unsupported trigger
implementations and mapping failures remain unresolved; the harness reference does not specify
one universal recovery procedure for all triggers.

## 4. Inspect state comparisons and cleanup

The harness reports initial/final checks and test results. Its configuration snapshots can reveal
changes remaining after the run. Success includes the requested comparisons and cleanup outcome,
not only the trigger action returning. A skipped verification or missing snapshot is incomplete
coverage, not state equality.

## Patterns

- Ordered trigger selection and independent device mapping make the same implementation reusable.
- Local verification parameters can override matching global verification parameters; the resolved
  values, including attempts and exclusions, define the actual check.

## Known limitations

- The selected trigger may disrupt service or leave changes after failure.
- This runner procedure does not supply platform-specific trigger requirements, topology inference,
  image upgrades, or a generic rollback algorithm.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local Easypy / Genie harness | Execute resolved trigger and verification definitions | Test harness |

## Verification checklist

- [ ] Mapping resolves every requested device and connection.
- [ ] Trigger effects and verification implementations are documented for the platform.
- [ ] Selected triggers, comparisons, retries, and cleanup results were inspected.
