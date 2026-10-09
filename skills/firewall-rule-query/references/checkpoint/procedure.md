# Check Point Quantum Management policy-rule queries

Read a selected management domain's policy package, access layer, access rules or NAT rulebase using the publisher MCP server.

Sources: [Management MCP README](https://github.com/CheckPointSW/mcp-servers/blob/main/packages/management/README.md), [tool implementation](https://github.com/CheckPointSW/mcp-servers/blob/main/packages/management/src/index.ts), [API client](https://github.com/CheckPointSW/mcp-servers/blob/main/packages/infra/src/api-client.ts), current main with Management API v2.1/R82.10+ schema, retrieved 2026-10-09. Literal bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Access policy: Discover packages → Resolve access layer → Read access rulebase → Read selected rule.
- NAT policy: Discover packages → Read NAT rulebase.

### Discover packages

The package read uses the intended domain and full detail to expose package access-layer references. Returned packages and installation-target fields are configuration evidence, not proof that a gateway currently enforces that revision. An error stops discovery. Bounded pages continue using the response pagination position until the requested coverage is reached; partial retrieval remains partial.

### Resolve access layer

The known package's layer name or identifier selects a full layer read. The layer list can resolve an ambiguous name within the chosen domain, but another domain is not silently substituted. Success is the intended layer record. Missing/invalid identifiers or API errors remain failures.

### Read access rulebase

The selected layer name or identifier, optional package and optional supported search filter scope the rule read. The default returns a formatted bounded page; raw output retains the API structure when that is required. Success includes the returned rules and their position/total coverage. A rulebase formatting error remains a failed formatted result rather than a valid empty rulebase; a raw read can retrieve the underlying evidence. An embedded textual error also matters even when MCP transport did not fail.

The wrapper supports an all-pages option, but pagination completion must still be checked. Its accumulator preserves the first response's object dictionary and counts top-level rulebase entries; sectioned rulebases and objects encountered on later pages therefore require care. Bounded raw pages preserve each page's dictionary and original pagination metadata. A partial response is never promoted to a complete audit.

### Read selected rule

The rule read requires the access-layer identifier plus one rule name, UID or number. Optional hit data uses an explicit requested time/target scope. Success is the requested rule with its references and observed hit data. A zero hit count is scoped evidence, not permission to remove the rule. API errors remain errors.

### Read NAT rulebase

The known package selects its NAT rulebase, optionally filtered. The response's object references, rules and pagination metadata define the retrieved scope. Success is the requested NAT-rule page; subsequent pages retain the same package/domain/filter. Unlike the access-rulebase all-pages helper, this binding does not implement automatic NAT pagination. A missing package or API error stops the sequence.

## Patterns

- A management domain, policy package and access layer are separate scopes.
- Wire methods do not determine whether an operation is a read; these publisher query tools use management API read operations.
- Rule matching is configuration evidence, not a live packet-forwarding test.

## Known limitations

- The source skill spans many Check Point products. This procedure covers Quantum Management access/NAT reads only; threat intelligence, emulation, logs, gateway diagnostics, SASE and other products are separate unconverted surfaces.
- Earlier management releases may not support all v2.1 arguments.
- **Publisher security finding:** parts of the cited management API client's HTTPS handling disable certificate validation. A production deployment must establish verified transport; this procedure does not endorse those defaults.
- The automatic access-rulebase accumulator may leave later-page object references unresolved because it does not merge their dictionaries. The procedure retains page coverage and favors bounded raw pages when object fidelity matters.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover packages | Read policy packages and access-layer references | Read |
| Resolve access layer | List or read layer metadata | Read |
| Read access rulebase | Retrieve selected access rules and references | Read |
| Read selected rule | Retrieve one rule in an explicit layer | Read |
| Read NAT rulebase | Retrieve package-scoped NAT rules | Read |

## Verification checklist

- Domain, package and layer identify the requested policy.
- API/textual/formatting errors were checked in addition to MCP transport.
- Rule page positions, totals and object dictionaries were retained; incomplete retrieval remains explicit.
- No packet-flow or installed-policy verdict was inferred from stored rule configuration.
