# Ansible content validation

Run ansible-lint against selected content with an explicit profile.

### 1. Establish the execution context

The publisher requires execution from the project or collection root; running inside a role/tasks subdirectory can miss violations. `ansible-lint --version` and `ansible-lint --help` identify the installed CLI. Missing binaries or dependencies are environment failures, not a passing lint run.

The publisher warns that project Ansible configuration can invoke an executable vault-password provider. Untrusted content therefore belongs in an isolated environment, or uses controlled Ansible/vault configuration. This is a documented code-execution risk even though the requested operation is linting.

### 2. Resolve the requested rule set

`ansible-lint --list-profiles`, `ansible-lint --list-rules`, and `ansible-lint --list-tags` expose installed selections. The profile comes from the request or project configuration; the skill does not impose a company-wide production policy. Rules marked as not implemented in the publisher profile catalogue are not claimed as checks that ran.

### 3. Validate selected content

From the project root, the documented form is `ansible-lint --offline --profile <profile> --format sarif <playbook-or-role-path>`. Omitting paths enables project discovery. Offline mode prevents requirement installation and schema refresh; required dependencies must already exist. Syntax/load/parser errors prevent normal validation and remain failures; the procedure does not hide them by adding skip rules.

The linter writes findings to stdout and diagnostics/statistics to stderr. Both and the process exit code are retained. The optional `--strict` flag makes warnings cause a nonzero exit as well; it is used only when requested. Profile, excluded files, skipped rules and warning overrides remain part of the result.

### 4. Report validation

The report includes processed-file count, rule identifiers, locations, warnings/failures, selected profile and native exit result. A run that processed no intended files is incomplete. Corrected source can be checked with the same scope and profile; this procedure does not automatically edit it.

## Patterns

The usage page’s help block calls JSON a Code Climate alias, while its prose describes a newer SARIF alias. The procedure selects `sarif` explicitly to avoid that documentation inconsistency. Profile rules apply even when their opt-in/experimental tags would normally exclude them.

## Known limitations

Linting can create caches. Offline mode is not a code sandbox and does not prevent executable configuration. Lint results do not prove that credentials are absent or that an automation job is safe to deploy. Auto-fix and ignore-file generation are outside scope.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Isolated local CLI runner | Run ansible-lint and retain stdout/stderr/exit result | Local validation |

## Verification checklist

- Execution started at the project root.
- The intended files were processed.
- Profile, skips, warnings and failure locations are preserved.
- No deployment or complete secret-scan result is inferred.

## Sources

- [ansible-lint usage](https://docs.ansible.com/projects/lint/usage/). Retrieved 2026-10-09.
- [ansible-lint profiles](https://docs.ansible.com/projects/lint/profiles/). Retrieved 2026-10-09.
