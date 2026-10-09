# Diagrams Python bindings

Sources: [Diagram](https://diagrams.mingrammer.com/docs/guides/diagram), [Cluster](https://diagrams.mingrammer.com/docs/guides/cluster), [node/edge guide](https://diagrams.mingrammer.com/docs/guides/node), [AWS nodes](https://diagrams.mingrammer.com/docs/nodes/aws), retrieved 2026-10-09. This is a local library, with no REST endpoint or AWS credential requirement for the rendering operation.

| Operation | Binding |
|---|---|
| Diagram context | `diagrams.Diagram(title, filename=<path-without-extension>, outformat=<format-or-list>, show=False)` |
| Group context | `diagrams.Cluster(label)`; contexts can nest |
| AWS node | Import the documented class from its `diagrams.aws.<category>` module and instantiate with a label |
| Edge | `>>` for forward, `<<` for reverse, `-` for undirected relationships in the supplied model |

Formats documented by the publisher are `png`, `jpg`, `svg`, `pdf`, `dot`. Example source, using only placeholder labels:

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2

with Diagram("Compute grouping", filename="architecture", outformat="svg", show=False):
    with Cluster("Supplied group"):
        first = EC2("instance-a")
        second = EC2("instance-b")
        first >> second
```

This example describes a supplied relationship; it does not query AWS or establish actual connectivity.
