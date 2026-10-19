# Endpoints — Versa Director, branch device onboarding

Literal wiring layer for `procedure.md`. Operation names in the procedure's Tools table map to the
calls below. Written against the Versa Director REST API Overview and the Activate VOS Devices page
(docs.versa-networks.com), retrieved 2026-10-19. Only routes those pages actually show are listed; every
other operation has no verified binding.

## Base URL and API families

Calls go to `<director_host>`. The overview names three path families: `/api/config` and
`/api/operational` (generated from the data model) and `/vnms` (custom APIs). Basic authentication is
served on port 9182 and OAuth 2.0 bearer tokens on port 9183, per the overview.

## authenticate

- Basic: HTTP Basic credentials of a Director user over HTTPS.
- OAuth 2.0: the overview lists a client-creation call, a token call, a refresh call, and a revoke call
  under the `/auth` path, with password and refresh-token grants. Send `Authorization: Bearer <token>`.
- Send `Content-Type: application/json` and `Accept: application/json`.
- Token lifetime is not stated in the overview (unknown).

## create_workflow_device

`PUT /vnms/sdwan/workflow/devices/device/<device-name>` — shown in the overview as the create-device
example. The request body schema is not on the pages used; read it from the Director's own API
documentation page (Director UI: user menu, then the API documentation entry) before building the call
(unverified).

## query_devices

`GET /vnms/sdwan/workflow/devices?offset=<n>&limit=<n>` — lists workflow devices with paging, per the
overview's example. Filtering by name is not shown (unverified); page through results and match the name.

## generate_activation_url / read the URL mapping

`GET /vnms/sdwan/device-url-mappings/device-url-mapping/<device-name>` — returns the URL-based
activation mapping for a device, per the Activate VOS Devices page. The page presents this as a
verification query; generating the link itself is described as a Director UI action (assumption: no
documented REST call generates it).

## read_tasks, read_device_status, commit_template, read_organization, read_device_group, read_template

No route for these is shown on the pages used. The overview says task monitoring uses separate task
management APIs without naming them. Use the Director UI, or take the route from the Director's own API
documentation page. Do not guess a path.

## Errors

- Status codes listed for the data-model APIs: 200, 201, 204, 400, 401, 500.
- The custom APIs return standard HTTP statuses and, optionally, a JSON body with fields named
  `http_status_code`, `code`, and `message`. Report them verbatim as FAILED detail. Rate limiting is not
  documented; on an HTTP 429, back off and honor any `Retry-After` header.
