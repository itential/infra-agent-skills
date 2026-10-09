# Containerlab lifecycle

Deploy, inspect, execute a specified node command, or destroy a lab described by an existing local topology file.

Sources: Containerlab current [deploy](https://containerlab.dev/cmd/deploy/), [inspect](https://containerlab.dev/cmd/inspect/), [exec](https://containerlab.dev/cmd/exec/), and [destroy](https://containerlab.dev/cmd/destroy/) references, retrieved 2026-10-09.

## Common Sequences

- Deploy or reconcile: Inspect → Deploy → Inspect.
- Command execution: Inspect → Execute command.
- Remove lab: Inspect → Destroy → Inspect.

## Inspect

`containerlab inspect --all --format json` identifies deployed labs and topology paths. `containerlab inspect -t <topology-file> --format json` returns the selected lab's containers, images, states, health, and management addresses. The expected result identifies the requested lab; container state is not proof of network-protocol convergence. Multiple topology files during automatic discovery produce an error; an explicit topology path resolves that ambiguity.

## Deploy

`containerlab deploy -t <topology-file> --dry-run` previews deployment or reconciliation where the installed release supports the current documented behavior. Before the actual deployment or reconciliation, **stop and confirm with the operator before proceeding**. `containerlab deploy -t <topology-file>` applies the topology. The completion output and subsequent Inspect establish what was deployed.

An existing deployment can have supported topology changes applied in place; tracked node-property changes can recreate affected nodes. The destructive `--reconfigure` option first removes the lab and its directory: **stop and confirm with the operator before proceeding**, explicitly including loss of generated configuration artifacts. Dry-run cannot be combined with reconfigure. Unsupported reconciliation changes, management-network overrides, or node filters rejected by the installed release require correcting the plan rather than silently adding reconfigure.

## Execute command

The transport runs a specified command in selected node containers: `containerlab exec -t <topology-file> --cmd '<approved-command>' --format json`. The requested command's own output and exit information determine success. **Before any command that changes state, stop and confirm with the operator before proceeding.** A topology selector can be narrowed with documented container labels. For vrnetlab nodes, execution reaches the launcher container, not the guest network OS; an executable-not-found error requires the guest's SSH/native CLI procedure, not repeated container execution.

## Destroy

Before removing the selected lab, **stop and confirm with the operator before proceeding**. `containerlab destroy -t <topology-file> --graceful` attempts to stop containers before removal. Adding `--cleanup` deletes the lab directory and all its contents and requires that loss to be included in confirmation. Without cleanup, configuration artifacts remain. A successful command followed by Inspect verifies the selected lab is no longer deployed. A failed destroy is reported with its diagnostics; it does not automatically authorize forceful removal.

## Patterns

The topology path remains the lab selector after deployment from a remote repository. This procedure uses an already reviewed local file. Runtime/container timeouts do not establish that deployment or destruction made no changes; Inspect establishes the current state.

## Known limitations

Containerlab CLI is the supported binding here; NetClaw's separate API server authentication behavior is not verified by these sources. Topology authoring, image entitlement, and guest-specific show commands are outside scope. Current reconciliation options must not be assumed on older releases. Full topology exports can include private keys; they are not routine inventory output.

## Tools

| Operation | Description | Category |
|---|---|---|
| Containerlab CLI | Controls the authorized container host's lab runtime | Local or remote process |

## Verification checklist

- The topology file and deployed lab identity agree.
- Inspect records actual container states and management addresses.
- Mutating command/deploy/destroy confirmation matches the exact scope.
- Cleanup and reconfigure artifact deletion are explicitly accounted for.
