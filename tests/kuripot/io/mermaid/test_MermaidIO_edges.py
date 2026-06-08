# tests/kuripot/io/mermaid/test_MermaidIO_edges.py

from __future__ import annotations

from kuripot.core.net import KuripotNet
from kuripot.io.io_mermaid import MermaidIO


def test__export__adds_input_edges(
    simple_transition_net: KuripotNet,
    mermaid_io: MermaidIO,
) -> None:
    # Input arcs become directed Mermaid edges from archive to operator.
    text = mermaid_io.export(simple_transition_net)

    assert (
        'node_state_archive -- "state_0" --> node_operator_generator'
        in text
    )


def test__export__adds_output_edges(
    simple_transition_net: KuripotNet,
    mermaid_io: MermaidIO,
) -> None:
    # Output arcs become directed Mermaid edges from operator to archive.
    text = mermaid_io.export(simple_transition_net)

    assert (
        'node_operator_generator -- "state_1" --> node_updated_state_archive'
        in text
    )