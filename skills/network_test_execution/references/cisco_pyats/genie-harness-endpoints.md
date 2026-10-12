# Cisco Genie — Harness Bindings

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Harness Getting Started](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/harness/user/gettingstarted.html).
- [Harness Datafiles](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/harness/user/datafile.html).

## mapping.yaml

```yaml
devices:
  dut:
    context: cli
    label: uut
    mapping:
      cli: cli
```

The last `cli` is the actual connection name in this example testbed.

## job.py

`PYATS_TRIGGER_UIDS` supplies a comma-separated, explicit list of approved, documented
trigger identifiers. The three YAML files must exist and contain matching definitions.

```python
import os
from pathlib import Path
from genie.harness.main import gRun

def main(runtime):
    directory = Path(__file__).parent
    gRun(runtime=runtime,
         mapping_datafile=str(directory / 'mapping.yaml'),
         trigger_datafile=str(directory / 'triggers.yaml'),
         verification_datafile=str(directory / 'verifications.yaml'),
         trigger_uids=os.environ['PYATS_TRIGGER_UIDS'].split(','))
```

| Input | Documented meaning |
|---|---|
| `extends` | Inherit another datafile, including installed default definitions |
| `devices` | Select target device roles for a trigger or verification |
| `order` | Order trigger execution in the trigger datafile |
| `iteration.attempt` | Verification attempts |
| `iteration.interval` | Fixed seconds between attempts |
| `exclude` | Fields omitted from verification comparison |

This is intentionally not an invented trigger library. A named trigger without its documented
implementation and arguments is not ready to run.
