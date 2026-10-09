# EVE-NG lab lifecycle: bindings

An authenticated cookie-backed JSON client for the configured EVE-NG server is already available. Paths are relative to that server; `{lab_path}` is the URL-encoded folder/file path, including `.unl`. No credentials or insecure TLS flags are embedded.

| Operation | Binding | Input/result |
|---|---|---|
| Discover | `GET /api/folders/{folder_path}` | `data.folders`, `data.labs` |
| Session/system | `GET /api/auth`; `GET /api/status` | Current user; system statistics |
| Create | `POST /api/labs` | `path`, `name`, `version`, `author`, `description`, `body`; success message number 60019 |
| Inspect | `GET /api/labs/{lab_path}`; `GET /api/labs/{lab_path}/nodes` | Lab metadata; node records |
| Start/stop all | `GET /api/labs/{lab_path}/nodes/start`; `GET /api/labs/{lab_path}/nodes/stop` | Mutating GET operations; envelope result |
| Delete | `DELETE /api/labs/{lab_path}` | Success message number 60022 |

Envelope: `code`, `status`, `message`, optional `data`. Native status words include `success`, `unauthorized`, `forbidden`, `fail`, `error`. These are retained in the report.


## Sources

- [EVE-NG API guide (version not specified; publisher warns of outdated examples)](https://www.eve-ng.net/index.php/how-to-eve-ng-api/). Retrieved 2026-10-09.
