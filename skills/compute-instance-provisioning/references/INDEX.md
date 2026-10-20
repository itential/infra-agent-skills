# Compute Instance Provisioning — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| Amazon EC2 | `aws-ec2/` | Launch, read, start/stop/reboot, resize (change instance type), back up (volume snapshots or image), terminate | Instance lifecycle only; networks, security groups, volumes as their own objects, Auto Scaling, load balancers, and Spot/Reserved purchasing are out of scope. EC2 has no documented in-place revert to a snapshot |
| Google Compute Engine | `google-compute-engine/` | Create, read, stop/start, suspend/resume, resize (machine type, while stopped), snapshot of disks, delete | REST. Snapshots are of disks and restore into a new disk, with no in-place revert. Several routes are marked as assumptions in `endpoints.md`. Networks, disks as standalone objects, images, instance groups, and IAM are out of scope |
| VMware vSphere | `vmware-vsphere/` | Create, read, power on/off/reset/suspend, guest shutdown, resize (CPU and memory), delete | REST (vSphere Automation API on vCenter). The vendor portal pages were unreadable on the check date, so routes, errors, and rules come from the assets repo's copy of the API definition, a secondary source flagged in the files. No snapshot or revert operation was found. Clusters, datastores, networks, templates, and clones are out of scope |
| Morpheus | `morpheus/` | Create, read, stop/start, resize, snapshot, delete | REST. A management layer over other clouds, so create takes cloud-specific config the file does not carry. No revert, restart, or status vocabulary was reviewed. Clouds, groups, layouts, plans, networks, and policies are out of scope |

### Corrections to the universal concepts

Adding these three platforms contradicted no claim outright, but two were too narrow and now say more:
resize may be possible while running on some platforms (vSphere hot add), and some platforms offer no
instance snapshot at all (vSphere, as reviewed). The "only one platform is documented" wording was removed.
