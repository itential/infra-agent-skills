# Cisco Genie — Robot Keyword Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Genie Robot Framework Guide](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/robot/index.html).
- [Unicon Robot Framework](https://pubhub.devnetcloud.com/media/unicon/docs/robot/index.html).

## suite.robot

```robot
*** Settings ***
Library    ats.robot.pyATSRobot
Library    genie.libs.robot.GenieRobot
Library    unicon.robot.UniconRobot
Suite Teardown    disconnect from device "dut"

*** Variables ***
${testbed}    testbed.yaml

*** Test Cases ***
Collect Version
    use genie testbed "${testbed}"
    connect to device "dut" via "cli"
    ${parsed}=    parse "show version" on device "dut"
```

This is a collection-only example; no unsupported dictionary key or invented expected version is
asserted. Additional network assertions are explicit suite inputs. Profile/compare and reusable
trigger keywords use the shapes in the linked Genie guide and its keyword reference.
