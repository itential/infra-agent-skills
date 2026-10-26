---
name: log-query
description: Retrieve stored log events from a log platform for a stated store, filter, and time window, and report what was and was not covered. Use when troubleshooting or verifying a change requires reading retained logs. Covers Splunk, Datadog Logs, Elasticsearch, Grafana Loki, AWS CloudWatch Logs, and Google Cloud Logging. Read-only. Assumes an authenticated API client for the selected platform is already available; the caller supplies the search expression, which this skill does not write for them.
argument-hint: "[platform] [store/index/log group] [time window] [search expression]"
---

# Log Query

Reads retained log events from one supported log platform, using that platform's documented search and paging sequence, and reports the scope and completeness of what came back.

## When to use this skill

- Retained log events must be read from Splunk, Datadog Logs, Elasticsearch, Grafana Loki, AWS CloudWatch Logs, or Google Cloud Logging as evidence while troubleshooting or checking a change.
- Not for ingesting logs, changing retention, saving searches or alerts (alert creation is `alert-monitor-management`), or reading numeric time series.

## Universal concepts

- No wire-level standard covers log search; each platform defines its own query language, time handling, and paging.
- Every result is evidence only within the store, filter, time window, and result bound that produced it.
- An empty result, a bounded page, a timed-out search, or a failed shard or partition is not proof that nothing matched.
- Where a platform paginates or runs searches asynchronously, the result is complete only when its own documented completion signal says so.
- Log lines can carry secrets or personal data; handle returned content as sensitive.
- The skill is read-only: it never changes data, so it has no confirmation gates. Any step that would write (saving results over an existing local file, running a search that writes data) needs operator confirmation first.

## Procedure

1. Identify the platform from the request or the `platform` argument. If it is not listed in [references/INDEX.md](references/INDEX.md), stop and report that it is unsupported.
2. Open that platform's `references/<platform>/procedure.md` and follow it exactly.
3. Report the outcome in that procedure's own status vocabulary, together with the scope and completeness details it names.

## Known limitations

Only the platforms in the index are covered. Writing search expressions beyond the caller's request, exporting to files, and inferring root cause from matches are out of scope.

## Contributing to this skill

Change this router only to correct shared concepts or routing, or to add a pointer to a newly supported platform. Platform detail belongs under `references/<platform>/`.

## Tools

An authenticated API client for the selected platform. Each procedure's `endpoints.md` lists the exact calls to bind.

## Verification checklist

- [ ] The platform and scope match the request and an index entry.
- [ ] The platform's own completion signal was checked and reported.
- [ ] Empty, bounded, or failed results are reported as such, not as an absence of events.
