# DuckDB exported-data query: bindings

The configured DuckDB client owns an in-memory database. The following are native SQL bindings; filenames and values are supplied safely by the client rather than interpolated from untrusted strings.

| Operation | Binding | Scope |
|---|---|---|
| Load JSON | `CREATE TABLE export_data AS SELECT * FROM read_json('<authorized-file>', format='newline_delimited');` | Trusted initialization; JSONL input only for this explicit format |
| Load CSV | `CREATE TABLE export_data AS SELECT * FROM read_csv('<authorized-file>', header=true);` | Trusted initialization; actual delimiter/header/schema required |
| Disable extension acquisition | `SET autoload_known_extensions=false; SET autoinstall_known_extensions=false; SET allow_community_extensions=false;` | Before untrusted input; required formats must already be available |
| Restrict external access | `SET enable_external_access=false; SET lock_configuration=true;` | After materialization; not a standalone sandbox |
| Describe/count | `DESCRIBE export_data;`; `SELECT count(*) AS loaded_rows FROM export_data;` | Actual schema; loaded count |
| Preview | `SELECT * FROM export_data LIMIT 20;` | Explicit example preview size, not a vendor limit |
| Controlled query | `connection.execute('SELECT * FROM export_data WHERE field_name = ?', [value])` | Python DB API parameter binding; `field_name` must be a verified fixed identifier |

Known restriction messages include `Cannot access file` when external access is blocked and `Cannot upgrade allow_community_extensions setting while database is running` when attempting to re-enable that disabled capability. These are safeguards, not errors to work around.


## Sources

- [DuckDB security model](https://duckdb.org/docs/current/operations_manual/securing_duckdb/overview). Retrieved 2026-10-09.
- [DuckDB JSON reader](https://duckdb.org/docs/current/data/json/loading_json). Retrieved 2026-10-09.
- [DuckDB CSV reader](https://duckdb.org/docs/current/data/csv/overview). Retrieved 2026-10-09.
- [DuckDB SELECT](https://duckdb.org/docs/current/sql/query_syntax/select). Retrieved 2026-10-09.
