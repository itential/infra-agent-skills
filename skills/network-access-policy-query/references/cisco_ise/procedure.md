# Cisco ISE network-access policy queries

Retrieve RADIUS policy sets and their authentication/authorization rules without changing policy.

Sources: [official tool catalogue](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/docs/MCP_TOOLS_CATALOG.md), [server schemas](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/server.py), current main, retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Authentication review: Discover policy sets → Read authentication rules → Verify coverage.
- Authorization review: Discover policy sets → Read authorization rules and global exceptions → Verify coverage.

### Discover policy sets

The filtered policy-set read returns names in ascending evaluation rank, with state, condition summary and hit count. Names, not internal UUIDs, supply the next operation's scope. Success is the requested collection with returned/total counts and the more-results flag. Missing hit counts are represented as zero by the publisher; zero alone therefore cannot prove the rule never matched.

### Read authentication rules

An exact policy-set name narrows the query; omission expands it across policy sets subject to the publisher's fan-out bound. An optional identity-source filter uses case-insensitive exact matching, while a rule-name filter uses substring matching. Success returns the identity source and documented authentication/user-not-found/process-failure actions for each matching rule. Failure or missing policy-set coverage remains visible; an empty filtered result does not prove a differently named identity source is unused.

### Read authorization rules and global exceptions

The authorization read applies the chosen policy-set, profile, security-group, state, hit-count and name filters. Profile and security-group filters use case-insensitive exact names. The publisher also returns matching global exception rules, including when a single policy set was named; these can override policy-set authorization rules. Success includes both the per-policy-set rules and global exceptions. A global-exception fetch error fails the entire call, so it cannot be treated as an empty exception list.

### Verify coverage

The result compares policy sets scanned with the total and separately records whether the rule result was truncated. These are independent coverage limits. Success is the requested evidence with exact counts/filters; incomplete scans remain partial even if no rule truncation occurred. Native rules and actions are reported without a universal permissiveness score or cleanup recommendation.

## Patterns

- Global exceptions are part of authorization evidence, not an optional follow-up inferred from the number of returned rules.
- Name matching semantics differ across filters; a substring is not an exact profile/store match.
- Hit-count filtering is selection, not proof that removing a rule is safe.

## Known limitations

- The wrapper limits rule fan-out and return counts; it does not establish complete policy coverage from a single unfiltered call.
- This scope excludes TACACS/device-administration policies, policy mutation, endpoint-group lifecycle and quarantine.
- Applied live-session facts require a session investigation; stored policy does not establish the last authorization actually used.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover policy sets | Read names/order/state/conditions | Read |
| Read authentication rules | Read identity-source and failure-action configuration | Read |
| Read authorization rules | Read profile/SGT conditions and global exceptions | Read |

## Verification checklist

- Names and matching semantics correspond to the intended scope.
- Authorization evidence includes matching global exceptions.
- Fan-out coverage and rule truncation were checked separately.
- Missing hit counts and empty filtered results were not converted into cleanup or compliance verdicts.
