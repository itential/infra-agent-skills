# Endpoints — Thruk Configuration & Problem Acknowledge

Literal wiring layer for `procedure.md`. Base URL is instance-specific; the documentation's
examples place the API under a `/thruk/r/` path on the Thruk host (assumption for a given
deployment). Authentication: the `X-Thruk-Auth-Key` header carries an API key (created from a
user's profile when API keys are enabled); basic authentication is possible but discouraged. A
superuser key can act as another user through the `X-Thruk-Auth-User` header. Sources retrieved
2026-10-19 (see `procedure.md`).

## Create a configuration object

```
POST /config/objects
```
Body: the object's attributes plus the special parameters `:TYPE` (for example `host`) and
`:FILE` (the configuration file). The documented example sends JSON with `:TYPE`, `:FILE` and
`name`. The response format is not documented.

## Change or delete an existing object

```
POST   /hosts/{name}/config
PATCH  /hosts/{name}/config
DELETE /hosts/{name}/config
POST   /services/{host}/{service}/config
PATCH  /services/{host}/{service}/config
DELETE /services/{host}/{service}/config
```
POST replaces the object entirely, PATCH changes only the sent attributes, DELETE removes it.

## Apply a staged change

```
GET  /config/diff
POST /config/save
POST /config/check
POST /config/reload
POST /config/revert
```
Run in the order diff, save, check, reload; revert discards staged changes.

## Acknowledge a service problem

```
POST /services/{host}/{service}/cmd/acknowledge_svc_problem
```
Required: `comment_data`. Optional: `sticky_ack`, `send_notification`, `persistent_comment`,
`comment_author`.

## Acknowledge a host problem

```
POST /hosts/{name}/cmd/acknowledge_host_problem
```
Required: `comment_data`. Optional: `sticky_ack`, `send_notification`, `persistent_comment`,
`comment_author`.

## Remove an acknowledgement

```
POST /services/{host}/{service}/cmd/remove_svc_acknowledgement
POST /hosts/{name}/cmd/remove_host_acknowledgement
```
No arguments.

## Generic command endpoint

```
POST /cmd
```
Form data: `cmd` (command name), `host`, `service`, `comment_data`, plus command-specific
parameters.
