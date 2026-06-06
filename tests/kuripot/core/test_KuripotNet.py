# tests/kuripot/core/test_KuripotNet.py

from __future__ import annotations

from kuripot.core.archive import KuripotArchive
from kuripot.core.net import KuripotNet
from kuripot.core.operator import KuripotOperator
from kuripot.core.token import KuripotToken


def test__init__with_net_id() -> None:
    # A net is created with a stable net identifier.
    # The net identifier names the semantic workflow graph.
    net = KuripotNet(net_id="demo_net")

    assert net.net_id == "demo_net"
    assert net.archives == {}
    assert net.operators == {}
    assert net.archive_tokens == {}
    assert net.input_arcs == []
    assert net.output_arcs == []


def test__add_archive__without_tokens() -> None:
    # An archive may be added without initial tokens.
    # The archive token list is initialized as empty.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")

    net.add_archive(archive)

    assert net.archives["state_archive"] == archive
    assert net.archive_tokens["state_archive"] == []


def test__add_archive__with_tokens() -> None:
    # An archive may be initialized with tokens.
    # These tokens represent the initial marking of that archive.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")
    token = KuripotToken(token_id="state_0")

    net.add_archive(archive, tokens=[token])

    assert net.archives["state_archive"] == archive
    assert net.archive_tokens["state_archive"] == [token]


def test__add_operator__with_operator() -> None:
    # An operator may be added to the semantic net.
    # The operator is stored by its stable operator identifier.
    net = KuripotNet(net_id="demo_net")
    operator = KuripotOperator(operator_id="operator_generator")

    net.add_operator(operator)

    assert net.operators["operator_generator"] == operator


def test__add_input_arc__with_token() -> None:
    # An input arc records that an operator consumes a token from an archive.
    # This is semantic structure only; execution is handled by a backend.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")
    operator = KuripotOperator(operator_id="operator_generator")
    token = KuripotToken(token_id="state_0")

    net.add_input_arc(archive, operator, token)

    assert net.input_arcs == [
        (
            "state_archive",
            "operator_generator",
            token,
        )
    ]


def test__add_output_arc__with_token() -> None:
    # An output arc records that an operator produces a token into an archive.
    # This is semantic structure only; execution is handled by a backend.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="updated_state_archive")
    operator = KuripotOperator(operator_id="operator_generator")
    token = KuripotToken(token_id="state_1")

    net.add_output_arc(operator, archive, token)

    assert net.output_arcs == [
        (
            "operator_generator",
            "updated_state_archive",
            token,
        )
    ]