# Pybatfish snapshot bindings

Assumes a configured `Session` instance named `bf`.

| Operation | SDK call | Evidence / caution |
|---|---|---|
| Select network | `bf.set_network(name="<network>")` | Returns network name; creates it when lookup returns 404 |
| List snapshots | `bf.list_snapshots(verbose=False)` | Snapshot names; `verbose=True` returns metadata |
| Upload | `bf.init_snapshot("<snapshot-directory-or-zip>", name="<snapshot>", overwrite=False)` | Returns initialized name; explicit `overwrite=True` replaces an existing snapshot |
| Initialization issues | `bf.q.initIssues().answer().frame()` | Parsing/conversion issue table |
| Delete | `bf.delete_snapshot(name="<snapshot>")` | Returns `None` on normal completion; verify through listing |

Input layout: `<snapshot-root>/configs/<device-config-files>`, with optional publisher-documented supplemental folders. A ZIP contains `<snapshot-root>` rather than only its child files.

The SDK rejects omitted deletion names with `ValueError("Snapshot to be deleted must be supplied")`; other network/access/processing errors remain native exceptions. The network selector wraps non-404 access errors as a `BatfishException` with `Unknown error accessing network`.

Sources: [interaction guide](https://batfish.readthedocs.io/en/stable/notebooks/interacting.html), [session source](https://github.com/batfish/pybatfish/blob/master/pybatfish/client/session.py), retrieved 2026-10-09.
