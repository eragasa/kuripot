# tests/kuripot/io/networkx/test_NetworkXIO_empty.py

from __future__ import annotations

import networkx as nx

from kuripot.core.net import KuripotNet
from kuripot.io.io_networkx import NetworkXIO


def test__export__empty_net_returns_directed_graph(
    networkx_io: NetworkXIO,
) -> None:
    # NetworkXIO exports an empty KuripotNet to a NetworkX directed graph.
    net = KuripotNet(net_id="demo_net")

    graph = networkx_io.export(net)

    assert isinstance(graph, nx.DiGraph)
    assert graph.graph["name"] == "demo_net"