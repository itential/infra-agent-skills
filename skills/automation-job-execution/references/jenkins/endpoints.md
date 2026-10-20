# Endpoints — Jenkins Build Trigger

Literal wiring layer for `procedure.md`.

Sources: jenkins.io "Remote access API" and "Authenticating scripted clients"; retrieved 2026-10-19.
Base: `{JENKINS_URL}`. Items below marked UNVERIFIED are not in a primary page read for this skill.

## Authentication

HTTP Basic with the user name and the user's API token (found on the user's security page). Send on
the first request. Unauthenticated requests receive 403.

## Trigger build (no parameters)

```
POST {JENKINS_URL}/job/{JOBNAME}/build
```

For multibranch pipelines and organization folders this triggers a scan.

## Trigger build (with parameters)

```
POST {JENKINS_URL}/job/{JOBNAME}/buildWithParameters
```

String parameters as `--data name=value`; file parameters as multipart `--form NAME=@path`, with the
job's file-location field matching the form key.

## Get crumb (only if CSRF protection requires it)

```
GET {JENKINS_URL}/crumbIssuer/api/json
```

Response gives `crumbRequestField` (header name) and `crumb` (value). API tokens are preferred.

## Build result values

`SUCCESS`, `UNSTABLE`, `FAILURE`, `NOT_BUILT`, `ABORTED` (Jenkins Javadoc `hudson.model.Result`).

## UNVERIFIED — not in a primary page read

- Queue item lookup (trigger response reference to queue item to build number).
- Build state read route and result field name.
- Stop/abort build route.
