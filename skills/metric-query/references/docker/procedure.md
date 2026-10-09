# Docker container resource snapshot

Read a bounded Docker container statistics sample.

## 1. Select containers

The existing Docker CLI context identifies the daemon and requested container names/IDs. Daemon or permission failure is reported without changing access.

## 2. Read one sample

`docker stats --no-stream CONTAINER` retrieves one sample for the selected container. Additional selected names/IDs can be supplied as separate arguments. A stopped container does not return statistics; that is not zero resource use.

## 3. Interpret native fields

The result retains container identity and CPU, memory, network/block I/O and PID fields that the platform provides. Linux CLI memory subtracts cache, unlike the raw statistics API. PID counts include kernel threads. A sample does not establish sustained load or an application-health verdict.

## Patterns

The CLI and API memory values need not match because the CLI applies a cache adjustment.

## Known limitations

No fixed warning/critical threshold, streaming monitor or container resource change is included.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Docker CLI | Read container resource statistics | Metrics read |

## Verification checklist

- Context and container identity match.
- Missing/stopped-container data is not reported as zero.
- One sample is not described as sustained utilization.

## Sources

- [Docker statistics CLI reference](https://docs.docker.com/reference/cli/docker/container/stats/). Retrieved 2026-10-09.
