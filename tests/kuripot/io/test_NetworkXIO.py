# tests/kuripot/io/test_NetworkXIO.py
from __future__ import annotations
import pytest
import networkx as nx

from kuripot.core.archive import KuripotArchive
from kuripot.core.net import KuripotNet
from kuripot.core.operator import KuripotOperator
from kuripot.core.token import KuripotToken
from kuripot.io.io_networkx import NetworkXIO

class ValidateSpyNet:
    def __init__(self) -> None:
        self.net_id = "spy_net"
        self.archives = {}
        self.operators = {}
        self.input_arcs = []
        self.output_arcs = []
        self.validate_was_called = False

    def validate(self) -> None:
        self.validate_was_called = True

def test__export__calls_validate() -> None:
    # NetworkXIO validates the semantic net before export.
    net = ValidateSpyNet()

    NetworkXIO().export(net)

    assert net.validate_was_called

def test__export__returns_directed_graph() -> None:
    # NetworkXIO exports a KuripotNet to a NetworkX directed graph.
    net = KuripotNet(net_id="demo_net")
    adapter = NetworkXIO()

    graph = adapter.export(net)

    assert isinstance(graph, nx.DiGraph)
    assert graph.graph["name"] == "demo_net"


def test__export__adds_archive_nodes() -> None:
    # Archives become graph nodes labeled with kind="archive".
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")

    net.add_archive(archive)

    graph = NetworkXIO().export(net)

    assert "state_archive" in graph.nodes
    assert graph.nodes["state_archive"]["kind"] == "archive"
    assert graph.nodes["state_archive"]["archive"] == archive


def test__export__adds_operator_nodes() -> None:
    # Operators become graph nodes labeled with kind="operator".
    net = KuripotNet(net_id="demo_net")
    operator = KuripotOperator(operator_id="operator_generator")

    net.add_operator(operator)

    graph = NetworkXIO().export(net)

    assert "operator_generator" in graph.nodes
    assert graph.nodes["operator_generator"]["kind"] == "operator"
    assert graph.nodes["operator_generator"]["operator"] == operator


def test__export__adds_input_edges() -> None:
    # Input arcs become directed graph edges from archive to operator.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")
    operator = KuripotOperator(operator_id="operator_generator")
    token = KuripotToken(token_id="state_0")

    net.add_archive(archive)
    net.add_operator(operator)
    net.add_input_arc(archive, operator, token)

    graph = NetworkXIO().export(net)

    assert graph.has_edge("state_archive", "operator_generator")
    assert graph.edges["state_archive", "operator_generator"]["kind"] == "input"
    assert graph.edges["state_archive", "operator_generator"]["token"] == token


def test__export__adds_output_edges() -> None:
    # Output arcs become directed graph edges from operator to archive.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="updated_state_archive")
    operator = KuripotOperator(operator_id="operator_generator")
    token = KuripotToken(token_id="state_1")

    net.add_archive(archive)
    net.add_operator(operator)
    net.add_output_arc(operator, archive, token)

    graph = NetworkXIO().export(net)

    assert graph.has_edge("operator_generator", "updated_state_archive")
    assert graph.edges["operator_generator", "updated_state_archive"]["kind"] == "output"
    assert graph.edges["operator_generator", "updated_state_archive"]["token"] == token

def test__export__raises_for_invalid_raw_net() -> None:
    # NetworkXIO validates the semantic net before export.
    # This protects imported, deserialized, or manually modified nets.
    net = KuripotNet(net_id="demo_net")

    archive = KuripotArchive(archive_id="state_archive")
    operator = KuripotOperator(operator_id="missing_operator")
    token = KuripotToken(token_id="state_0")

    net.add_archive(archive)

    # Deliberately bypass the public add_input_arc() method to simulate a
    # malformed raw/imported net.
    net.input_arcs.append(
        (
            archive.archive_id,
            operator.operator_id,
            token,
        )
    )

    with pytest.raises(ValueError, match="unknown operator"):
        NetworkXIO().export(net)