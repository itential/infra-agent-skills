# SuzieQ collected-state query

The SuzieQ CLI reads collected tables and returns scoped records, aggregates, assertions or computed paths.

Sources: [Analyzer](https://suzieq.readthedocs.io/en/latest/analyzer/) and [CLI verbs](https://suzieq.readthedocs.io/en/latest/tutorials/how_to_think_about_verbs/), current documentation, retrieved 2026-10-09. This is the CLI procedure; installation and REST transport are outside scope.

## Common Sequences

- Table investigation: Discover fields → Read records → Summarize or Count values.
- Consistency check: Discover fields → Read records → Evaluate assertions.
- Path investigation: Discover fields → Compute path → Read records for the implicated tables.

The examples below use the interactive CLI after `suzieq-cli` starts. Placeholders stand for operator-selected values, not literal device names.

## Discover fields

`<table> help` identifies available verbs; `<table> help command=<verb>` identifies filters; `<table> describe` shows the schema. Successful output identifies the table, supported operation and valid field names. An unknown table, verb or filter is corrected against that help; a nearby name is not assumed equivalent. The ordinary table-query verbs do not apply to every specialized command.

## Read records

`<table> show namespace=<namespace> columns='<selected-columns>'` returns selected records. `columns='*'` requests all available fields. Hostname, time and view filters use the selected verb's help. A successful empty result means no matching collected records, not proof of absence on live devices. CLI or data-access errors remain errors.

## Summarize

`<table> summarize namespace=<namespace>` returns the table's per-namespace aggregates. The summary operation does not accept the columns selector. Three-value statistical lists in the documented summaries mean minimum, maximum and median; they are not chronological samples.

## Count values

`<table> unique namespace=<namespace> columns=<field>` returns distinct values and their counts for the selected field. The column is required. Success preserves counts and scope rather than treating uniqueness as a policy requirement.

## Evaluate assertions

`<table> assert namespace=<namespace>` is supported for BGP, OSPF, interfaces and EVPN VNI tables. The result includes pass/fail and reasons for failures. The CLI prints `Assert failed` for failed checks and returns a nonzero shell status (the docs describe -1 in the application, commonly observed as 255 by a shell). Failure reasons are evidence, not an instruction to modify devices. A query error is distinguished from a completed assertion with failed rows.

For a protocol symptom, the assertion reasons and corresponding protocol records identify the documented consistency checks that failed. For an interface symptom, its checks compare collected link attributes. An empty or incomplete collection cannot establish that every device passed.

## Compute path

`path show src='<source-ip>' dest='<destination-ip>' namespace=<namespace>` returns paths identified by path ID and hop number, with collected forwarding attributes and any hop errors. `path summarize` with the same arguments returns its aggregate view. Quoted IP arguments preserve the documented CLI parsing behavior. A hop error or failed query remains in the result rather than becoming a successful reachability claim.

## Patterns

The default latest view selects the latest collected change. All-history and time-window queries have different semantics: specifying both time bounds without the all view selects changes in that window. The installed help supplies the exact time-filter spellings. Collection retains changed data, so table row history is not a fixed-rate series of identical polls.

## Known limitations

Paths are inferred from collection data; the publisher identifies unsupported EVPN/overlay cases. Assertions cover the publisher's checks rather than an organization's compliance policy. Dynamic BGP peer mismatch and single-VXLAN-interface-for-all-VNIs cases are documented limitations. The referenced docs do not enumerate all stable error strings; unexpected errors require the installed platform's guidance.

## Tools

| Mechanism | Purpose | Category |
|---|---|---|
| Configured SuzieQ CLI session | Run table, assertion and path queries against collected data | Read |

## Verification checklist

- Namespace, table, filters and view match the requested collection scope.
- Output distinguishes empty data, query errors and assertion failures.
- Assertion reasons and path hop errors are preserved.
- The result describes collected/model state, with documented unsupported cases visible.
