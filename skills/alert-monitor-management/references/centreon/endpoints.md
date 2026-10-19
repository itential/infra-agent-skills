# Endpoints — Centreon Host/Service Creation & Problem Acknowledge

Literal wiring layer for `procedure.md`. Base URL is instance-specific: `https://<centreon-server>`
plus the API v2 base path for the target version (assumption: the version-specific prefix, such as
`/centreon/api/latest`, is taken from the deployment; the OpenAPI definition lists paths relative to
its configured server). Source: Centreon REST API v2 OpenAPI definition 25.10, retrieved 2026-10-19.

## Authenticate

```
POST /login
```
Body carries the credentials under a `security` object. The response returns a token. Send it on
every later call in the `X-AUTH-TOKEN` header; the definition states a token unused for more than
one hour is deleted. A `PHPSESSID` cookie from an existing web session is also accepted.

## Create host

```
POST /configuration/hosts
```
Required: `monitoring_server_id` (integer), `name`, `address`. Optional examples: `alias`,
`check_command_id`, `check_command_args`, `check_timeperiod_id`, `max_check_attempts`,
`normal_check_interval`, `retry_check_interval`, `notification_enabled`, `templates` (IDs),
`groups` (IDs), `categories` (IDs), `macros`. Success: 201. Other documented statuses: 400, 403,
404, 409 (conflict), 500.

## Create service

```
POST /configuration/services
```
Required: `name`, `host_id`. Optional examples: `service_template_id`, `check_command_id`,
`check_command_args`, `max_check_attempts`, `normal_check_interval`, `retry_check_interval`,
`notification_enabled`, `service_groups`, `service_categories`, `macros`. Success: 201. Other
statuses: 400, 403, 404, 409, 500.

## Generate and reload the configuration

```
GET /configuration/monitoring-servers/{monitoring_server_id}/generate-and-reload
```
Success: 204. Statuses 403, 404, 500 also documented. Separate `.../generate` and `.../reload`
calls exist, as do the same calls without an ID that act on all monitoring servers; **the
all-servers variants affect every poller, so do not use them unless the operator asked for that**
(assumption: the no-ID variants apply to all monitoring servers, inferred from their path shape).

## Acknowledge a service problem

```
POST /monitoring/hosts/{host_id}/services/{service_id}/acknowledgements
```
Body fields: `comment`, `is_notify_contacts`, `is_persistent_comment`, `is_sticky`. Success: 204
("command sent"). Statuses 400, 403, 500 also documented. Minimum API version 21.10.

## Acknowledge a host problem

```
POST /monitoring/hosts/{host_id}/acknowledgements
```
Success: 204. Body fields (unverified): the definition's request schema is referenced indirectly
and was not resolved; assume the same field names as the service call.

## Cancel an acknowledgement

```
DELETE /monitoring/hosts/{host_id}/acknowledgements
DELETE /monitoring/hosts/{host_id}/services/{service_id}/acknowledgements
```
Success: 204 ("command sent"). Statuses 400, 403, 500 documented.

## List acknowledgements

```
GET /monitoring/hosts/{host_id}/acknowledgements
GET /monitoring/hosts/{host_id}/services/{service_id}/acknowledgements
```
Use to confirm an acknowledgement is recorded after the "command sent" response.
