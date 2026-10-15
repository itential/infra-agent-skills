# Endpoints — Amazon EC2 instance lifecycle (Query API)

Literal wiring layer for `procedure.md`. Operation names in its Tools table map to the actions below.

Written against the Amazon EC2 API reference, API version 2016-11-15, checked 2026-10-14. Parameter
names are as the reference spells them; list parameters take an index suffix (`InstanceId.1`,
`InstanceId.2`, and so on, shown as `.N`). Values are placeholders.

## Request form and authentication

Calls are plain HTTP(S) requests, by GET or POST, carrying a parameter `Action` that names the operation, plus `Version=2016-11-15`, the action's parameters, and authentication parameters. Either
verb carries the same data. Signature Version 4 is recommended (Signature Version 2 is also supported).
Credentials, signing, and the choice of regional endpoint are normally handled by an SDK or CLI client;
the reference's examples use `ec2.amazonaws.com`, and the per-Region endpoint list was not read for
this file (assumption: use the Region's own endpoint for the instance being managed). Optional common
parameters: `DryRun` and `SecurityToken` (for temporary credentials).

`DryRun=true` returns `DryRunOperation` if the caller has the permissions and the call would succeed,
or `UnauthorizedOperation` if not; nothing is changed either way.

Writes return before the work completes. The API follows an eventual consistency model, so a read
shortly after a write can lag or report `InvalidInstanceID.NotFound`. Throttling by request rate or resource rate returns `RequestLimitExceeded`; retry with exponential backoff.

## describe_instances

```
Action=DescribeInstances
```
Parameters: `InstanceId.N` (specific instances) and `Filter.N` (`Name`, `Value.N`). Documented filter
for state: `instance-state-name` with values `pending`, `running`, `shutting-down`, `terminated`,
`stopping`, `stopped`. Tag filters use the name `tag:<key>`.
The instance's current network bandwidth weighting is read with the `network-performance-options.bandwidth-weighting` filter or in the returned instance data (assumption: also returned as a field). Without identifiers or filters every
instance in the Region is returned; page with `MaxResults` and `NextToken`. An invalid identifier
returns an error; instances you do not own are omitted; terminated instances can remain visible for
under an hour.

## describe_instance_status

```
Action=DescribeInstanceStatus
```
Parameters: `InstanceId.N` (up to 100), `Filter.N`, `IncludeAllInstances` (by default only running
instances are described). Documented values: `instance-status.status` and `system-status.status` of
`ok`, `impaired`, `initializing`, `insufficient-data`, `not-applicable`; `instance-status.reachability`
of `passed`, `failed`, `initializing`, `insufficient-data`.

## describe_subnets / describe_security_groups / describe_vpcs

```
Action=DescribeSubnets          Filter: subnet-id, vpc-id, availability-zone, state (pending | available),
                                available-ip-address-count, default-for-az
Action=DescribeSecurityGroups   Filter: group-id, group-name, vpc-id
Action=DescribeVpcs             Filter: vpc-id, state (pending | available), is-default
```
Each accepts specific identifiers (`SubnetId.N`, `GroupId.N`, `VpcId.N`) or filters; with neither, all of
the account's objects in the Region are returned. A security group is tied to the network it was created
in, so compare its `vpc-id` with the chosen subnet's `vpc-id`. A group referenced through a peering
connection may sit in another network, but that case is for rules, not for launching.

## describe_images / describe_instance_type_offerings / describe_instance_types

```
Action=DescribeImages                 Filter: image-id, state (available | pending | failed), architecture
Action=DescribeInstanceTypeOfferings  LocationType, Filter: location, instance-type
Action=DescribeInstanceTypes          Filter: processor-info.supported-architecture, network-info.bandwidth-weightings (whether a type supports
                                      bandwidth weighting), and others
```
`DescribeInstanceTypeOfferings` lists the types offered in a location; with no location it uses the
current Region. `LocationType` takes `availability-zone`, `availability-zone-id`, or `outpost`; when a
`location` filter is given it must be a value of that type for the current Region, so pass
`LocationType=availability-zone` with `location=<zone name>` to check one zone.

## run_instances

```
Action=RunInstances
```
| Parameter | Required | Notes |
|---|---|---|
| `MinCount`, `MaxCount` | Yes | Between 1 and the account's quota for the instance type. If the minimum cannot be met, nothing launches |
| `ImageId` | Yes, here or in a launch template | |
| `InstanceType` | Required unless a launch template supplies it | Assumption: required in the same way as `ImageId`; the reference does not mark it |
| `LaunchTemplate` | No | Can replace most launch parameters |
| `SubnetId`, `SecurityGroupId.N` | No | Defaults to a subnet in the default VPC and the default security group |
| `KeyName`, `IamInstanceProfile`, `UserData` | No | `UserData` must be base64-encoded |
| `TagSpecification.N` | No | Tags for instances, volumes, Spot requests, network interfaces at launch |
| `ClientToken` | No | Up to 64 ASCII characters; same token and parameters retried succeeds without a second launch; a different parameter set fails with `IdempotentParameterMismatch` |
| `DisableApiTermination`, `DisableApiStop` | No | Termination and stop protection |
| `InstanceInitiatedShutdownBehavior` | No | `stop` (default) or `terminate` |
| `DryRun` | No | See above |

Response: `reservationId`, `ownerId`, and `instancesSet`. The instance is ready at `running`. Launch
large requests in smaller batches; both request-rate and resource-rate limits apply.

## stop_instances

```
Action=StopInstances
```
Parameters: `InstanceId.N` (required), `Hibernate` (only for hibernation-enabled instances; if it
fails, a normal shutdown occurs), `Force` (for an instance stuck in stopping), `SkipOsShutdown` (skips
the graceful shutdown; may risk data integrity), `DryRun`. EBS-backed instances only.

## start_instances

```
Action=StartInstances
```
Parameters: `InstanceId.N` (required), `DryRun`. EBS-backed instances only; instance-store-backed
instances return an error. A start fails for a T3 instance that has host tenancy and the unlimited CPU credit option
until the credit option is set to standard or the tenancy is changed.

## reboot_instances

```
Action=RebootInstances
```
Parameters: `InstanceId.N` (required), `DryRun`. Asynchronous; only queues the reboot.

## modify_instance_attribute

```
Action=ModifyInstanceAttribute
```
One attribute per call. Parameters: `InstanceId`, and one of `Attribute` with `Value`, or the matching
typed parameter. Documented `Attribute` values include `instanceType`, `disableApiTermination`,
`disableApiStop`, `instanceInitiatedShutdownBehavior`, `userData`, `sourceDestCheck`, `groupSet`, and
`blockDeviceMapping` (for volume delete-on-termination). The instance must be stopped to change some
attributes, including the instance type. An invalid type returns `InvalidInstanceAttributeValue`.
Termination protection cannot be enabled for Spot instances.

## modify_instance_network_performance_options

```
Action=ModifyInstanceNetworkPerformanceOptions
```
Parameters: `InstanceId` (required), `BandwidthWeighting` (required: `default`, `vpc-1`, or `ebs-1`), `DryRun`.
`default` is the standard bandwidth configuration for the type; `vpc-1` boosts network baseline bandwidth
at the cost of EBS baseline bandwidth, and `ebs-1` the reverse. Used here only to set `default` before a
type change when the target type does not support configurable bandwidth.

## create_snapshots

```
Action=CreateSnapshots
```
Parameters: `InstanceSpecification` (required: instance identifier, plus options to exclude the root
volume or specific data volumes), `Description`, `CopyTagsFromSource=volume`, `TagSpecification.N`,
`DryRun`. Produces one crash-consistent snapshot per included volume, consistent across the instance.

## create_image

```
Action=CreateImage
```
Parameters: `InstanceId` (required), `Name` (required; 3 to 128 characters from a documented set),
`NoReboot` (default `false`: the instance is rebooted first; `true`: no reboot, crash-consistent),
`Description`, `BlockDeviceMapping.N` (volume size cannot be changed here), `TagSpecification.N`,
`DryRun`. EBS-backed instances only, running or stopped.

## describe_snapshots

```
Action=DescribeSnapshots     Filter: status (pending | completed | error), snapshot-id, start-time, tag:<key>
```

(`describe_images` is defined above.)

## describe_instance_attribute

```
Action=DescribeInstanceAttribute
```
Parameters: `InstanceId` (required), `Attribute` (required; one per call). Documented values include
`instanceType`, `userData`, `disableApiTermination`, `instanceInitiatedShutdownBehavior`,
`rootDeviceName`, `blockDeviceMapping`, `sourceDestCheck`, `groupSet`, `ebsOptimized`, `disableApiStop`
(one value per call: use `disableApiTermination` for termination protection and `disableApiStop` for stop
protection). The response
carries `disableApiStop` (stop protection) and `disableApiTermination` (termination protection) as
boolean attribute values. `DescribeInstances` does not return these two settings; it does return each
volume's `deleteOnTermination` in the block device mapping, and filters on
`block-device-mapping.delete-on-termination`.

## terminate_instances

```
Action=TerminateInstances
```
Parameters: `InstanceId.N` (required, up to 1000; smaller batches recommended), `Force`,
`SkipOsShutdown`, `DryRun`. Idempotent. Permanent and irreversible. A single invalid identifier fails the
whole request; termination protection on one instance blocks the others in its Availability Zone.

## create_tags

```
Action=CreateTags
```
Parameters: `ResourceId.N`, `Tag.N` (`Key`, `Value`), `DryRun`.

## Error handling

Report FAILED with the error code and message. Codes referenced above: `IncorrectInstanceState` (for example a start of a non-stopped instance, or a
modification that needs the instance stopped), `OperationNotPermitted` (for example terminating an
instance with termination protection), `InvalidSubnetID.NotFound`, `InvalidSubnetID.Malformed`, `InvalidGroup.NotFound`,
`InvalidGroupId.Malformed`, `InvalidVpcID.NotFound`, `VPCIdNotSpecified`, `InvalidAMIID.NotFound`,
`InvalidAMIID.Unavailable`, `InvalidKeyPair.NotFound`, `InvalidInstanceType`, `InvalidParameter` (including
a security group and subnet in different networks), `InsufficientInstanceCapacity`, `DryRunOperation`,
`UnauthorizedOperation`, `IdempotentParameterMismatch`, `InvalidInstanceAttributeValue`,
`InvalidInstanceID.NotFound`, `RequestLimitExceeded`.
