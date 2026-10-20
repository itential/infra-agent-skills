# Endpoint Wiring — AWS Network Firewall

Literal calls behind the capabilities in `procedure.md`.

Citation: AWS, "AWS Network Firewall API Reference", docs.aws.amazon.com/network-firewall,
retrieved 2026-10-19. The call shape (single POST with an action target header) comes from the
curated spec in itential/assets (`AWS/Network Firewall/OpenAPIs`) — secondary source, matches the
vendor's published action names; verify the header form against the API reference before relying on it.

Base URL: `https://network-firewall.<region>.amazonaws.com`. Every call is `POST /` with JSON body
and header `X-Amz-Target: NetworkFirewall_20201112.<Action>`, `Content-Type: application/x-amz-json-1.0`.
Auth: AWS Signature Version 4 (service `network-firewall`), normally produced by an AWS SDK or the
client's signing layer, not hand-built.

| Capability | `<Action>` | Key body fields |
|---|---|---|
| Create rule group | `CreateRuleGroup` | `RuleGroupName`, `Type` (`STATELESS`/`STATEFUL`), `Capacity`, `RuleGroup`, `DryRun` |
| List rule groups | `ListRuleGroups` | optional `Scope`, `NextToken` |
| Read rule group | `DescribeRuleGroup` | `RuleGroupName` + `Type` (or `RuleGroupArn`); response includes `UpdateToken` |
| Update rule group | `UpdateRuleGroup` | `UpdateToken`, name/ARN, `RuleGroup`, `DryRun` |
| Delete rule group | `DeleteRuleGroup` | name/ARN, `Type` |
| Create policy | `CreateFirewallPolicy` | `FirewallPolicyName`, `FirewallPolicy` |
| Read policy | `DescribeFirewallPolicy` | name/ARN; response includes `UpdateToken` |
| Update policy | `UpdateFirewallPolicy` | `UpdateToken`, name/ARN, `FirewallPolicy` |
| Delete policy | `DeleteFirewallPolicy` | name/ARN |
| Read firewall sync | `DescribeFirewall` | `FirewallName`; see `FirewallStatus.ConfigurationSyncStateSummary` (`PENDING`/`IN_SYNC`/`CAPACITY_CONSTRAINED`) and `Status` |

Errors to branch on: `InvalidTokenException` (stale token: re-describe, retry),
`InvalidOperationException` (e.g. deleting an in-use rule group or policy).
