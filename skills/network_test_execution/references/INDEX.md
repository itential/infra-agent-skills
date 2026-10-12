# Network Test Execution — Platform Index

| Vendor / platform | Directory | Scope | Notes |
|---|---|---|---|
| Cisco pyATS / AEtest | [aetest.md](cisco_pyats/aetest.md) | Prepare and run Python tests through Easypy; inspect results | Explicit test assertions; setup/test/cleanup effects require review |
| Cisco Genie / Blitz | [blitz.md](cisco_pyats/blitz.md) | Prepare and run a named YAML testcase; inspect action results | Dedicated Blitz schema validation is not promised |
| Cisco Genie / Robot Framework | [robot.md](cisco_pyats/robot.md) | Prepare and execute keyword suites; inspect Robot results | Optional libraries must be installed |
| Cisco Genie harness | [genie-harness.md](cisco_pyats/genie-harness.md) | Run approved trigger/verification datafiles | Trigger implementations and platform requirements are inputs |
| Cisco pyATS Health Check | [health.md](cisco_pyats/health.md) | Run built-in/custom health processors within a job | No standalone monitoring; clearing/deletion options are flagged |
| Cisco XPRESSO | [cisco_xpresso/](cisco_xpresso/procedure.md) | Submit one registered job/profile and inspect its request results | Authenticated UI; registration, scheduling, bundles, and deployment excluded |

Companion files use each mode's basename (`aetest-endpoints.md`, for example). Each pyATS row links straight to its complete mode procedure; `cisco_pyats/procedure.md` holds the
shared result vocabulary. Native result vocabularies remain
platform-specific; queue acceptance does not establish that a test passed.
