# Jenkins MCP bindings

Sources: [README](https://github.com/jenkinsci/mcp-server-plugin/blob/main/README.md), [core tools](https://github.com/jenkinsci/mcp-server-plugin/blob/main/src/main/java/io/jenkins/plugins/mcp/server/extensions/DefaultMcpServer.java), [log tools](https://github.com/jenkinsci/mcp-server-plugin/blob/main/src/main/java/io/jenkins/plugins/mcp/server/extensions/BuildLogsExtension.java), [SCM tools](https://github.com/jenkinsci/mcp-server-plugin/blob/main/src/main/java/io/jenkins/plugins/mcp/server/extensions/JobScmExtension.java), retrieved 2026-10-09. The configured authenticated plugin connection supplies transport. The deployed `tools/list` schema identifies optional version-specific fields.

| Operation | Tool and inputs |
|---|---|
| Identity / Status | `whoAmI()`, `getStatus()` |
| Jobs | `getJobs(parentFullName?, skip?, limit?)`; current limit at most 10 |
| Job detail | `getJob(jobFullName)`; optional exported-model `tree` projection |
| Trigger | `triggerBuild(jobFullName, parameters?)`; parameters is an object keyed by parameter name |
| Queue | `getQueueItem(id)` |
| Build | `getBuild(jobFullName, buildNumber?)`; explicit number for correlation |
| Metadata | `updateBuild(jobFullName, buildNumber?, displayName?, description?)`; boolean result |
| Log lines | `getBuildLog(jobFullName, buildNumber?, skip?, limit?, cursor?)`; `nextCursor`, `hasMoreContent`, `totalLines` |
| Log search | `searchBuildLog(jobFullName, buildNumber?, pattern, ...)`; optional matching/limits from deployed schema |
| Job SCM | `getJobScm(jobFullName)` |
| Build SCM / Changes | `getBuildScm(jobFullName, buildNumber?)`, `getBuildChangeSets(jobFullName, buildNumber?)` |
| Repository jobs | `findJobsWithScmUrl(scmUrl, branch?, ...)`; remaining paging inputs from deployed schema |

Current compact build fields include `number`, `url`, `result`, `building`, `timestamp`, `duration`, `displayName`, `description`. An explicit `tree` replaces the compact selection; `tree="*"` disables pruning and can return large or sensitive data. Invalid cross-build cursors are rejected. No exhaustive stable error-code table is published for every plugin tool; native permission/validation errors and null results remain distinguishable.
