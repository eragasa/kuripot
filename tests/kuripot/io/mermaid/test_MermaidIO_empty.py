# tests/kuripot/io/mermaid/test_MermaidIO_empty.py

from __future__ import annotations

from kuripot.core.net import KuripotNet
from kuripot.io.io_mermaid import MermaidIO


def test__export__empty_net_returns_flowchart_header(
    mermaid_io: MermaidIO,
) -> None:
    # An empty net exports to a valid Mermaid flowchart header.
    net = KuripotNet(net_id="demo_net")

    text = mermaid_io.export(net)

    assert text == "flowchart LR"