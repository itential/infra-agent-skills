# Cisco pyATS Clean — Definition Schema

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Cleaning Devices](https://pubhub.devnetcloud.com/media/genie-docs/docs/clean/user_guide/writing_a_clean/cleaning_devices.html).

## Connection-only schema illustration

```yaml
cleaners:
  PyatsDeviceClean:
    module: genie.libs.clean
    devices: [dut]
devices:
  dut:
    connect:
    order:
      - connect
```

`dut` must be a device in the supplied testbed. This illustration does not reset a device.
An actual Clean requires the selected platform's stage mappings and arguments, referenced in
`order` in the documented sequence. The procedure's confirmation gate applies before execution,
including any connection initialization changes.
