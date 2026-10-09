# Cisco ISE network access diagnosis

Select the documented read path for a session-presence, applied-policy, authentication-failure, or authentication-latency symptom.

Sources: [official server schemas](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/server.py), [tool catalogue](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/docs/MCP_TOOLS_CATALOG.md), [authentication and MnT considerations](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/README.md), current main, retrieved 2026-10-09. Bindings and result fields are in [endpoints.md](endpoints.md).

## Diagnostic decision tree

1. **Connection or presence question → locate sessions.** A single username, MAC, NAS address, endpoint address or audit-session identifier selects a direct lookup. A second filter or ISE-node filter selects the time-windowed scan. Success is the returned matching count and bounded session sample, together with the lookup path. An empty sample is no matching active session in that scope; it is not a historical authentication-failure verdict. Missing or failed data remains an error.
2. **Applied posture, profile or authentication method question → enrich the known session.** The detail read returns the observed authentication result, profile, posture, identity group/store and response time. Username or MAC uses a direct lookup without a time window; MAC takes precedence when both are supplied. Missing posture is unknown, not noncompliance. Success requires actual returned detail; the count of returned samples is distinct from the total found.
3. **Why was access authorized → resolve matched policy.** The policy-enriched read associates the selected session with policy-set, authentication-rule and authorization-rule conditions, identity source, security group and failure actions. The native resolution errors or missing-policy note remain part of the finding. The current server projects some basic session fields out of this view; those values require the detail read instead of being assumed present.
4. **Authentication rejected → investigate AAA failure.** The failure read uses the endpoint MAC and username when available. Its documented search order is recent MAC authentication-status failures, then the MAC's latest session, then the username's latest session, stopping when failures are found. The first source is windowed; the session fallbacks are not. Success is a native failure reason/cause/resolution and execution trace. Unresolved catalogue codes retain a partial-context note; they are not replaced with guessed causes. An empty result cannot exclude a reject older than the window that never created a session.
5. **Authentication is slow → inspect execution latency.** The latency read selects the known identity and, if requested, caller-supplied response-time bounds. It returns the per-step timing and catalogue text. Missing timing or unresolved step text remains unavailable, not zero. The largest observed step supports a timing finding but does not prove an unreported root cause. No universal latency threshold is supplied by this procedure.
6. **Deployment count question → read counters.** The count operation returns active, posture-assessed and profiled session counts. The posture and profiler populations overlap and are subsets of active sessions, so addition would double-count. Failure of any counter fails the complete counter result instead of manufacturing a zero.

At every branch, publisher backpressure is a retryable busy result, not an authentication failure. The documented reaction is backoff before another heavy MnT query. Direct single-identifier lookups and aggregate counters avoid the expensive full-window scan; broadening scope is not a retry strategy.

## Patterns

- Direct identity lookups ignore the lookback window; the reported lookup/source field determines temporal coverage.
- Audit-session identifiers and accounting-session identifiers are different values.
- A bounded sample does not establish a complete endpoint inventory. Actual total and returned counts remain separate.
- The catalogue's AAA parameter table uses a MAC parameter name that differs from the current server schema. The binding follows the implementation, and supplies an explicit lookback because the catalogue's examples also disagree on its default.

## Known limitations

- MnT tools need username/password or a forwarded per-user credential; ISE Open-API client-certificate authentication alone does not authenticate MnT queries.
- This read-only procedure does not decide whether an endpoint deserves quarantine or change any identity group, authorization rule or session.
- The current schema permits zero lookback numerically while its description requires at least one minute; this procedure uses an explicit positive duration within the published maximum.
- Returned evidence can include user/device identifiers. Only the requested investigation scope belongs in the outcome.

## Tools

| Operation | Description | Category |
|---|---|---|
| Locate sessions | Query active session identifiers/counts | Read |
| Read applied session detail | Retrieve observed posture/profile/authentication facts | Read |
| Resolve matched policy | Retrieve the rules behind the session result | Diagnostic read |
| Investigate AAA failure | Retrieve failure catalogue context and execution trace | Diagnostic read |
| Inspect execution latency | Return step timing for selected sessions | Diagnostic read |
| Read deployment counters | Return active/posture/profiler counts | Read |

## Verification checklist

- The branch matches the symptom and uses the intended identity.
- Lookup/source and window applicability are reported accurately.
- Total counts, sample sizes, missing values and enrichment errors remain distinct.
- Failure reasons and timing findings come from returned evidence rather than arbitrary risk thresholds.
- Busy/authentication/transport errors were not treated as endpoint failures.
