# Compute Instance Provisioning — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Amazon EC2 | `aws_ec2/` | Launch, read, start/stop/reboot, resize (change instance type), back up (volume snapshots or image), terminate | Only one platform is documented, so `SKILL.md`'s universal concepts are hedged. Instance lifecycle only; networks, security groups, volumes as their own objects, Auto Scaling, load balancers, and Spot/Reserved purchasing are out of scope. EC2 has no documented in-place revert to a snapshot |
