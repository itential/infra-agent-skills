# ComfyUI image workflow execution

Run an already supplied ComfyUI workflow on the explicitly selected server.

## Common Sequences

- Generate: **Inspect prerequisites** → **Submit workflow** → **Observe completion** → **Retrieve images**.

### Inspect prerequisites

Node information and model catalogues establish that the supplied workflow's node classes/models are available on the selected server. Missing dependencies leave execution unsupported. The connection targets only that approved backend; no port scanning or alternate instance discovery is implied. Custom nodes are executable server code, not inert prompt data.

### Submit workflow

Submission consumes compute and the workflow may write files or call services: stop and confirm with the operator before proceeding. The API validates the supplied workflow and returns a prompt identifier and queue number, or validation errors. Node errors are retained even in an accepted response. Missing prompt, malformed identifiers or failed validation are corrected before a new submission. An uncertain transport result is inspected by the known identifier/queue before any repeat.

### Observe completion

The native queue/history or correlated WebSocket events track the accepted identifier. A node-executed event alone is not whole-workflow completion. The publisher example uses the executing event with a null node and matching prompt identifier as the completion signal, then reads history. Error/interruption outcomes remain failures, and an absent history entry alone is not proof of success or failure. No fixed polling rate is documented here.

### Retrieve images

History provides each output node's image descriptors. The image read uses the returned filename, subfolder and storage type. Successful retrieval yields the requested image bytes; a missing/forbidden/invalid path is a retrieval failure. The output is kept in the requested new artifact location; before overwriting an existing artifact, stop and confirm with the operator before proceeding. Output existence does not establish accurate topology, labels or connectivity.

## Patterns

Native prompt identity joins submission, completion and outputs. Preview frames do not substitute for the completed output images.

## Known limitations

No queue clearing, interruption of other jobs or history deletion is included. Authentication and isolation depend on the deployed server. Visual correctness requires checking the resulting artifact against the supplied specification.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Inspect nodes/models | Read workflow prerequisites | Read |
| Submit | Queue an approved workflow | Compute/file change |
| Track/read output | Read job state and resulting images | Read |

## Verification checklist

- Correct backend and required nodes/models are established.
- Prompt ID is retained across all stages.
- Validation/execution/output failures remain distinct.
- Output images match history descriptors and are inspected.

## Sources

- [ComfyUI server routes](https://docs.comfy.org/development/comfyui-server/comms_routes). Retrieved 2026-10-09.
- [Publisher end-to-end WebSocket/history/image example](https://github.com/comfyanonymous/ComfyUI/blob/master/script_examples/websockets_api_example.py). Retrieved 2026-10-09.
- [Publisher server validation](https://github.com/comfyanonymous/ComfyUI/blob/master/server.py). Retrieved 2026-10-09.
