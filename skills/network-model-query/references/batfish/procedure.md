# Batfish snapshot analysis

Analyze an existing Batfish network snapshot through a configured Pybatfish session, retaining model-initialization evidence and native query results.

## Common Sequences

- Packet or ACL analysis: **Select snapshot** → **Read initialization issues** → **Trace forwarding** or **Evaluate filter**.
- Before/after evidence: **Select snapshot** and **Read initialization issues** for each snapshot → **Compare snapshots**.

### Select snapshot

The configured session lists snapshots in its existing network and selects the requested name. Success is the selected name returned by the client. A nonexistent name is a selection error, not an empty topology. This procedure assumes the session's network already exists: the publisher's network-selection helper can create a missing network and is not treated as a read-only operation.

### Read initialization issues

The initialization-issues query returns model parsing/conversion findings, with affected nodes, source lines, issue type and detail where available. Success is the returned issue table; a warning remains part of subsequent results. A completed query does not establish that every construct in an uploaded configuration was modeled. Connection or service errors leave model quality unknown.

### Trace forwarding

A virtual traceroute uses the selected start location and packet constraints. Its result contains the evaluated flow, traces and total trace count. A reachability search instead returns examples matching the requested header, path and disposition constraints. Success is the native result table, not an assumption that the supplied source/destination alone tested every possible flow. The traceroute is directional; it does not establish return-path connectivity. A trace limit can omit traces even when the total count is larger.

### Evaluate filter

A filter test selects nodes, filter names and packet headers. Its result identifies the node, filter, evaluated flow, action, matching line and trace. The native permit/deny outcome is retained. Filter search can instead produce an example matching a requested permit, deny or specific-line behavior. An empty search result means no matching witness in the specified model and scope, not a global policy verdict.

### Compare snapshots

The query explicitly identifies the candidate/current and reference snapshots. A differential route query returns routing changes; a differential reachability query returns example flows that succeed in one snapshot but not the other, with separate traces/counts. Filter comparison identifies same-named filters whose line behaviors differ. Success preserves both snapshot identities and the native differential evidence. The publisher table uses potentially confusing BASE/DELTA prose; the explicit current/reference arguments and returned column names determine how the results are labeled here.

All query errors retain the service/client exception and scope. The cited question guides do not establish NetClaw's custom error-code strings or one complete error taxonomy. Invalid selectors, absent snapshots or unreachable services are not successful empty results.

## Patterns

Initialization issues qualify later findings. A concrete filter test and an existential reachability search have different coverage. The default reachability action searches successful flows; a requested failure disposition must be explicit.

## Known limitations

No device configuration, live packet probing or organization-specific compliance policy is executed. Snapshot upload/deletion is outside this read procedure. Model support and omitted configuration features limit the conclusions.

Sources: Pybatfish 0.36.0 [service interaction](https://batfish.readthedocs.io/en/stable/notebooks/interacting.html), [forwarding](https://batfish.readthedocs.io/en/stable/notebooks/forwarding.html), [filter questions](https://batfish.readthedocs.io/en/stable/notebooks/filters.html), [differential questions](https://batfish.readthedocs.io/en/stable/notebooks/differentialQuestions.html), and publisher [session implementation](https://github.com/batfish/pybatfish/blob/master/pybatfish/client/session.py), retrieved 2026-10-09. SDK bindings are in [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Select snapshot | List/select existing snapshot in the configured network | Read |
| Read initialization issues | Read parsing/conversion findings | Read |
| Trace forwarding | Query directional traces or reachability witnesses | Analyze |
| Evaluate filter | Query action, matched line and filter trace | Analyze |
| Compare snapshots | Query route, reachability or filter differences | Analyze |

## Verification checklist

- Network and exact snapshot identities accompany every result.
- Initialization issues are retained as model qualifications.
- Packet, path, filter and disposition constraints are explicit.
- Trace counts and returned traces are compared for truncation.
- Candidate and reference evidence are labeled consistently.
