# Vault KV secret lifecycle

Read, replace, list, inspect metadata, or remove a secret in an existing Vault KV mount.

Sources: HashiCorp current [KV v1](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v1), [KV v2](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2), [mounts](https://developer.hashicorp.com/vault/api-docs/system/mounts), and [HTTP API](https://developer.hashicorp.com/vault/api-docs), retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Retrieve: Identify engine → Read value.
- Inspect without values: Identify engine → List names or Read version metadata.
- Change lifecycle: Identify engine → Read version metadata (v2) → Replace or Remove/restore → Read version metadata (v2).

## Identify engine

The mount configuration establishes whether the engine is KV v1 or KV v2. A failed metadata read does not prove the mount is v1: absent keys and insufficient permissions can also produce not-found responses. If mount information is unavailable, the version remains unknown and the operation is blocked until confirmed.

## Read value

KV v1 returns the current value map. KV v2 returns a value map plus metadata for the requested version; omitting the version selects the latest version, even when that version has been deleted or destroyed. There is no automatic fallback to an older readable version. A value response contains secrets and is not safe to echo into a report. Only an approved secret-capable consumer receives the requested value; the report records nonsecret outcome metadata.

## List names or Read version metadata

A directory listing returns immediate child names; folder names have a trailing slash. KV v2 listing requires metadata-list permission and does not filter each returned name by its own policy, so names can themselves reveal sensitive information. The per-secret metadata read returns version history and deletion/destruction state without secret values. A successful empty LIST can be reported as 404; a generic 404 also permits absent or inaccessible resources, so its context matters.

## Replace

Before writing a secret consumed by live systems, **stop and confirm with the operator before proceeding**. Both versions replace the entire value map; v2 creates a new version. The v2 check-and-set condition can require a nonexistent key or an exact current version. When required by the engine or key, it must be supplied. A mismatch is a failed conditional write: metadata must be read again before a new reviewed attempt. Success is a successful status for v1 or the new version metadata for v2.

## Remove/restore

Each operation below requires **stop and confirm with the operator before proceeding**, including the exact path and version selection.

- KV v1 removal permanently deletes the value.
- KV v2 soft deletion marks the latest or explicitly named versions unreadable; metadata records deletion state.
- KV v2 restoration makes specified soft-deleted versions readable again; it cannot restore destroyed data.
- KV v2 destruction permanently removes specified version contents; metadata records destruction.

A successful response followed by the metadata state confirms a v2 lifecycle change. A not-found response alone is insufficient evidence of a completed removal.

## Error handling

For every operation, invalid requests require corrected inputs; forbidden responses require authentication/policy review; unsupported operations require the correct engine binding. Not-found may mean hidden access, not just absence. Enterprise consistency preconditions can be retried with backoff. A sealed/uninitialized/unavailable server blocks execution. After a write timeout or server failure, read-back is needed before a repeat because completion is unknown. Exact common statuses are in the binding.

## Patterns

Metadata inspection is a different operation from reading a value. NetClaw's claim that its read wrapper never returns values is not a property of the Vault read API. Secret injection into an integration is that integration's separate binding; Vault does not expose the source wrapper's generic inject operation.

## Known limitations

Mount enablement, engine-wide retention configuration, and non-KV secret engines are outside scope. Reducing retention can permanently remove history; this procedure does not modify retention. KV v1 has no version metadata or version-based recovery in this API.

## Tools

| Operation | Description | Category |
|---|---|---|
| Identify engine | Reads the mount's type/version | Read |
| Read value | Retrieves the current or selected version | Secret read |
| List names/read metadata | Retrieves names or version state without values | Read |
| Replace | Replaces a value; v2 creates a version | Secret write |
| Remove/restore | Deletes, undeletes, or destroys selected data | Lifecycle write |

## Verification checklist

- Engine version was confirmed from mount configuration.
- A latest-version read was not misreported as fallback to older data.
- Confirmation covered the exact mutation and version selection.
- Values were kept out of logs/reports; metadata was used where values were unnecessary.
