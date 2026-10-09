# Cisco Secure Firewall FMC: find matching policy rules

Search configured access/prefilter policies for a supplied network or identity indicator.

Sources: [Cisco FMC connector README](https://github.com/CiscoDevNet/CiscoFMC-MCP-server-community), [tool schema](https://github.com/CiscoDevNet/CiscoFMC-MCP-server-community/blob/main/sfw_mcp_fmc/server.py), and [search implementation](https://github.com/CiscoDevNet/CiscoFMC-MCP-server-community/blob/main/sfw_mcp_fmc/tools/search_access.py), main retrieved 2026-10-09. Bindings appear in [endpoints.md](endpoints.md).

## Common Sequences

- Known policy: Discover FMC → Search policy → Report matches.
- Device assignment: Discover FMC → Resolve target and search → Report matches.
- Domain search: Discover FMC → Search management scope → Report matches.

## Discover FMC

Profile discovery identifies configured FMC instances and the selected/default profile. The chosen profile and management domain establish the query scope.

Success: the profile identifies the intended controller. A profile-resolution or authentication failure ends the attempt; it does not establish that no policies exist.

## Search policy

A known access policy is searched by identifier for an IP, CIDR, or FQDN. The general search also supports explicit policy scope, policy identifier/name, access/prefilter selection and identity indicators.

Success: matching rules and referenced objects are returned, or a successful result has no matches. An invalid indicator requires corrected input; missing required policy scope or unsupported parameters cause validation failure. Ambiguous or missing policy resolution remains an error rather than a guessed selection.

## Resolve target and search

The target search resolves a firewall device, HA pair or cluster to its assigned policies, then searches the requested access and/or prefilter set. The returned resolution note and policy identities are part of the evidence.

Success: the intended target and assigned policy are resolved before its matches are reported. A missing assignment or unresolved/ambiguous target is a resolution failure; it is not a successful zero-rule result.

## Search management scope

Management-wide search uses the selected domain and optional policy/rule filters. Result and policy limits bound the query. The result records policies considered and scanned, matched-rule count, and a truncation indicator.

Success: metadata and returned rule records describe the requested bounded search. No-policy and unexpected connector errors remain native error outcomes.

## Report matches

The report retains policy identity/type, returned rule information, matched objects, selected indicator and all filters. Truncated results or limited policy scans are explicitly partial. A rule reference is not a packet-trace result or proof that a rule was deployed to the intended firewall.

## Patterns

Identity searches support security groups and realm users/groups in addition to network indicators. Target searches resolve policy assignment before matching; management-wide searches have a different scope and cannot be substituted without changing the meaning of the result.

## Known limitations

The publisher's HTTP mode does not reliably enforce the earlier documented bearer-token mechanism; its README states that it runs without that authentication. A secured local or externally authenticated deployment is a prerequisite. Example configurations disable TLS verification; that is an unsafe example default, not a requirement of policy search.

No universal traffic decision, shadow-rule diagnosis, retry schedule or policy-deployment status is inferred from this connector's search results.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover FMC | List configured instances and profile identifiers | MCP query |
| Search policy | Match one known policy's indicator references | MCP query |
| Resolve target and search | Find assigned policies then their matching rules | MCP query |
| Search management scope | Search access/prefilter policies with explicit filters | MCP query |

## Verification checklist

- FMC profile, domain and policy/device scope match the request.
- Indicator interpretation and filters remain visible.
- Resolution/validation errors are distinguished from zero matches.
- Truncation and policy limits qualify any completeness claim.
