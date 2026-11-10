# Google Cloud VPC Firewall Rules — Audit Bindings

Read operations used by the procedure. Source: `gcloud compute firewall-rules list` and `gcloud recommender insights list` references and the Firewall Insights documentation (retrieved 2026-11-10).

## List firewall rules

CLI: `gcloud compute firewall-rules list --project <project> --format=json`. Flags: `--filter`, `--limit`, `--sort-by`.
- Fields per rule: `name`, `network`, `direction` (`INGRESS`/`EGRESS`), `priority`, `sourceRanges`, `allowed`, `denied`, `targetTags`, `disabled`. Unverified: names of the destination-range, target-service-account, and logging-configuration fields; read them from the returned object.
- `gcloud compute firewall-rules describe <name>` returns one rule (used to re-read a rule before cross-checking an insight). Unverified: flags.

## List Firewall Insights

CLI: `gcloud recommender insights list --project <project> --location global --insight-type google.compute.firewall.Insight`. Optional `--filter`, `--limit`, `--page-size`, `--sort-by`, `--format`.
- Insight type ID: `google.compute.firewall.Insight`. Subtype values and output field names: unverified.
- Required role named in the documentation: `recommender.computeFirewallInsightViewer`.

## Read Firewall Insights configuration

API: the Firewall Insights configuration method (the documentation names `updateConfig` for changing it, with observation-period and feature settings). The read counterpart and its fields are unverified; if no read call can be bound, report that configuration state could not be read and rely on whether insights were returned.
