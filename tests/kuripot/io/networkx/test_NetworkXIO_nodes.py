# tests/kuripot/io/networkx/test_NetworkXIO_nodes.py

from __future__ import annotations

from kuripot.core.archive import KuripotArchive
from kuripot.core.net import KuripotNet
from kuripot.core.operator import KuripotOperator
from kuripot.io.io_networkx import NetworkXIO


def test__export__adds_archive_nodes(
    networkx_io: NetworkXIO,
) -> None:
    # Archives become graph nodes labeled with kind="archive".
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")

    net.add_archive(archive)

    graph = networkx_io.export(net)

    assert archive.archive_id in graph.nodes
    assert graph.nodes[archive.archive_id]["kind"] == "archive"
    assert graph.nodes[archive.archive_id]["archive"] == archive


def test__export__adds_operator_nodes(
    networkx_io: NetworkXIO,
) -> None:
    # Operators become graph nodes labeled with kind="operator".
    net = KuripotNet(net_id="demo_net")
    operator = KuripotOperator(operator_id="operator_generator")

    net.add_operator(operator)

    graph = networkx_io.export(net)

    assert operator.operator_id in graph.nodes
    assert graph.nodes[operator.operator_id]["kind"] == "operator"
    assert graph.nodes[operator.operator_id]["operator"] == operator