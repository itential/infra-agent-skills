# WAF Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Cloudflare WAF (zone) | `cloudflare-waf/` | Create, read, update, disable, and delete custom rules and rate limiting rules; deploy a managed ruleset with overrides | REST (Rulesets API). Zone level only; account-level rulesets, exceptions, bot management, and DDoS are not covered. Plan limits apply to rule counts, actions (`log` is Enterprise only), and rate limiting options. Cloudflare's network-layer firewall is a separate vendor under `firewall-management`. Only one platform is documented. |
