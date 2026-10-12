# Cisco Genie — Blitz Test Execution

Runs a named declarative testcase and inspects its action results.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Blitz Design](https://pubhub.devnetcloud.com/media/genie-docs/docs/blitz/design/index.html).
- [Blitz Usage](https://pubhub.devnetcloud.com/media/genie-docs/docs/blitz/usage/usage.html).

## 1. Define the named testcase

The trigger datafile places the testcase name at the top level and associates it with the Blitz
class. Ordered sections contain ordered actions. [blitz-endpoints.md](blitz-endpoints.md) supplies
a concrete parse-only example; the expected data assertion remains an explicit test input.
Success is a named testcase whose actions and device references match the requested run.

## 2. Resolve action inputs

Each action uses its own documented arguments. Captured values can be saved and referenced later;
parallel groups are available for independent actions. Their exact forms are linked from
[blitz-endpoints.md](blitz-endpoints.md). A missing saved value or unsupported action leaves the
workflow incomplete; the design page does not enumerate all action-specific errors. Those require
the selected action's reference, not a fabricated common argument schema.

## 3. Execute the testcase

**Before actions or connection initialization configure, reset, restore, or otherwise alter live
state: stop and confirm with the operator before proceeding.** The approval covers every resolved
action, including cleanup. The selected testcase is invoked with:

```bash
pyats run genie --trigger-datafile blitz.yaml --trigger-uids collect_version --testbed-file testbed.yaml
```

Success is the intended testcase's action/section results. Passed, Failed, and Errored actions
retain their actual reasons; execution returning does not override failed assertions.

## 4. Inspect assertions and artifacts

The result report identifies which sections/actions executed. Completion requires the requested
assertions to have run and their results to be reported. The example only verifies parsing succeeds;
it does not establish an approved software version or network state.

## Patterns

- A sequence remains ordered unless explicitly grouped for parallel execution.
- The trigger UID must match the datafile's testcase key; an unrelated testcase is not equivalent.

## Known limitations

- Cisco labels dedicated Blitz schema validation as under construction in the usage page. Generic
  YAML validation alone cannot be presented as full action-schema validation.
- Mutating actions, REST/YANG payloads, and recovery require their own documented parameters.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local pyATS CLI | Execute the selected Blitz testcase | Test harness |

## Verification checklist

- [ ] The top-level testcase name matches the selected trigger UID.
- [ ] Requested actions and assertions ran against the intended device.
- [ ] Action and section results were inspected, including failures.
