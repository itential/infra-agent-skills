# DuckDB exported-data query

Analyze selected infrastructure exports in an isolated, in-memory DuckDB session.

## Common Sequences

- Analyze an export: **Load selected data** → **Restrict external access** → **Inspect schema** → **Query**.
- Correlate exports: **Load selected data** for both → **Restrict external access** → **Inspect schema** → **Query** with an explicit shared key.

### Load selected data

The JSON/CSV readers infer columns and types or accept an explicit schema. The supplied local paths are selected before reading; arbitrary globs and remote URLs are outside this procedure. A trusted initialization query materializes the selected file into an in-memory table. JSON-lines input uses its documented newline-delimited format. CSV headers/delimiters can be supplied explicitly when detection is unsuitable.

Parse, type-conversion, inaccessible-file and object-size errors remain failures; ignored-error modes are not silently enabled. Explicit JSON column selection excludes unspecified fields. A raw Zeek TSV file’s comment header is not an ordinary CSV header: its column mapping must be supplied from the actual export rather than fabricated.

### Restrict external access

After materialization, the publisher’s external-access and configuration-lock settings restrict further file/network operations and subsequent configuration changes. Extension autoload/install and community extensions can also be disabled during trusted initialization. These settings do not create a complete sandbox; the publisher explicitly requires OS/container isolation for untrusted SQL. A setting failure stops the untrusted-query stage.

### Inspect schema

The table-description operation returns actual column names/types. Row counting establishes the number loaded. Missing tables or columns require correcting the query against that schema; a wrapper’s assumed renamed columns or all-text conversion is not inherited.

### Query

A selected read query returns its rows or aggregate result. Values in a controlled query use parameter binding; arbitrary query text is executable code, even if it starts with a read operation. Joins use a documented shared key present in both exports, never an assumed universal identifier.

A result limit is a preview, not a count of the dataset. Aggregation/counting runs over the selected loaded scope. Syntax/binding/cast errors, interrupted queries and resource failures are reported without inventing partial totals. The application must provide its own execution timeout/resource policy; no universal 30-second timeout is assumed.

## Patterns

DuckDB infers native types; it does not universally load every Zeek field as text. External access must be restricted after selected file materialization, because it also blocks the file readers themselves.

## Known limitations

The publisher warns that SQL and non-SQL expression APIs can access system resources. Configuration controls are defense in depth, not a proof against every filesystem/network path. Source export omissions remain omissions after SQL aggregation.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Load selected data | Materialize authorized exports into local memory | Local input |
| Restrict access | Apply publisher configuration restrictions | Local configuration |
| Inspect/query | Read table schemas and results | Local query |

## Verification checklist

- Loaded file paths and schemas match the selected exports.
- Parse failures and omitted fields are visible.
- Query limits do not become dataset totals.
- Isolation and configuration state are not confused with a complete security guarantee.

## Sources

- [DuckDB security model](https://duckdb.org/docs/current/operations_manual/securing_duckdb/overview). Retrieved 2026-10-09.
- [DuckDB JSON reader](https://duckdb.org/docs/current/data/json/loading_json). Retrieved 2026-10-09.
- [DuckDB CSV reader](https://duckdb.org/docs/current/data/csv/overview). Retrieved 2026-10-09.
- [DuckDB SELECT](https://duckdb.org/docs/current/sql/query_syntax/select). Retrieved 2026-10-09.
