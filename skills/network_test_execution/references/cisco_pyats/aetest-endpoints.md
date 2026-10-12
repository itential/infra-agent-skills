# Cisco pyATS — AEtest Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Script Structure](https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html).
- [Steps](https://pubhub.devnetcloud.com/media/pyats/docs/aetest/steps.html).
- [Jobfiles and Tasks](https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html).
- [Unicon Connections](https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html).

## test.py

Original example: the caller supplies the expected substring for the approved command. This
illustrates a text assertion; it does not assert that any particular version is correct.

```python
from pyats import aetest

class Prepare(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed, device_name):
        device = testbed.devices[device_name]
        self.parent.parameters['device'] = device
        device.connect(via='cli', init_exec_commands=[], init_config_commands=[])

class CheckOutput(aetest.Testcase):
    @aetest.test
    def check(self, device, command, expected_text, steps):
        with steps.start('Check requested output') as step:
            observed = device.execute(command)
            if not expected_text or expected_text not in observed:
                step.failed('The requested output assertion was not satisfied')

class Release(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed, device_name):
        testbed.devices[device_name].disconnect()
```

## job.py

```python
import os
from pathlib import Path
from pyats.easypy import run

def main(runtime):
    run(testscript=str(Path(__file__).with_name('test.py')),
        runtime=runtime,
        device_name='dut',
        command='show version',
        expected_text=os.environ['PYATS_EXPECTED_TEXT'])
```

`PYATS_EXPECTED_TEXT` is an explicit assertion input, not a default threshold. A missing input is
an error. These files execute only after the procedure's live-action review and confirmation gate.
