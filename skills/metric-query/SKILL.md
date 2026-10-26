---
name: metric-query
description: Read historical or current metric samples (time series) for a resource from a monitoring platform, for troubleshooting or before/after comparison. Use when you need observed numbers for a known metric over a time window. Covers Prometheus, Zabbix, Datadog, Amazon CloudWatch, and Google Cloud Monitoring. Read-only. Assumes an authenticated API client for the chosen platform is already available. Not for creating monitors or acknowledging alerts (see alert-monitor-management).
argument-hint: "[platform] [metric or item] [start] [end]"
---

# Metric Query

Reads time-series samples for a named metric or monitored item over a bounded window from a monitoring platform, and reports them together with the scope and completeness of what came back.

## When to use this skill

- Fetching observed values (utilisation, error counters, latency) for a known metric and interval to support troubleshooting or to compare against an earlier window.
- Checking whether a platform returned partial, truncated, or empty data for a query before drawing conclusions.
- Not for creating monitors, thresholds or alert rules, or acknowledging alerts: see `alert-monitor-management`. Not for dashboards or log searches.

## Universal concepts

This capability has no wire-level standard behind it; each platform defines its own query model. Where documented, the following hold on every platform listed:

- A query names a series (metric or item, plus any label/dimension selection) and a time window.
- Results carry timestamps and values, or aggregates over a period, and their meaning depends on the platform's own aggregation, resolution, and units.
- A result can be bounded, paginated, or aggregated by the platform; a bounded or aggregated result is not the full raw record.
- An empty result or an error does not show that a resource is healthy, idle, or unmonitored.

## Procedure

1. Identify the platform from the request and find it in `references/INDEX.md`. If it is not listed, stop: this skill does not cover it.
2. Open that platform's `procedure.md` and follow it exactly.
3. Report the outcome using that procedure's own status vocabulary, with the query scope, window, and any warnings or incompleteness.

## Known limitations

- Read-only: no monitor, alert, retention, or collection changes, and no thresholds or diagnoses are produced.
- The caller supplies the metric identity; discovery is covered only where a platform procedure includes it.

## Contributing to this skill

This router changes only to correct shared concepts or to add a pointer to a newly supported platform. Platform detail belongs under `references/<platform>/`.

## Tools

An authenticated API client for the selected platform. Each platform's `procedure.md` names its operations and `endpoints.md` binds them.

## Verification checklist

- The platform, metric, and window in the result match the request.
- Warnings, truncation, pagination state, and platform status values are carried into the report.
- No health conclusion is drawn from an empty or failed read.
