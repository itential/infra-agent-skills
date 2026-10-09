# AWS IAM bindings

The AWS IAM MCP server is preconfigured with `--readonly`. IAM SDK actions use API version `2010-05-08` and the authenticated AWS partition/account configuration; credentials are not arguments in these examples.

| Operation | Literal binding | Inputs / returned evidence |
|---|---|---|
| List identities | `list_users`, `list_groups`, `list_roles` | Optional `path_prefix`, `max_items` (default 100) |
| List policies | `list_policies` | `scope`: `Local` (default), `AWS`, `All`; optional `only_attached`, `path_prefix`, `max_items` |
| Read user/group | `get_user(user_name=...)`, `get_group(group_name=...)` | Named identity with related metadata documented by the MCP publisher |
| Read role | IAM `GetRole(RoleName=...)` | `Role`, including `AssumeRolePolicyDocument` |
| List inline policies | `list_user_policies(user_name=...)`, `list_role_policies(role_name=...)` | Policy names |
| Read inline policy | `get_user_policy(user_name=..., policy_name=...)`, `get_role_policy(role_name=..., policy_name=...)` | Inline policy document |
| Read managed metadata | IAM `GetPolicy(PolicyArn=...)` | `Policy.DefaultVersionId` identifies the default version; this is not the document |
| Read managed version | IAM `GetPolicyVersion(PolicyArn=..., VersionId=...)` | `PolicyVersion.Document`; API policy documents are RFC3986 URL-encoded, and some SDKs decode them |
| Read credential report | IAM `GetCredentialReport()` | `Content` is base64; `GeneratedTime`; `ReportFormat=text/csv` |

Credential CSV columns used here include `user`, `arn`, `mfa_active`, password activity, and `access_key_1_*` / `access_key_2_*`. The guide explains field-specific `N/A` and `no_information` values; they are not interchangeable with false or zero. No secret access-key value is returned by these reads.

## Native conditions

- `GetRole`: `NoSuchEntity` (404), `ServiceFailure` (500).
- `GetPolicy` / `GetPolicyVersion`: `InvalidInput` (400), `NoSuchEntity` (404), `ServiceFailure` (500).
- `GetCredentialReport`: `ReportExpired` (410), `ReportNotPresent` (410), `ReportInProgress` (404), `ServiceFailure` (500).
- MCP error text and continuation behavior are not specified as stable contracts in its guide. Native failures are retained, not matched against invented strings.

Sources: [IAM MCP](https://awslabs.github.io/mcp/servers/iam-mcp-server), [GetRole](https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetRole.html), [GetPolicy](https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetPolicy.html), [GetPolicyVersion](https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetPolicyVersion.html), [GetCredentialReport](https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetCredentialReport.html), [CSV fields](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html), retrieved 2026-10-09.
