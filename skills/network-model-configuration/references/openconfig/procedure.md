# OpenConfig gNMI: apply one configuration transaction

Apply an approved set of model-defined deletes, replacements, or updates atomically.

Source: [gNMI specification](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md), v0.11.0, sections 3.1, 3.2 and 3.4, retrieved 2026-10-09. Bindings appear in [endpoints.md](endpoints.md).

## 1. Establish supported scope

The authenticated TLS session discovers the target version, supported models and encodings. The payload uses valid model paths and schema-compatible values. Complete keys identify list entries. Conflicting key values or an invalid scalar type cause an invalid-argument response rather than a partial correction by the server.

Success: the requested paths, complete keys and encoding match the target schema. Authentication or permission failure stops the change.

## 2. Form the transaction

A single transaction contains all operations that must succeed together. The server processes deletions, replacements, then updates, preserving order within each operation group. An update changes only specified values; a replacement can remove omitted configuration or restore schema defaults. Deleting a subtree recursively deletes its children; deleting an already absent path succeeds. A replacement with a null value or an empty keyed-list object is not a valid way to delete it.

Success: the operator can review exactly which paths and descendants may change. This procedure does not use union-replace, which cannot be mixed with these operation groups.

## 3. Apply the approved transaction

**This changes live configuration: stop and confirm with the operator before proceeding.** The client submits the complete reviewed transaction through the configuration-change operation.

Success: the RPC reports success and its ordered operation results correspond to every requested change. If any operation fails, the specification requires the whole transaction to fail and restores its prior state. The error is retained for the failing operation; other operations may carry aborted status.

- Authentication failure requires corrected authentication, not a retry with weaker transport.
- Permission failure requires authorized access to the specific path.
- Invalid path, key or value requires correction against the model.
- Unsupported encoding requires an advertised supported encoding.
- A failed transaction is not reported as partly applied merely because some operations preceded the failure.

## Patterns

Atomicity is scoped to one configuration request, not a series of requests. A deletion with no existing target can succeed without changing anything. Protocol transaction success confirms acceptance; it does not certify application reachability or a wider operational objective.

## Known limitations

The protocol does not define business rollback policy, a common post-change health threshold, or a safe interval before retrying a lost response. A transport interruption that leaves the result unknown requires platform-specific state inspection before another mutation. Target conformance and actual schema constraints remain platform-specific.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover support | Obtain target model and encoding support | gNMI RPC |
| Apply configuration transaction | Submit the reviewed operations atomically | gNMI mutation RPC |

## Verification checklist

- The approved payload uses valid paths, keys and value types.
- The operator confirmed the live change and replacement/deletion scope.
- The RPC and all ordered operation results were examined.
- Unknown transport outcomes and failed transactions are reported explicitly.
