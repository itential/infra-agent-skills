# Infrastructure Plan Execution — Vendor Index

One row per supported platform. Each directory holds a `procedure.md`. CLI commands stay inline, so there is no `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| HashiCorp Terraform CLI | `terraform/` | Init; format check; validate; plan and destroy plan; apply a saved plan; list state; read outputs; import one resource | A single implementation exists today. Applying a saved plan does not prompt, so the operator gate sits before apply. Output reads can reveal sensitive values. |

**Not in scope:** authoring configuration, provider-specific resource behavior, tool installation, backend setup.
