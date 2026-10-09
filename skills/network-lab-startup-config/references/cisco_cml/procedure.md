# Cisco CML stored node configuration

Read, replace or extract a supported CML node’s stored configuration.

## Common Sequences

- Inspect/replace: **Resolve and read** → **Replace** → **Resolve and read**.
- Extract running configuration: **Resolve and read** → **Extract** → **Resolve and read**.

### Resolve and read

The lab resolves a node by ID; the publisher exposes the main configuration and all named configuration files. Missing node is a resolution failure. Configuration contents are sensitive and are returned only to the authorized consumer.

### Replace

Setting a stored configuration can replace content: stop and confirm with the operator before proceeding. A string supplies the main configuration, a named dictionary supplies one file, a list supplies the file collection, and null clears it. The publisher’s unsupported-type error means the payload is invalid. The subsequent read establishes stored content; this is not a claim that the running guest changed.

### Extract

The publisher updates stored configuration from the running node: stop and confirm with the operator before proceeding. Completion followed by a refreshed configuration read is the available evidence. Extraction support and guest prerequisites depend on the node definition; a server rejection remains failure, not permission to substitute a guest command.

## Patterns

A list replaces the collection, whereas a named dictionary addresses a particular file. Stored configuration and active guest state must not be conflated.

## Known limitations

Extraction is only available where the installed node definition supports it. Server error catalogues and prerequisites are not fully enumerated by the client docstrings; platform-specific guidance is required for an unsupported extraction.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Read | Retrieve stored main/named configuration | Read |
| Replace | Set stored configuration | Destructive |
| Extract | Replace stored content from running node | Change |

## Verification checklist

- The exact node ID and affected named file are retained.
- Read-back shows the stored content requested.
- Running guest changes are not claimed from stored configuration alone.

## Sources

- [Cisco CML Node documentation and implementation](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/node.py). Retrieved 2026-10-09.
