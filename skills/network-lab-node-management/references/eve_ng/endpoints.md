# EVE-NG node lifecycle: bindings

An authenticated cookie-backed JSON client for the configured EVE-NG server is already available. Paths are relative to that server; `{lab_path}` is the URL-encoded folder/file path, including `.unl`. No credentials or insecure TLS flags are embedded.

| Operation | Binding | Input/result |
|---|---|---|
| Templates | `GET /api/list/templates/`; `GET /api/list/templates/{template}` | Available templates and image/settings options |
| Create | `POST /api/labs/{lab_path}/nodes` | Required `type`, `template`; selected `image`, `name`, `config`, resources and layout from template; result includes node identifier |
| Inspect | `GET /api/labs/{lab_path}/nodes`; `GET /api/labs/{lab_path}/nodes/{node_id}` | Node data; native `status`, `url` |
| Interfaces | `GET /api/labs/{lab_path}/nodes/{node_id}/interfaces` | Ethernet/serial interface mapping |
| Start/stop/wipe | `GET /api/labs/{lab_path}/nodes/{node_id}/{action}` | `action`: `start`, `stop`, `wipe`; **mutating GET** |

`config` is documented as `Unconfigured` or `Saved`. The selected template determines resource fields; IOL `ethernet` counts groups of four interfaces, whereas QEMU `ethernet` counts interfaces.

**Node start failed:** `Failed to start node (12).` The native envelope may contain `code: 400`, `status: "fail"`; it is not a success acknowledgement.


## Sources

- [EVE-NG API guide (version not specified; publisher warns of outdated examples)](https://www.eve-ng.net/index.php/how-to-eve-ng-api/). Retrieved 2026-10-09.
