# CRM Contact Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Salesforce | `salesforce/` | Create/read/update/delete a Contact record via the generic REST `sobjects` resource | Only `LastName` is structurally required; org-layered validation rules can add more. Contact-only skill; account records are out of scope. |
