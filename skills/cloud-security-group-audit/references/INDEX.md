# Cloud Security Group Audit — Vendor Index

One row per supported cloud. Each directory holds a decision-list procedure (one section per check) and a bindings file for the read calls. All platforms are read-only: no rule is changed and no group is deleted.

| Vendor / Platform | Directory | Checks covered | Notes |
|---|---|---|---|
| AWS EC2 security groups | `aws-ec2-security-groups/` | Open to the internet (admin port, wide range, web port, other), all-protocol rules, unused groups, default-group use, redundant rules, hygiene | Per Region. Allow rules only, rules combine additively. Usage is read from network interfaces (include AWS-managed ones). Network ACLs and AWS Network Firewall are not read. |
| Azure network security groups | `azure-network-security-groups/` | Open to the internet (with deny-rule shadowing), unassociated NSGs, broad rules, shadowed and redundant rules, hygiene | Per subscription. Priority-ordered allow and deny rules; default rules are never findings. Virtual Network Manager security admin rules are evaluated first and are not read; effective exposure is not computed. |
| Google Cloud VPC firewall rules | `google-cloud-vpc-firewall/` | Open to the internet, broad rules, disabled and unused rules, shadowed rules, Firewall Insights findings | Per project. No attachment object: rules apply by network and target selector. Insights (shadowed, no-hit, overly permissive) need APIs, logging, and enabled features, and take up to 48 hours (10 days for predictions). Hierarchical and network firewall policies are not read. |

