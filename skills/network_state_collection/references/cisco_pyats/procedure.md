# Cisco Genie — Collect and Compare Network State

Captures parsed command data or feature snapshots and compares matching saved observations.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Genie Parse](https://pubhub.devnetcloud.com/media/genie-docs/docs/cli/genie_parse.html).
- [Genie Learn](https://pubhub.devnetcloud.com/media/genie-docs/docs/cli/genie_learn.html).
- [Genie Diff](https://pubhub.devnetcloud.com/media/genie-docs/docs/cli/genie_diff.html).
- [Ops Use](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/Ops/user/ops.html).
- [Unicon Connections](https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html).

## Common Sequences

- **Command snapshot:** Select coverage → Capture commands → Inspect artifacts.
- **Captured command text:** Select coverage → Parse captured text.
- **Feature comparison:** Select coverage → Capture features → Capture features again → Compare snapshots → Inspect artifacts.

## Select coverage

A parser structures a command's output; an Ops model collects the commands needed for one
feature. The model and parser coverage must match the device OS/platform. The Genie Feature
Browser linked in [endpoints.md](endpoints.md) identifies available implementations.
Success is a supported command/feature and an explicit device selection. Unsupported coverage is
reported as unsupported, without substituting another platform's schema.

## Capture commands

**Before any live connection: stop and confirm with the operator before proceeding.** Unicon
initialization can run configuration commands even for read-only intent (Cisco's own example sets
terminal and logging options).

Cisco's CLI sequence is:

```bash
genie parse "show version" --testbed-file testbed.yaml --devices dut --output snapshot_before
```

Success is a parsed structure, console capture, and connection log listed in the summary.
`--output` names a directory, not a JSON filename. The documented missing-parser diagnostic is
`Could not find parser for '<command>'`; parser errors or empty output are incomplete collection,
not evidence of a healthy network. Captured-text parsing bindings are in [endpoints.md](endpoints.md).

## Parse captured text

The parser reads saved output for the selected platform; no command runs and no session opens.
The binding and its version assumption are in [endpoints.md](endpoints.md). Success is the
returned structure; a parsing or schema error leaves the capture unparsed. It says nothing about
current device state.

## Capture features

After the same live-connection gate, the selected feature is collected with:

```bash
genie learn interface --testbed-file testbed.yaml --devices dut --output snapshot_before
```

Success is the feature's Ops structure plus console/connection evidence. A second collection uses
a different output directory, such as `snapshot_after`, after the independently authorized event.
`Feature not yet developed for this os` identifies missing coverage; the summary's exception file
is the evidence for failure. A feature exception is not a valid empty baseline.

## Compare snapshots

```bash
genie diff snapshot_before snapshot_after --output comparison
```

Cisco supplies default exclusions for changing fields. Additional exclusions are optional and
must match the requested comparison; this procedure does not invent an exclude list that hides
state being checked. `--no-default-exclusion` disables those defaults when explicitly requested.
Success is the comparison artifact for the matching snapshots. A leading minus or plus marks the
before or after side of a changed or absent key; missing source artifacts leave the comparison
incomplete, not unchanged.

## Inspect artifacts

The collection summaries name the data, console, connection, and any exception files. The diff
summary names its comparison files. Completion requires the requested device/feature or command
artifacts, with collection failures reported separately. An empty diff establishes equality only
for the successfully collected fields included in that comparison.

## Patterns

- Without device selection, learning targets all devices in the testbed and normally runs in
  parallel. `--single-process` selects sequential collection.
- Both objects in an Ops comparison must be learned before comparing.

## Known limitations

- This is collection/comparison, not a root-cause decision tree or a health policy.
- Feature schemas aim at a common structure; populated fields and implementation coverage vary.
- Custom parser development is excluded. Offline parsing of captured text is in the binding reference.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local CLI with device transport | Run Genie collection and file comparison | Shell / SSH |
| Python parser binding | Parse already captured text without device execution | Local Python |

## Verification checklist

- [ ] Requested device/command/feature coverage is identified.
- [ ] Every requested collection has its data and evidence or an explicit failure.
- [ ] Both comparison inputs contain collected state.
- [ ] Exclusions and the resulting differences are reported with artifact locations.
