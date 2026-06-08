# tests/kuripot/io/mermaid/test_MermaidIO_nodes.py

from __future__ import annotations

from kuripot.core.archive import KuripotArchive
from kuripot.core.net import KuripotNet
from kuripot.core.operator import KuripotOperator
from kuripot.io.io_mermaid import MermaidIO


def test__export__adds_archive_nodes(
    mermaid_io: MermaidIO,
) -> None:
    # Archives become rounded Mermaid nodes.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")

    net.add_archive(archive)

    text = mermaid_io.export(net)

    assert "flowchart LR" in text
    assert "node_state_archive((state_archive))" in text


def test__export__adds_operator_nodes(
    mermaid_io: MermaidIO,
) -> None:
    # Operators become rectangular Mermaid nodes.
    net = KuripotNet(net_id="demo_net")
    operator = KuripotOperator(operator_id="operator_generator")

    net.add_operator(operator)

    text = mermaid_io.export(net)

    assert "flowchart LR" in text
    assert 'node_operator_generator["operator_generator"]' in text