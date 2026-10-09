# ComfyUI image workflow execution: bindings

Paths are relative to the configured ComfyUI instance; no public default server is supplied.

| Operation | Binding | Fields |
|---|---|---|
| Node information | `GET /object_info` or `/object_info/{node_class}` | Node schemas |
| Models | `GET /models/{folder}` | Available model names |
| Submit | `POST /prompt` | JSON `prompt` workflow object; optional `client_id`; current server accepts a canonical UUID `prompt_id` |
| Queue | `GET /queue` | Current pending/running items |
| History | `GET /history/{prompt_id}` | Prompt-keyed entry with `outputs` |
| Progress | WebSocket `/ws?clientId={client_id}` | Match `data.prompt_id`; `executing` with `data.node=null` marks completion in publisher example |
| Image | `GET /view` | Query `filename`, `subfolder`, `type` from `outputs[node_id].images` |

Submission success includes `prompt_id`, `number`, `node_errors`. HTTP400 validation errors include `error` plus `node_errors`; current invalid-ID code is `invalid_prompt_id`, missing workflow `no_prompt`. Output retrieval can return400,403,404 for invalid/out-of-scope/missing files. No automatic path repair is performed.

## Sources

- [ComfyUI server routes](https://docs.comfy.org/development/comfyui-server/comms_routes). Retrieved 2026-10-09.
- [Publisher end-to-end WebSocket/history/image example](https://github.com/comfyanonymous/ComfyUI/blob/master/script_examples/websockets_api_example.py). Retrieved 2026-10-09.
- [Publisher server validation](https://github.com/comfyanonymous/ComfyUI/blob/master/server.py). Retrieved 2026-10-09.
