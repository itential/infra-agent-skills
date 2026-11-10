# AWS EC2 Security Groups — Audit Bindings

Operation names and documented parameters for the read operations the procedure uses. Source: AWS CLI EC2 reference (retrieved 2026-11-10). All operations are EC2 API reads; the AWS CLI names are the `aws ec2` subcommands shown. Region is chosen per call.

## List security groups

CLI: `describe-security-groups`. Paged (`NextToken`); keep paging until it is empty.
- Filters: `group-id`, `group-name`, `vpc-id`, `description`, `owner-id`, `tag:<key>`, `tag-key`, plus rule filters such as `ip-permission.cidr`, `ip-permission.from-port`, `ip-permission.to-port`, `ip-permission.protocol`, `ip-permission.group-id`. Several rule filters match a group whose rules together satisfy them, not necessarily one rule.
- Output per group: `GroupId`, `GroupName`, `Description`, `VpcId`, `OwnerId`, `Tags`, `IpPermissions` (inbound), `IpPermissionsEgress` (outbound). Each permission has `IpProtocol`, `FromPort`, `ToPort`, `IpRanges[].CidrIp`, `Ipv6Ranges[].CidrIpv6`, `PrefixListIds`, `UserIdGroupPairs` (with `GroupId`, `VpcId`, `VpcPeeringConnectionId`, `PeeringStatus`), and a `Description` on each entry.
- CIDRs come back canonicalized (host bits zeroed).

## List security group rules

CLI: `describe-security-group-rules`. Paged.
- Filters: `group-id`, `security-group-rule-id`, `tag:<key>`.
- Output per rule: `SecurityGroupRuleId`, `GroupId`, `IsEgress`, `IpProtocol`, `FromPort`, `ToPort`, `CidrIpv4`, `CidrIpv6`, `PrefixListId`, `ReferencedGroupInfo` (`GroupId`, `PeeringStatus`, `UserId`, `VpcId`, `VpcPeeringConnectionId`), `Description`, `Tags`.

## List network interfaces

CLI: `describe-network-interfaces`. Paged; the reference states the call can fail on large accounts unless paged or filtered by `group-id`, `mac-address`, `private-dns-name`, `private-ip-address`, `subnet-id`, or `vpc-id`.
- Option `--include-managed-resources` includes interfaces managed by AWS services that are hidden by default.
- Filters: `group-id` (a group on the interface), `vpc-id`, `subnet-id`, `status`, `interface-type`, `requester-managed`, `attachment.instance-id`, `tag:<key>`.
- Output per interface: `NetworkInterfaceId`, `Status` (`available`, `associated`, `attaching`, `in-use`, `detaching`), `InterfaceType`, `Groups[]` (`GroupId`, `GroupName`), `Attachment.InstanceId`, `VpcId`, `SubnetId`, `RequesterManaged`, `Operator`.

## List security group VPC associations

CLI: `describe-security-group-vpc-associations`. Documented to report each association's state (for example `associated`). Parameters and output fields: unverified; consult the reference before use.
