# Cisco pyATS Clean — Execute an Approved Clean Definition

Validates and runs a caller-supplied, platform-specific sequence that restores a device baseline.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Preparing Clean](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/user_guide/writing_a_clean/getting_ready.html).
- [Cleaner Class](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/user_guide/writing_a_clean/cleaner_class.html).
- [Cleaning Devices](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/user_guide/writing_a_clean/cleaning_devices.html).
- [Executing Clean](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/user_guide/executing_a_clean.html).
- [Viewing Clean Logs](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/user_guide/viewing_clean_logs.html).

## 1. Resolve devices and supported stages

The testbed supplies the OS/platform and abstraction selection. The Clean definition names its
cleaner class, explicitly selected devices, stage arguments, and execution order. Success requires
the selected devices to exist in the testbed and every stage to match the selected platform's
[Clean Stage Browser](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/clean).
Image compatibility, stage timeouts, recovery, and required postconditions remain inputs from that
platform's documented procedure. Without them, a destructive run is not ready.

## 2. Build the definition

The cleaner is `PyatsDeviceClean` from `genie.libs.clean`. Stages are named mappings under each
device, with an `order` list at the same level. Only devices assigned to the cleaner are cleaned.
Success is a complete definition for the approved reset/baseline sequence. The schema illustration
in [endpoints.md](endpoints.md) is connection-only; it deliberately does not invent an erase/install
sequence that would supposedly apply to every device.

## 3. Validate

```bash
pyats validate clean --testbed-file testbed.yaml --clean-file clean.yaml
```

Success is validation without schema errors. The reported device/stage/key identifies malformed
input requiring correction. Validation does not establish image compatibility or guarantee recovery.

## 4. Execute the approved sequence

**Destructive boundary: stop and confirm with the operator before proceeding**, covering the
resolved devices, every erase/reload/install/configuration stage, image inputs, and recovery plan.
Cisco's runner executes the stages in the definition:

```bash
pyats clean --testbed-file testbed.yaml --clean-file clean.yaml
```

For a Clean that explicitly precedes a test job, the documented integrated command is:

```bash
pyats run job job.py --testbed-file testbed.yaml --clean-file clean.yaml --invoke-clean
```

The same confirmation gate applies immediately before this integrated command. Success is completion
of the requested stages according to their results. A failed stage is reported with its log;
a failure does not authorize restarting the whole destructive sequence. Stage-specific recovery
and retries require the matching platform guidance, not a guessed retry count.

## 5. Inspect the Clean results

The run produces a log location viewable with `pyats logs view <log-directory>`.
Success requires the intended stages to complete and the source-defined resulting image/configuration
checks to hold. A completed connect-only demonstration is not a completed reset or image installation.

## Patterns

- Supplying a Clean file to a job is distinct from invoking Clean; integrated execution includes
  the documented invocation flag.
- The `order` list is necessary even when only one stage is defined.

## Known limitations

- Erase, reload, image installation, and baseline replacement can destroy state or connectivity.
- This is the Clean runner procedure. Platform upgrade recipes remain separate; stage names and
  recovery behavior cannot be transferred between platforms by analogy.
- Group expansion and CLI image overrides are excluded to keep the resolved target set explicit.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local pyATS CLI with device transport | Validate, execute, and inspect Clean results | Shell / SSH / console |

## Verification checklist

- [ ] Selected devices, stage implementations, image inputs, and recovery are documented.
- [ ] Clean schema validation succeeded.
- [ ] Operator confirmation covered the exact destructive sequence.
- [ ] Stage results and required resulting image/configuration checks were inspected.
