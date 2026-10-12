# Cisco pyATS — Health Processor Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Health Check Usage](https://pubhub.devnetcloud.com/media/genie-docs/docs/health/health_usage/usage.html).

## health.yaml

Original CPU example using the documented criterion form. `90` illustrates Cisco's documented
example/default criterion; it is not a recommended universal operational threshold. A different
requested criterion belongs in the corresponding expression, not a nonexistent CPU threshold argument.

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
| `health_crashinfo` argument `copy_files` | Defaults true; copies newly detected crashinfo to the run directory |
| `health_crashinfo` argument `delete_files` | Defaults false; true requests deletion, including the documented no-copy case |

Processor result overrides such as `failed_result_status: passx` alter reporting. They do not make
an existing crash disappear; any override remains visible when reporting observed evidence.
