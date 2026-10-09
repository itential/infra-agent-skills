# CloudWatch alarm bindings

Sources: [DescribeAlarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_DescribeAlarms.html), [DescribeAlarmHistory](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_DescribeAlarmHistory.html), retrieved 2026-10-09.

Authorized AWS CloudWatch SDK client with account/region and request signing:

| Operation | SDK binding | Inputs and response |
|---|---|---|
| Read states | `DescribeAlarms` / Boto3 `describe_alarms` | `AlarmNames` or `AlarmNamePrefix` (mutually exclusive), `AlarmTypes`, optional `StateValue`, `NextToken`, `MaxRecords`; returns `MetricAlarms`, `CompositeAlarms`, `LogAlarms`, `NextToken` |
| Read history | `DescribeAlarmHistory` / Boto3 `describe_alarm_history` | `AlarmName`, `AlarmTypes`, `StartDate`, `EndDate`, `HistoryItemType`, `ScanBy`, `NextToken`, `MaxRecords`; returns `AlarmHistoryItems`, `NextToken` |

`AlarmTypes` enums are `MetricAlarm`, `CompositeAlarm`, `LogAlarm`. State enums: `OK`, `ALARM`, `INSUFFICIENT_DATA`. History categories: `ConfigurationUpdate`, `StateUpdate`, `Action`, `AlarmContributorStateUpdate`, `AlarmContributorAction`. `MaxRecords` is 1–100. Both APIs document `InvalidNextToken` (400). Composite reads require the respective describe permission scoped to `*`; a narrower policy does not return composites. No mutation binding is included.
