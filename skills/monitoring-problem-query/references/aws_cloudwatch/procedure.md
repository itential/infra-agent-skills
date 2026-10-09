# CloudWatch alarm and history query

Retrieve alarm states and their recorded history without changing alarm configuration or actions.

Sources: AWS current [alarm query](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_DescribeAlarms.html) and [alarm history](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_DescribeAlarmHistory.html), retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Current alarms: Read alarm states → Continue pages → Report.
- State history: Read alarm states → Read alarm history → Continue pages → Report.

## Read alarm states

The account/region, names or name prefix, alarm types and optional state filter select the result. Types are explicit when composite or log alarms are required; omission returns metric alarms only. Results retain `OK`, `ALARM`, or `INSUFFICIENT_DATA`. Composite-alarm reads require the documented permission scope; inaccessible composites cannot be interpreted as absent.

## Read alarm history

The requested alarm/type, interval and event category select history. History can remain available after the alarm is deleted. State-change events are distinct from configuration changes or action events. A successful history read is evidence of recorded events, not an assertion that an associated remediation succeeded.

## Continue pages

Each continuation token is supplied with the original selection until no token remains. Invalid-token errors require a fresh read sequence; a failed continuation leaves the result incomplete. Authentication, permission, and other AWS errors remain failures with their native diagnostics rather than empty alarm lists.

## Report

The result retains account/region, query filters, alarm types and native states or history categories. An alarm in insufficient-data state is not normalized to healthy. A currently empty `ALARM` query does not prove no earlier alarm occurred.

## Patterns

Composite relationships and ordinary alarm reads differ: this scope reads states/history, not parent/child traversal. The source reference contains an inconsistent plural spelling in its alarm-type prose; the binding follows the schema's singular enum values.

## Known limitations

No alarm acknowledgement, state override, action execution, creation, or deletion occurs. Publisher rate/retention values not present in these two references are not assumed.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read alarm states | Retrieves selected alarm definitions and states | Read |
| Read alarm history | Retrieves recorded state/configuration/action events | Read |

## Verification checklist

- Alarm type selection includes the requested families.
- Pagination and access limitations are preserved.
- Native alarm state and event category remain distinct.
