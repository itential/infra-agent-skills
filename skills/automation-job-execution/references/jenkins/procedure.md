# Jenkins existing-job execution

The Jenkins MCP Server Plugin reads a selected job, schedules its build and follows the resulting queue item and build.

Sources: [publisher README](https://github.com/jenkinsci/mcp-server-plugin/blob/main/README.md), [core tool implementation](https://github.com/jenkinsci/mcp-server-plugin/blob/main/src/main/java/io/jenkins/plugins/mcp/server/extensions/DefaultMcpServer.java), [log tools](https://github.com/jenkinsci/mcp-server-plugin/blob/main/src/main/java/io/jenkins/plugins/mcp/server/extensions/BuildLogsExtension.java), and [SCM tools](https://github.com/jenkinsci/mcp-server-plugin/blob/main/src/main/java/io/jenkins/plugins/mcp/server/extensions/JobScmExtension.java), current main, retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Run existing job: Inspect connection → Find job → Inspect job inputs → Trigger build → Follow queue → Read build → Read/search logs.
- Inspect execution: Find job → Read build → Read/search logs → Read SCM evidence.
- Update display metadata: Read build → Change display metadata → Read build.

## Inspect connection

Identity inspection returns the authenticated user; status inspection returns platform health/readiness information. Success is the native result, including any root-URL configuration problem. Permission failures are reported against the configured identity. This does not reconfigure Jenkins or bypass its authorization.

## Find job

The job collection is sorted by name and paged within the selected folder. The current implementation limits each page to ten entries. Its pagination uses an offset, not the source wrapper's regex filter. A full job path identifies nested jobs. An empty page is valid, but an invalid parent can also yield an empty list; a known parent is verified before interpreting it as an empty folder.

## Inspect job inputs

A job read returns the requested job or no object. The compact default result does not include every parameter definition; an explicit field selection obtains the definition and required values. Success identifies the intended job, its buildability and its parameter contract. File parameters are not supported by this MCP path. The publisher warns that unsupported parameter types can fall back to defaults; required values are verified against the resulting build parameters rather than assumed accepted.

## Trigger build

Before scheduling, **stop and confirm with the operator before proceeding**, including the job, target systems and selected parameter values. Success returns a queue item identifying the scheduled execution; it is not build success. A null result is not confirmation of scheduling. Permission or parameter errors remain failed requests. An ambiguous timeout requires queue/build inspection before any replay, because the request may already have scheduled work.

## Follow queue

The returned queue identifier is used to obtain its current record and eventual executable build identity. Success when started is the associated build identity; a queued item remains queued. A null queue response can mean the record is unavailable or not visible and does not prove a completed build. The subsequent build read uses the confirmed number, avoiding an unrelated later build.

## Read build

The build read returns the selected build's number, result, building flag, timestamps and duration. While building is true or a final result is absent, completion is not established. Once complete, the native result is reported unchanged. A missing result object is not a successful build. Explicit field selection obtains parameters or additional evidence omitted by compact defaults.

## Read/search logs

Log reads return lines and continuation metadata. The next cursor is reused only with its originating job/build. A cursor plus no more currently available content can mean a running build has written nothing further yet; the cursor remains useful later. Forward/cursor reads may report total lines as unknown. Search reads return matches up to their limit, not a guaranteed complete log. Invalid cursors or patterns are corrected from the native error. Returned console content may contain sensitive values and is limited to the requested evidence.

## Read SCM evidence

Job SCM configuration, build SCM revision information, build change sets and repository-based job discovery are separate reads. Success retains which evidence belongs to the job configuration versus the specific build. Missing SCM data remains missing rather than inventing a revision or cause.

## Change display metadata

Before changing a build's display name or description, **stop and confirm with the operator before proceeding** with the exact build number and new values. The update returns a boolean; true indicates a metadata update and a subsequent build read verifies the values. False is not a successful change. This operation does not support the older source's keep-forever option.

## Patterns

The current plugin uses object-shaped parameters, line/cursor log paging and explicit full job names. A latest-build default is convenient for inspection but insufficient to correlate a specific triggered execution under concurrent builds.

## Known limitations

The two source pipeline-history/log wrapper methods are not in the current publisher's built-in tool list and are unconverted. Rebuild, replay and script mutation are outside scope. Job side effects depend on its definition; this skill does not claim transactional rollback.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Connection/job/build/queue inspection | Resolve execution identity and status | Read |
| Trigger build | Schedule an existing job | Write |
| Log and SCM reads | Retrieve execution evidence | Read |
| Change display metadata | Update build label/description | Write |

## Verification checklist

- Job identity and parameter definitions are known before scheduling.
- The returned queue is correlated to the specific build.
- Final native result is preserved; acceptance is not completion.
- Logs retain paging/truncation state and metadata updates are read back.
