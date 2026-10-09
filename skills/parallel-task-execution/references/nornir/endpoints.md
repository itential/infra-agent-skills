# Nornir scoped task execution: bindings

Native Python bindings, Nornir 3.6.0:

- `nr = InitNornir(config_file=config_path, runner={"plugin": "threaded", "options": {"num_workers": selected_workers}})` from `nornir`.
- `selected = nr.filter(**inventory_filters)`; selected identities are `selected.inventory.hosts`.
- `results = selected.run(task=approved_read_task, **task_arguments)`.
- Inspect `results.failed`, `results.failed_hosts`; each `results[host]` is a `MultiResult`, with `Result.result`, `failed`, `changed`, `exception`.
- `results.raise_on_error()` raises `NornirExecutionError` if needed.
- Existing skipped state: `nr.data.failed_hosts`. Explicit reruns use `on_failed=True`; `on_good=False` limits that rerun to failed hosts. `recover_host`/`reset_failed_hosts` change eligibility only and are not invoked automatically.

Task transport/plugins are supplied by the caller and must be independently verified. No invented Netmiko/NAPALM plugin name is required by this generic executor.

## Sources

- [Nornir initialization](https://nornir.readthedocs.io/en/latest/tutorial/initializing_nornir.html). Retrieved 2026-10-09.
- [Nornir result structure](https://nornir.readthedocs.io/en/latest/tutorial/task_results.html). Retrieved 2026-10-09.
- [Nornir failure and skipped-host handling](https://nornir.readthedocs.io/en/latest/tutorial/failed_tasks.html). Retrieved 2026-10-09.
