# tests/kuripot/io/networkx/conftest.py

from __future__ import annotations

import pytest

from kuripot.core.archive import KuripotArchive
from kuripot.core.net import KuripotNet
from kuripot.core.operator import KuripotOperator
from kuripot.core.token import KuripotToken
from kuripot.io.io_networkx import NetworkXIO


class ValidateSpyNet:
    """
    Minimal net-like object used to verify that NetworkXIO calls validate().

    This object is intentionally not a KuripotNet. It isolates the adapter
    contract:

        export(net) must call net.validate() before reading net structure.

    The object only provides the attributes NetworkXIO needs after validation.
    """
    def __init__(self) -> None:
        self.net_id = "spy_net"
        self.archives = {}
        self.operators = {}
        self.input_arcs = []
        self.output_arcs = []
        self.validate_was_called = False

    def validate(self) -> None:
        self.validate_was_called = True


@pytest.fixture
def networkx_io() -> NetworkXIO:
    """
    Shared NetworkX adapter instance.

    The adapter is stateless, so tests can safely use a fresh instance from
    this fixture.
    """
    return NetworkXIO()


@pytest.fixture
def simple_transition_net() -> KuripotNet:
    """
    Canonical archive -> operator -> archive workflow.

    This fixture represents the minimal nontrivial KURIPOT net:

        state_archive -> operator_generator -> updated_state_archive

    It is reused by edge-export tests because both input and output arc
    behavior depend on the same canonical structure.
    """
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

    return net


@pytest.fixture
def invalid_raw_net() -> KuripotNet:
    """
    Malformed net that bypasses public construction rules.

    Normal KURIPOT construction fails early when an arc references an unknown
    archive or operator. This fixture deliberately mutates input_arcs directly
    to simulate a future loader, deserializer, or importer producing malformed
    raw structure.

    I/O adapters should reject this net by calling net.validate() before export.
    """
    net = KuripotNet(net_id="demo_net")

    archive = KuripotArchive(archive_id="state_archive")
    missing_operator = KuripotOperator(operator_id="missing_operator")
    token = KuripotToken(token_id="state_0")

    net.add_archive(archive)

    # Deliberately bypass the public add_input_arc() method to simulate a
    # malformed raw/imported net.
    net.input_arcs.append(
        (
            archive.archive_id,
            missing_operator.operator_id,
            token,
        )
    )

    return net


@pytest.fixture
def validate_spy_net() -> ValidateSpyNet:
    """
    Spy net used only to check whether validate() was called.
    """
    return ValidateSpyNet()