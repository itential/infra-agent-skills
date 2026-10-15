# Cisco pyATS — Health Processor Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Health Check Usage](https://pubhub.devnetcloud.com/media/genie-docs/docs/health/health_usage/usage.html).

## health.yaml

Adapted from the usage page's CPU example. `90` is the documented example criterion, not a
recommended threshold; a different criterion goes in the `include` expression.

```yaml
pyats_health_processors:
  source:
    pkg: genie.libs.health
    class: health.Health
  test_sections:
    - selected_cpu:
        - api:
            device: dut
            function: health_cpu
            include:
              - sum_value_operator('value', '<', 90)
```

## Mutating options requiring the procedure's gate

| Binding | Effect |
|---|---|
| `--health-clear-logging` | Clears device logs before checks |
| `--health-remote-device` | Core files are copied to a remote server (documented option) |
| `health_crashinfo` argument `copy_files` | Defaults true; copies newly detected crashinfo to the run directory |
| `health_crashinfo` argument `delete_files` | Defaults false; true requests deletion, including the documented no-copy case |

A result override such as `failed_result_status: passx` changes reporting only; report it alongside the evidence.
