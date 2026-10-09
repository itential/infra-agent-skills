# AWS IAM identity and credential metadata

Read IAM identities, policy documents and an existing account credential report using the AWS IAM MCP server in read-only mode and an authenticated IAM API client.

## Common Sequences

- Identity context: **List identities** → **Read identity context** → **Read policy documents**.
- Credential evidence: **Read credential report** → retain the report generation time and the documented meaning of unavailable fields.

### List identities

The IAM server lists users, groups, roles or managed policies for the requested account and optional path. Success is a returned collection of matching identity or policy records. Policy listing defaults to customer-managed policies; AWS-managed policies require the appropriate scope. A bounded MCP result is not proof that every account record was returned: the publisher documents a maximum-item argument, but no continuation argument on these tools. A completeness requirement therefore needs a separately documented IAM paginator.

Authentication failures require a usable credential context; permission failures identify unavailable evidence; validation failures require corrected inputs. Missing objects remain missing, rather than being interpreted as compliant.

### Read identity context

A user read supplies attached-policy, group and access-key metadata; a group read supplies membership and policy context. The IAM role API supplies the selected role and its trust-policy document. Success requires the returned identity to match the requested name and account. URL-encoded policy documents are decoded according to the API contract unless the client has already decoded them.

The role API's missing-entity condition means that role is unavailable; service failure leaves the read unresolved. The MCP publisher documents descriptive authentication, permission, validation and missing-resource errors without a fixed message contract.

### Read policy documents

An inline-policy collection identifies the user or role policy names to retrieve. For a managed policy, its metadata identifies the default version; that version is then read to obtain the document. Success is the document for the requested identity/policy/version, not merely the managed policy's descriptive metadata. Invalid input is corrected; absent policies are reported as absent; service failure leaves the document unavailable.

### Read credential report

The IAM API retrieves an already-generated account report. A successful result contains a report generation time and CSV content, which is decoded from its transport encoding. MFA state and password/access-key activity retain the CSV's literal unavailable-value semantics; lack of an activity timestamp does not establish that a credential is unused.

An expired or absent report ends this read with that native condition. A report still being generated can be retrieved after its generation completes. A service failure leaves the report unavailable. Generating or replacing a report is outside this read-only procedure.

## Patterns

IAM policy text is evidence about the policy document, not a complete effective-permissions decision. This scope does not evaluate service-control policies, resource policies, session policy effects or every other authorization constraint. Credential-report timestamps describe the generated report, not necessarily current state.

## Known limitations

No IAM mutations, report generation, policy simulation, credential rotation or compliance score are included. The MCP catalog does not document complete role attachment expansion here; policy text must not be inferred from a role name. Credential reports omit service-specific credentials and do not represent every credential type. Organization-defined age thresholds and mandatory-MFA judgments are outside this procedure.

Sources: [AWS IAM MCP server](https://awslabs.github.io/mcp/servers/iam-mcp-server), [credential-report guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html), and the IAM API references linked in [endpoints](endpoints.md), retrieved 2026-10-09.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| List identities | Read user, group, role or policy metadata | Read |
| Read identity context | Read a selected identity and documented related metadata | Read |
| Read policy documents | Retrieve selected inline or managed policy text | Read |
| Read credential report | Retrieve existing credential metadata with its generation time | Read |

## Verification checklist

- Account, identity name, policy identifier and selected version match the request.
- Collection bounds and missing authorization are visible in the result.
- Credential report generation time and unavailable fields are preserved.
- No absence, wildcard or credential age is silently converted into a compliance verdict.
