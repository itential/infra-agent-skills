---
name: exported-data-query
description: >-
  Query explicitly selected local JSON or CSV exports with SQL. Use for schema inspection, filtering, grouping, counting and joining previously exported infrastructure data. Covers DuckDB. Assumes an isolated local DuckDB client and authorized input files.
---

# Exported data query

Query explicitly selected local JSON or CSV exports with SQL.

## When to use this skill

Use for schema inspection, filtering, grouping, counting and joining previously exported infrastructure data.

## Universal concepts

No common wire protocol is implied by this capability. Query results describe the loaded dataset; they do not establish that the source export was complete. No cross-platform database schema is implied.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No live infrastructure queries, arbitrary filesystem discovery, or NetClaw runtime sandbox guarantees are included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an isolated local DuckDB client and authorized input files. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
