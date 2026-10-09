# FortiManager console bindings

Sources and versions are cited in [procedure.md](procedure.md). This binding uses published UI controls; no HTTP API route is inferred from them.

| Operation | Console binding |
|---|---|
| Open wizard | Correct ADOM → `Device Manager` → `Device & Groups` → `Install Wizard` or `Install` → `Install Wizard` |
| Select mode | `Install Policy Package & Device Settings`; `Policy Package`, `Comment`, optional `Create ADOM Revision`, `Revision Name`, `Revision Comments` |
| Set schedule | Optional `Schedule Install`, `Date`, `Time` |
| Validate | `Next` → select device(s)/group(s) → `Next`; validation results and error-message links |
| Preview | `Install Preview`; `Assigned Devices` selects the device; optional `Download` |
| Compare policy | Optional `Policy Package Diff` |
| Execute | `Install` or `Schedule Install`, following the procedure's inline confirmation gate |
| Complete | Read per-device installation results, then `Finish` |

The installation wizard documentation does not enumerate all terminal status strings. The actual displayed result, warnings and errors remain the outcome vocabulary; no invented common success enum is used.
