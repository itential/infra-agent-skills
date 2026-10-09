# Batfish snapshot lifecycle

Create, list or delete a stored Batfish configuration snapshot through Pybatfish.

## Common Sequences

- New model: **Select network** → **List snapshots** → **Upload snapshot** → **Read initialization issues**.
- Remove a stored model: **Select network** → **List snapshots** → **Delete snapshot** → **List snapshots**.

### Select network

The session's network selection returns the selected name and can create a missing network. If creation is intended, **stop and confirm with the operator before proceeding**. Existing-network analysis uses its known network name. Access failure leaves the selection unresolved.

### List snapshots

The list operation returns names, or metadata when verbose mode is selected, for the current network. Success is that collection; a named target must be identified within its network before overwrite or deletion.

### Upload snapshot

The publisher packages configuration files in a top-level snapshot folder containing a configurations subfolder. A ZIP retains that top-level folder. The initialization operation accepts that directory or ZIP and a snapshot name. Before uploading to the service or replacing a stored snapshot, **stop and confirm with the operator before proceeding**. Overwrite is disabled by default; replacing an existing name must be separately explicit. Success is the returned initialized snapshot name, followed by initialization-issue review. A timeout or processing exception is unresolved until the stored snapshot collection/state is reconciled; automatic overwrite is not a recovery method.

### Read initialization issues

The model initialization query returns parsing/conversion issues with their source context. A completed upload with warnings remains a model with warnings, not a passed validation result.

### Delete snapshot

Deletion removes the selected snapshot from the current network: **stop and confirm with the operator before proceeding**. The SDK deletion method has no success payload. A successful deletion call followed by a same-network snapshot list without the name confirms removal. Missing network context or an omitted snapshot name is an input error; other client/service exceptions leave the result unresolved.

## Patterns

Snapshot creation and deletion mutate the analysis service even though they do not configure network devices. The source's blanket read-only description therefore does not apply to these operations. Reusing an existing snapshot does not require re-uploading it.

## Known limitations

Deletion and overwrite remove stored analysis inputs. No backup/recovery procedure, storage-retention guarantee or automatic ephemeral cleanup is established by these sources. Live configuration deployment is outside scope.

Sources: Pybatfish 0.36.0 [interaction guide](https://batfish.readthedocs.io/en/stable/notebooks/interacting.html) and publisher [session implementation](https://github.com/batfish/pybatfish/blob/master/pybatfish/client/session.py), retrieved 2026-10-09. Bindings are in [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Select network | Select or create the analysis network | Read/Create |
| List snapshots | Read snapshot names or metadata | Read |
| Upload snapshot | Initialize a stored model from supplied configurations | Create/Overwrite |
| Read initialization issues | Read parsing/conversion evidence | Read |
| Delete snapshot | Remove the named stored model | Delete |

## Verification checklist

- Network and snapshot names are explicit.
- Service-side creation, upload, overwrite or deletion was confirmed at its step.
- Initialization returned the intended name and issues were reviewed.
- Deletion was verified against the same network's snapshot list.
