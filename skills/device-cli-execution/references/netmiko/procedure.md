# Netmiko operational CLI execution

Run an explicitly supplied operational command through the matching Netmiko driver.

## Common Sequences

- Read command: **Select connection** → **Open session** → **Execute read** → **Close session**.

### Select connection

The request supplies a supported device type, target, authentication method and an operational CLI payload documented for that device. This procedure covers read commands only. Netmiko does not supply NetClaw's ownership routing or command allowlist. A command's spelling alone is not evidence of read-only behavior.

### Open session

The selected driver establishes the connection and prepares its session. Netmiko accepts unknown SSH host keys by default; that insecure default is explicitly not a verification result. The binding enables strict checking against pre-provisioned known hosts. An unknown/changed key ends connection pending independent identity verification, without disabling checking. Authentication failure and connection timeout remain distinct failures. If driver initialization changes live settings: stop and confirm with the operator before proceeding.

### Execute read

The command operation waits for the expected prompt/pattern and returns text with the command echo/prompt handling selected in the binding. Output is evidence, not a success verdict for the command's purpose. A read timeout means the expected completion pattern was not observed; partial output does not prove completion. Platform error text remains a failed command even if transport returned normally. Expected platform state must come from the supplied command procedure.

### Close session

The connection is disconnected after completion or failure. Context-manager use performs this cleanup automatically. The result retains device, payload and output or failure, with cleanup errors separate.

## Patterns

Prompt-based and timing-based reads have different completion rules. This procedure uses prompt-based reads; it does not automatically answer arbitrary prompts.

## Known limitations

No configuration, file transfer, reload, shell composition or automatic device detection is included. Parser support and device-command semantics are separate from transport support.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Device session | Establish a trusted session and transport the supplied CLI payload | SSH/device transport |

## Verification checklist

- Device driver and operational payload match.
- Host identity is verified with strict checking.
- Command-specific output and transport errors are separate.
- Session cleanup completes.

## Sources

- [Netmiko publisher API reference](https://ktbyers.github.io/netmiko/docs/netmiko/). Retrieved 2026-10-09.
- [Netmiko context-manager and command examples](https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md). Retrieved 2026-10-09.
