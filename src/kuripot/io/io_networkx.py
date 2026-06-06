# kuripot/io/io_networkx.py

from __future__ import annotations

import networkx as nx

from kuripot.core.net import KuripotNet


class NetworkXIO:
    name = "networkx"

    def export(
        self,
        net: KuripotNet,
    ) -> nx.DiGraph:
        graph = nx.DiGraph(name=net.name)

        for archive in net.archives.values():
            graph.add_node(
                archive.name,
                kind="archive",
            )

        for operator in net.operators.values():
            graph.add_node(
                operator.name,
                kind="operator",
            )

        for archive_name, operator_name, token in net.input_arcs:
            graph.add_edge(
                archive_name,
                operator_name,
                token=token,
                kind="input",
            )

        for operator_name, archive_name, token in net.output_arcs:
            graph.add_edge(
                operator_name,
                archive_name,
                token=token,
                kind="output",
            )

        return graph