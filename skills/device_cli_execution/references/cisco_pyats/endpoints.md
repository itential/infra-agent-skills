# Cisco Unicon — Python Transport Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Connections](https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html).
- [Common Services](https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/services/generic_services.html).

## Connect session

```python
from pyats.topology import loader
testbed = loader.load('testbed.yaml')
device = testbed.devices['dut']
device.connect(via='cli', init_exec_commands=[], init_config_commands=[])
```

The empty initialization lists override plugin initialization commands where supported. They
are not universal permission or availability guarantees. A testbed connection's arguments can
also supply initialization settings; the effective connection definition must be reviewed.

## Execute command / Execute verification command

```python
output = device.execute(command, timeout=timeout_seconds)
```

`command` and `timeout_seconds` are inputs. `reply` accepts a `unicon.eal.dialogs.Dialog` containing
`Statement` objects with the platform's exact `pattern`, `action`, `loop_continue`, and
`continue_timer` settings. This reference supplies no universal confirmation regex.
`error_pattern` replaces the error patterns; `append_error_pattern` adds patterns.
`allow_state_change` defaults to false and controls whether a different valid end state is accepted.

## Configure device

After the procedure's confirmation gate:

```python
output = device.configure(configuration_lines, timeout=timeout_seconds)
```

`configuration_lines` is the approved configuration input, not a generic generated template.
`reply` supplies any documented configuration dialog. Platform save/commit bindings must come
from that platform's documentation; they are not inferred here.

## Disconnect session

```python
device.disconnect()
```

## Error names

`SubCommandFailure` is a service failure; an `EOF` cause identifies connection loss.
`StateMachineError` identifies an unexpected state transition. The original error and relevant
output remain part of the result; there is no automatic rollback in this binding.
