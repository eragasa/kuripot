# tests/kuripot/core/test_Kuripot.py

from __future__ import annotations

import pytest

from kuripot.core.archive import KuripotArchive
from kuripot.core.kuripot import Kuripot
from kuripot.core.net import KuripotNet
from kuripot.core.operator import KuripotOperator
from kuripot.core.token import KuripotToken


class DummyIO:
    def export(self, net: KuripotNet) -> str:
        return f"exported:{net.net_id}"


def test__init__creates_empty_io_registry() -> None:
    # A Kuripot instance starts with no registered I/O adapters.
    kuripot = Kuripot()

    assert kuripot.io_registry == {}


def test__create_net__with_net_id() -> None:
    # Kuripot creates backend-independent net objects.
    kuripot = Kuripot()

    net = kuripot.create_net(net_id="demo_net")

    assert isinstance(net, KuripotNet)
    assert net.net_id == "demo_net"


def test__create_archive__with_archive_id() -> None:
    # Kuripot creates archive semantic objects.
    kuripot = Kuripot()

    archive = kuripot.create_archive(archive_id="state_archive")

    assert isinstance(archive, KuripotArchive)
    assert archive.archive_id == "state_archive"


def test__create_operator__with_operator_id() -> None:
    # Kuripot creates operator semantic objects.
    kuripot = Kuripot()

    operator = kuripot.create_operator(operator_id="operator_generator")

    assert isinstance(operator, KuripotOperator)
    assert operator.operator_id == "operator_generator"


def test__create_token__without_payload() -> None:
    # Kuripot creates token semantic objects.
    # The payload is optional and defaults to None.
    kuripot = Kuripot()

    token = kuripot.create_token(token_id="state_0")

    assert isinstance(token, KuripotToken)
    assert token.token_id == "state_0"
    assert token.payload is None


def test__register_io__with_adapter() -> None:
    # I/O adapters are registered under explicit adapter identifiers.
    kuripot = Kuripot()
    adapter = DummyIO()

    kuripot.register_io(io_id="dummy", adapter=adapter)

    assert kuripot.io_registry["dummy"] is adapter


def test__export__with_registered_adapter() -> None:
    # Export delegates to the registered adapter.
    kuripot = Kuripot()
    net = kuripot.create_net(net_id="demo_net")

    kuripot.register_io(io_id="dummy", adapter=DummyIO())

    assert kuripot.export(net, target="dummy") == "exported:demo_net"


def test__export__with_unknown_target_raises_value_error() -> None:
    # Export should fail clearly when the requested adapter is not registered.
    kuripot = Kuripot()
    net = kuripot.create_net(net_id="demo_net")

    with pytest.raises(ValueError, match="Unknown I/O target"):
        kuripot.export(net, target="missing")