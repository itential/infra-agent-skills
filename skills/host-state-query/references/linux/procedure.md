# Linux host inspection

Collect selected process, file metadata and client-build observations.

## Common Sequences

- Host observation: **Select scope** → **Read requested state** → **Report results**.

### Select scope

The request selects the host and desired process, directory or curl observation. A pre-established authenticated shell supplies the execution context. Missing utilities or permission failures are reported for the affected read; this procedure does not install software or raise privileges.

### Read requested state

- `ps -ef` reads all visible processes in full format. The process table includes identifiers, timing and command arguments; arguments can contain secrets, so raw rows are not suitable for unrestricted publication. A process-name match is not a service-health check.
- `ls -l -- /requested/path` reads long-format file metadata. The path is a supplied, safely quoted argument. Hidden names are omitted by default and directory contents are not traversed recursively. Exit 0 indicates success; 1 indicates a partial/minor problem; 2 indicates a serious failure. Neither failure is an empty directory result.
- `curl --version` reads the installed build version, supported protocols and feature flags without making a transfer. It does not verify network connectivity or remote TLS.

### Report results

Each observation retains host, command, time and native output or error. The report includes only requested non-secret fields. Counts and capability claims are limited to the command's visible selection.

## Patterns

File metadata does not establish file contents. A process snapshot does not measure sustained CPU load. No arbitrary shell pipeline is required.

## Known limitations

GNU/procps behavior is not a contract for ESXi or other Unix variants. No fixed critical CPU, memory or process-count thresholds are supplied.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authorized shell/SSH | Execute explicit read-only command payloads | Host read |

## Verification checklist

- Host and requested observation match.
- Exit/errors are preserved.
- Command arguments and other secrets are not exposed in the report.
- No service-health conclusion exceeds the observations.

## Sources

- [procps-ng ps manual](https://gitlab.com/procps-ng/procps/-/blob/master/man/ps.1). Retrieved 2026-10-09.
- [GNU ls invocation](https://www.gnu.org/software/coreutils/manual/html_node/ls-invocation.html). Retrieved 2026-10-09.
- [GNU long-format listing](https://github.com/coreutils/coreutils/blob/master/doc/coreutils.texi). Retrieved 2026-10-09.
- [curl manual: version](https://curl.se/docs/manpage.html#-V). Retrieved 2026-10-09.
