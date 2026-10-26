# Endpoints — Citrix ADC (NetScaler) NITRO API

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever
authenticated REST client/adapter is assumed available for the target NetScaler/ADC appliance.

Source: NetScaler developer docs NITRO API reference ("current-release" tree, ADC 14.1 at retrieval
time), https://developer-docs.netscaler.com/en-us/adc-nitro-api, retrieved 2026-09-17 — specifically
the resource-operations guide, the basic load-balancing use case, the basic-operations guide, the
disable-service use case, and the error-messages reference.

## Base URL / resource pattern

Configuration objects: `http://<NSIP>/nitro/v1/config/<resource-type>`
Statistics: `http://<NSIP>/nitro/v1/stat/<resource-type>`

CRUD mapping confirmed for object-type resources such as `lbvserver`:
- Create: `POST /nitro/v1/config/<resource-type>` with the object nested under its own type name in
  the JSON body.
- Read all: `GET /nitro/v1/config/<resource-type>`
- Read one: `GET /nitro/v1/config/<resource-type>/<name>`
- Update: `PUT /nitro/v1/config/<resource-type>/<name>`
- Delete: `DELETE /nitro/v1/config/<resource-type>/<name>`

Binding-type resources follow the naming convention `<resource-type>_<bound-resource-type>_binding`
(confirmed for `lbvserver_service_binding`). The equivalent name for a `servicegroup` member binding
is Unverified, with no worked example — do not assume a
specific literal name for it without checking the target NetScaler's own current reference.

## Create a service (pool-member equivalent)

```
POST http://<NSIP>/nitro/v1/config/service
Content-Type: application/json

{
  "service": {
    "name": "<service-name>",
    "ip": "<backend-member-address>",
    "servicetype": "<HTTP|TCP|...>",
    "port": <port>
  }
}
```

**Success:** 2xx (this source described 200/201 as success codes generally; a specific success body
shape beyond standard HTTP status was not itemized for this exact call).
**Documented failure example (from the error-messages reference):** a service create can fail with
an error in the load-balancing/vserver error range whose documented message is "service exists with
the same port and service type" for a duplicate. Surface the platform's actual error response
verbatim for any other failure — this source's error catalog does not itemize every possible service
create failure.

## Create a virtual server (`lbvserver`)

```
POST http://<NSIP>/nitro/v1/config/lbvserver
Content-Type: application/json

{
  "lbvserver": {
    "name": "<vserver-name>",
    "servicetype": "<HTTP|TCP|...>",
    "ipv46": "<vip-address>",
    "port": <port>
  }
}
```

Note the VIP's own address field is `ipv46`, not `ip` (that name is used by the service object
instead — see above). No further optional-field catalog (e.g. an `lbmethod` load-balancing-algorithm
field) is documented with a worked example; if a caller needs to set the LB
algorithm, confirm the exact field name against the target NetScaler's own current reference before
scripting it rather than assuming a remembered field name is correct.

## Bind a service to a virtual server

```
PUT http://<NSIP>/nitro/v1/config/lbvserver_service_binding
Content-Type: application/json

{
  "lbvserver_service_binding": {
    "name": "<vserver-name>",
    "servicename": "<service-name>",
    "weight": "<weight-as-string>"
  }
}
```

Note this specific worked example used `PUT`, not `POST`, for the binding create — don't assume
every binding-type create uses the same verb as a plain object create without checking.

## Disable a service (graceful drain option)

```
POST http://<NSIP>/nitro/v1/config/service?action=disable
Content-Type: application/json

{"service":{"name":"<service-name>","graceful":"<Yes|No>","delay":<seconds>}}
```

`graceful: Yes` — stop accepting new connections; the service finishes disabling once existing
connections close. `delay` — seconds allowed for the graceful drain; during this window new requests
route to the service only for clients with an existing persistent session there. The one worked
example retrieved omitted `delay` even though the field is documented, and used a generic placeholder
IP/user (not a real credential — do not reuse literal doc placeholders as if they were realistic
production values).

**Re-enable:** Unverified, with no worked example — by extension of the same `?action=` query-parameter convention an `?action=enable` call is expected to
exist, but its exact required body was not found. Confirm directly against the target system's own
current reference before relying on it.

## Response envelope / errors

Confirmed fields: `errorcode` (numeric) and `message` (human-readable) exist in NITRO's error
responses; a `severity` field's presence was implied but not confirmed in a full worked example.
Documented error ranges seen in the error-messages reference: a base system-error range (e.g.
"NetScaler not running", "permission denied", "cannot allocate memory"), a network/configuration
range (e.g. "invalid interface name/number", "maximum manager limit reached"), a monitor/health-check
range (e.g. "monitor interval must be greater than response timeout"), and a load-balancing/vserver
range (e.g. the duplicate-service message quoted above). Do not fabricate a specific error string
for a condition not itemized here — surface the platform's actual response.

## Authentication

Two methods are both documented on this platform, and the sources do not fully reconcile
them into a single mechanism:

1. **Session login:** `POST /nitro/v1/config/login` with body
   `{"login": {"username": "<user>", "password": "<pass>"}}` and header
   `Content-Type: application/json`. Success is HTTP 201 Created with a `Set-Cookie:
   NITRO_AUTH_TOKEN=<token>; path=/nitro/v1` response header. Subsequent calls send
   `Cookie: NITRO_AUTH_TOKEN=<token>`.
2. **Per-call header credentials:** headers `X-NITRO-USER:<username>` and
   `X-NITRO-PASS:<password>` alongside `Content-Type: application/json`, described as an alternative
   to establishing a session.

One documented worked example (the disable-service use case) instead used a generic HTTP Basic Auth
flag (`curl -u <user>:<password>`) rather than either of the two mechanisms above spelled out
literally as headers — it is not confirmed from these sources whether that's a third equivalent
mechanism the platform accepts, or shorthand the doc author used that maps onto one of the two above.
Confirm the exact expected mechanism against the target NetScaler's own current documentation before
scripting authentication rather than assuming any one of these three forms is universally accepted.
