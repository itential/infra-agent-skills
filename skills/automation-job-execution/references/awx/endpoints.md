# Endpoints — AWX Job Execution

Literal wiring layer for `procedure.md`.

Sources: `ansible/awx` repository — `awx/api/templates/api/job_template_launch.md`, `job_cancel.md`,
`job_relaunch.md`, `unified_job_stdout.md`, `awx/api/urls/{urls,job,job_template}.py` (routes), and
`docs/docsite/rst/rest_api/authentication.rst`;
retrieved 2026-10-19. Base path is `https://{awx-host}/api/v2/`.

## Authentication

- **Basic:** send `Authorization` basic credentials on every request (stateless).
- **Session:** GET `/api/login/` to obtain a `csrftoken` cookie, then POST `/api/login/` with
  username, password and the `X-CSRFToken` header; subsequent requests carry the session cookie (the
  response header `X-API-Session-Cookie-Name` names the cookie). Sessions expire (default timeout in
  the source's example: 1800 s).

## Read launch requirements

```
GET /api/v2/job_templates/{id}/launch/
```

Fields: `can_start_without_user_input`, `passwords_needed_to_start`, `variables_needed_to_start`,
`survey_enabled`, `inventory_needed_to_start`, and `ask_*_on_launch` flags (variables, tags,
skip_tags, job_type, limit, inventory, credential).

## Launch job template

```
POST /api/v2/job_templates/{id}/launch/
```

Body: any required passwords, `inventory` (if `inventory_needed_to_start`), `extra_vars` (YAML/JSON
string), and other prompted fields. **Success:** `201`. **Failure:** `400` missing password, `405`
cannot launch, `403` credential/inventory not allowed.

## Get job

```
GET /api/v2/jobs/{id}/
```

`status` values: `new`, `pending`, `waiting`, `running`, `successful`, `failed`, `error`, `canceled`.

## Get job stdout

```
GET /api/v2/jobs/{id}/stdout/?format=txt
```

`format`: `api`, `html`, `txt`, `ansi`, `json`, `txt_download`, `ansi_download`. `start_line` /
`end_line` select a range for the browsable API, HTML and JSON formats. Output above the configured
display limit must use a `_download` format.

## Check / cancel job

```
GET  /api/v2/jobs/{id}/cancel/     -> can_cancel (boolean)
POST /api/v2/jobs/{id}/cancel/     -> 202 success, 405 cannot cancel
```

## Relaunch job

```
GET  /api/v2/jobs/{id}/relaunch/   (what is required)
POST /api/v2/jobs/{id}/relaunch/   (passwords/variables in the body)
```
