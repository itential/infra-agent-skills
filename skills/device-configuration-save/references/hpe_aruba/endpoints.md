# AOS-CX 10.13 configuration bindings

Sources: [read](https://developer.arubanetworks.com/aoscx/v10.13/reference/get_fullconfigs-name), [copy](https://developer.arubanetworks.com/aoscx/v10.13/reference/put_fullconfigs-to), retrieved 2026-10-09.

Base: `https://<switch>/rest/v10.13`; existing authenticated session and CSRF handling are prerequisites.

| Operation | Binding | Input/result |
|---|---|---|
| Read running | `GET /fullconfigs/running-config` | 200 JSON configuration object |
| Read startup | `GET /fullconfigs/startup-config` | 200 JSON configuration object |
| Save running to startup | `PUT /fullconfigs/startup-config?from=/rest/v10.13/fullconfigs/running-config` | No body specified; 200 success |

The `from` value is an API resource path including the current version. Query encoding belongs to the HTTP client. `running-config` is the documented configuration name; the copy page's one occurrence of `runnig-config` is a publisher typo, not another supported name.

Both operations document 400 invalid request, 401 unauthenticated, 403 forbidden, 404 not found, 500 internal error and 503 unavailable. The reference supplies no response body for copy success or stable error-code payloads.
