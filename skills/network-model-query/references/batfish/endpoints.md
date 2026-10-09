# Pybatfish query bindings

Assumes `bf` is an already-configured `pybatfish.client.session.Session` for an existing network. `set_network` is deliberately excluded here because it creates a missing network.

| Operation | SDK binding | Native evidence |
|---|---|---|
| List/select snapshot | `bf.list_snapshots()`; `bf.set_snapshot(name="<snapshot>")` | Names; selected name |
| Initialization issues | `bf.q.initIssues().answer().frame()` | `Nodes`, `Source_Lines`, `Type`, `Details`, `Line_Text`, `Parser_Context` |
| Virtual traceroute | `bf.q.traceroute(startLocation="<location-spec>", headers=HeaderConstraints(srcIps="<source>", dstIps="<destination>"), maxTraces=<limit>, ignoreFilters=False).answer().frame()` | `Flow`, `Traces`, `TraceCount` |
| Reachability | `bf.q.reachability(pathConstraints=PathConstraints(startLocation="<location-spec>"), headers=<HeaderConstraints>, actions="<disposition-spec>", ignoreFilters=False).answer().frame()` | Example flows and traces; default action is `success` |
| Filter test | `bf.q.testFilters(nodes="<node-spec>", filters="<filter-spec>", headers=<HeaderConstraints>).answer().frame()` | `Node`, `Filter_Name`, `Flow`, `Action`, `Line_Content`, `Trace` |
| Filter search | `bf.q.searchFilters(nodes="<node-spec>", filters="<filter-spec>", headers=<HeaderConstraints>, action="deny").answer().frame()` | Actions also support `permit` or `matchLine <lineNumber>` |
| Route diff | `bf.q.routes().answer(snapshot="<candidate>", reference_snapshot="<reference>").frame()` | Native differential route columns |
| Reachability diff | `bf.q.differentialReachability(headers=<HeaderConstraints>, ignoreFilters=False).answer(snapshot="<candidate>", reference_snapshot="<reference>").frame()` | `Flow`, `Snapshot_Traces`, `Snapshot_TraceCount`, `Reference_Traces`, `Reference_TraceCount` |
| Filter diff | `bf.q.compareFilters(nodes="<node-spec>", filters="<filter-spec>").answer(snapshot="<candidate>", reference_snapshot="<reference>").frame()` | Current and reference filter-line columns |

Header constraints and selectors are Pybatfish typed inputs, not arbitrary JSON keys inferred from the NetClaw wrapper. Additional protocol/port constraints use the installed version's documented `HeaderConstraints` model. The examples are binding templates, not executable Python until placeholders are supplied.

Selection errors include `One of name and index must be set`, `Only one of name and index can be set`, and a `ValueError` describing the missing named snapshot. Index selection can raise `IndexError`; this procedure selects by explicit name. Query guides do not promise custom codes such as `FILTER_NOT_FOUND`.

Sources: [forwarding](https://batfish.readthedocs.io/en/stable/notebooks/forwarding.html), [filters](https://batfish.readthedocs.io/en/stable/notebooks/filters.html), [differential questions](https://batfish.readthedocs.io/en/stable/notebooks/differentialQuestions.html), [session source](https://github.com/batfish/pybatfish/blob/master/pybatfish/client/session.py), retrieved 2026-10-09.
