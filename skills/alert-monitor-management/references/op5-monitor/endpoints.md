# Endpoints — OP5 Monitor Host/Service Creation & Problem Acknowledge

Literal wiring layer for `procedure.md`. Base URL is instance-specific: `https://<op5-monitor-server>/api`.
Authentication in the sources: HTTP basic authentication; send `Content-Type: application/json`.
Sources retrieved 2026-10-19 (see `procedure.md`).

## Create host

```
POST /api/config/host
```
Body fields named in the source: `file_id` (for example the standard hosts file), `host_name`,
`template`; optional settings such as `max_check_attempts`, `notification_interval`,
`notification_options`, `notification_period`. Success and error response bodies are not described
in the source.

## Create service

```
POST /api/config/service
```
Body fields named in the source: `file_id` (the standard services file), `host_name`,
`service_description`, `check_command`, `template`.

## List, save and discard pending changes

```
GET    /api/config/change
POST   /api/config/change
DELETE /api/config/change
```
GET lists the staged changes, POST saves and exports them, DELETE reverts the unsaved set.

## Acknowledge a host problem

```
POST /api/command/ACKNOWLEDGE_HOST_PROBLEM
```
Body fields: `host_name`, `comment`, `sticky`, `notify`, `persistent`.

## Acknowledge a service problem

```
POST /api/command/ACKNOWLEDGE_SVC_PROBLEM
```
Body fields: `host_name`, `service_description`, `comment`, `sticky`, `notify`, `persistent`.

## Command help

The source states the server publishes help for its commands at a `help/command` page under the
API path (unverified path shape: taken from a search-result summary rather than the pages above).
Use it to confirm parameters and to find the command for removing an acknowledgement.
