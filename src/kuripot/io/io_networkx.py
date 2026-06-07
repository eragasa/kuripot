# src/kuripot/io/io_networkx.py

from __future__ import annotations

import networkx as nx

from kuripot.core.net import KuripotNet


class NetworkXIO:
    """
    I/O adapter that exports a KuripotNet to a NetworkX directed graph.

    The exported graph is structural, not executable.

    A NetworkX DiGraph is a directed graph, not necessarily a directed
    acyclic graph. Cycles are allowed. This matters because Kuripot workflows
    may include feedback loops, iterative refinement, and repeated state
    updates.

    Node kinds:

    - archive
    - operator

    Edge kinds:

    - input
    - output
    """

    def export(
        self,
        net: KuripotNet,
    ) -> nx.DiGraph:
        """
        Export a KuripotNet as a NetworkX DiGraph.
        """

        graph = nx.DiGraph(name=net.net_id)

        for archive_id, archive in net.archives.items():
            graph.add_node(
                archive_id,
                kind="archive",
                archive=archive,
            )

        for operator_id, operator in net.operators.items():
            graph.add_node(
                operator_id,
                kind="operator",
                operator=operator,
            )

        for archive_id, operator_id, token in net.input_arcs:
            graph.add_edge(
                archive_id,
                operator_id,
                kind="input",
                token=token,
            )

        for operator_id, archive_id, token in net.output_arcs:
            graph.add_edge(
                operator_id,
                archive_id,
                kind="output",
                token=token,
            )

        return graph