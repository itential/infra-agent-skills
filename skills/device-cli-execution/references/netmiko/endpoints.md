# Netmiko operational CLI execution: bindings

Python bindings (Netmiko 4 reference):

`from netmiko import ConnectHandler`

`with ConnectHandler(device_type=device_type, host=target, username=username, password=password, ssh_strict=True, system_host_keys=True) as session:`

Inside the context: `output = session.send_command(command_string=approved_read_command, expect_string=expected_prompt_pattern, read_timeout=selected_seconds, strip_prompt=True, strip_command=True)`.

Outside a context manager, `session.disconnect()` closes the session. The selected prompt and timeout are operator/platform inputs, not universal constants. Error types include `NetmikoAuthenticationException`, `NetmikoTimeoutException` and `ReadTimeout`. No automatic trust enrollment or retry is bound here.

## Sources

- [Netmiko publisher API reference](https://ktbyers.github.io/netmiko/docs/netmiko/). Retrieved 2026-10-09.
- [Netmiko context-manager and command examples](https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md). Retrieved 2026-10-09.
