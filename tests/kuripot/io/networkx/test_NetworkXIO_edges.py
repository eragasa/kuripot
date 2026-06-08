# tests/kuripot/io/networkx/test_NetworkXIO_edges.py

from __future__ import annotations

from kuripot.core.net import KuripotNet
from kuripot.io.io_networkx import NetworkXIO


def test__export__adds_input_edges(
    simple_transition_net: KuripotNet,
    networkx_io: NetworkXIO,
) -> None:
    # Input arcs become directed graph edges from archive to operator.
    graph = networkx_io.export(simple_transition_net)

    assert graph.has_edge("state_archive", "operator_generator")
    assert graph.edges["state_archive", "operator_generator"]["kind"] == "input"
    assert (
        graph.edges["state_archive", "operator_generator"]["token"].token_id
        == "state_0"
    )


def test__export__adds_output_edges(
    simple_transition_net: KuripotNet,
    networkx_io: NetworkXIO,
) -> None:
    # Output arcs become directed graph edges from operator to archive.
    graph = networkx_io.export(simple_transition_net)

    assert graph.has_edge("operator_generator", "updated_state_archive")
    assert (
        graph.edges["operator_generator", "updated_state_archive"]["kind"]
        == "output"
    )
    assert (
        graph.edges["operator_generator", "updated_state_archive"]["token"].token_id
        == "state_1"
    )