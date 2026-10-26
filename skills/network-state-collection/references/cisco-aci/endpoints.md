# Cisco ACI APIC — State Collection Wiring

Source (Cisco, APIC REST API Configuration Guide, "Using the REST API", retrieved 2026-10-26). Placeholders: `{apic}`, `{user}`, `{password}`, `{dn}`, `{page}`, `{size}`.

Base: `https://{apic}`. The deployed model reference is served by the controller at `/doc/html/`.

## Authentication

| Operation | Call | Notes |
|---|---|---|
| Log in | `POST /api/aaaLogin.json` with `{"aaaUser":{"attributes":{"name":"{user}","pwd":"{password}"}}}` | Token is then sent as cookie `APIC-cookie`. Opens a session only; no configuration changes. The logout method is documented to return a response without ending the session; the session ends when refreshes stop. |
| Refresh | `GET /api/aaaRefresh.json` | Resets the timer and returns a new token. Default session timeout 600 s |

## Calls

| Operation | Method and path | Query options |
|---|---|---|
| System nodes | `GET /api/class/topSystem.json` | `page`, `page-size` |
| Attached endpoints | `GET /api/class/fvCEp.json` | `page`, `page-size` |
| Faults | `GET /api/class/faultInst.json` | `query-target-filter=and(eq(faultInst.cause,"config-failure"))` for configuration failures |
| Managed object | `GET /api/mo/{dn}.json` | `query-target=self`; optional `rsp-subtree-include=health` or `faults` where supported |

Page cap: from release 5.1(1), a page with more than 2000 objects is cut to 2000. Class names and attributes vary by release; check them against the model reference served by the controller. The `/api/node/class` and `/api/node/mo` forms are documented aliases. `.json` or `.xml` must end the path. Paging: `page={page}` (starts at 0) and `page-size={size}`; ordering `order-by=<class>.<property>|asc` or `|desc`. A response has `imdata` (objects keyed by class, each with `attributes` and optional `children`) and `totalCount`.

## Documented error strings

| Condition | Text | Handling |
|---|---|---|
| Timeout after 90 s (HTTP 503) | `Unable to deliver the message, destination is not available` | Retry three to five times |
| More than 100,000 objects | `Unable to process the query, result dataset is too big` | Narrow filters or scope |

## Unverified

- Whether `order-by` can combine with `query-target-filter` on every release; not stated.
