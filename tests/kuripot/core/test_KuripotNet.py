# tests/kuripot/core/test_KuripotNet.py

from __future__ import annotations

import pytest

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
    # The archive and operator must already be registered in the net.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")
    operator = KuripotOperator(operator_id="operator_generator")
    token = KuripotToken(token_id="state_0")

    net.add_archive(archive)
    net.add_operator(operator)
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
    # The operator and archive must already be registered in the net.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="updated_state_archive")
    operator = KuripotOperator(operator_id="operator_generator")
    token = KuripotToken(token_id="state_1")

    net.add_archive(archive)
    net.add_operator(operator)
    net.add_output_arc(operator, archive, token)

    assert net.output_arcs == [
        (
            "operator_generator",
            "updated_state_archive",
            token,
        )
    ]


def test__has_archive__with_existing_archive() -> None:
    # has_archive returns True when the archive has been added to the net.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")

    net.add_archive(archive)

    assert net.has_archive("state_archive")


def test__has_archive__with_missing_archive() -> None:
    # has_archive returns False when the archive is absent.
    net = KuripotNet(net_id="demo_net")

    assert not net.has_archive("missing_archive")


def test__has_operator__with_existing_operator() -> None:
    # has_operator returns True when the operator has been added to the net.
    net = KuripotNet(net_id="demo_net")
    operator = KuripotOperator(operator_id="operator_generator")

    net.add_operator(operator)

    assert net.has_operator("operator_generator")


def test__has_operator__with_missing_operator() -> None:
    # has_operator returns False when the operator is absent.
    net = KuripotNet(net_id="demo_net")

    assert not net.has_operator("missing_operator")


def test__add_input_arc__raises_for_unknown_archive() -> None:
    # Input arcs require the archive to already be registered.
    net = KuripotNet(net_id="demo_net")

    missing_archive = KuripotArchive(archive_id="missing_archive")
    operator = KuripotOperator(operator_id="operator_generator")
    token = KuripotToken(token_id="state_0")

    net.add_operator(operator)

    with pytest.raises(ValueError, match="unknown archive"):
        net.add_input_arc(missing_archive, operator, token)


def test__add_input_arc__raises_for_unknown_operator() -> None:
    # Input arcs require the operator to already be registered.
    net = KuripotNet(net_id="demo_net")

    archive = KuripotArchive(archive_id="state_archive")
    missing_operator = KuripotOperator(operator_id="missing_operator")
    token = KuripotToken(token_id="state_0")

    net.add_archive(archive)

    with pytest.raises(ValueError, match="unknown operator"):
        net.add_input_arc(archive, missing_operator, token)


def test__add_output_arc__raises_for_unknown_operator() -> None:
    # Output arcs require the operator to already be registered.
    net = KuripotNet(net_id="demo_net")

    missing_operator = KuripotOperator(operator_id="missing_operator")
    archive = KuripotArchive(archive_id="updated_state_archive")
    token = KuripotToken(token_id="state_1")

    net.add_archive(archive)

    with pytest.raises(ValueError, match="unknown operator"):
        net.add_output_arc(missing_operator, archive, token)


def test__add_output_arc__raises_for_unknown_archive() -> None:
    # Output arcs require the archive to already be registered.
    net = KuripotNet(net_id="demo_net")

    operator = KuripotOperator(operator_id="operator_generator")
    missing_archive = KuripotArchive(archive_id="missing_archive")
    token = KuripotToken(token_id="state_1")

    net.add_operator(operator)

    with pytest.raises(ValueError, match="unknown archive"):
        net.add_output_arc(operator, missing_archive, token)


def test__validate__with_valid_net() -> None:
    # A net validates when all arcs reference registered archives and operators.
    net = KuripotNet(net_id="demo_net")

    state_archive = KuripotArchive(archive_id="state_archive")
    updated_archive = KuripotArchive(archive_id="updated_state_archive")
    operator = KuripotOperator(operator_id="operator_generator")

    state_0 = KuripotToken(token_id="state_0")
    state_1 = KuripotToken(token_id="state_1")

    net.add_archive(state_archive, tokens=[state_0])
    net.add_archive(updated_archive)
    net.add_operator(operator)

    net.add_input_arc(state_archive, operator, state_0)
    net.add_output_arc(operator, updated_archive, state_1)

    net.validate()