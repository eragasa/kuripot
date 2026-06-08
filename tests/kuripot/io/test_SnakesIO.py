# tests/kuripot/io/test_SnakesIO.py
from __future__ import annotations
import pytest

from snakes.nets import PetriNet, Substitution

from kuripot.core.archive import KuripotArchive
from kuripot.core.net import KuripotNet
from kuripot.core.operator import KuripotOperator
from kuripot.core.token import KuripotToken
from kuripot.io.io_base import KuripotIOProtocol
from kuripot.io.io_snakes import SnakesIO


@pytest.fixture
def empty_net() -> KuripotNet:
    return KuripotNet(net_id="demo_net")


@pytest.fixture
def simple_transition_net() -> KuripotNet:
    net = KuripotNet(net_id="demo_net")

    state_archive = KuripotArchive(archive_id="state_archive")
    updated_archive = KuripotArchive(archive_id="updated_state_archive")
    operator = KuripotOperator(operator_id="operator_generator")

    state_0 = KuripotToken(token_id="state_0")
    state_1 = KuripotToken(token_id="state_1")

    net.add_archive(state_archive, tokens=[state_0])
    net.add_archive(updated_archive)
    net.add_operator(operator)

    net.add_input_arc(
        state_archive,
        operator,
        state_0,
    )

    net.add_output_arc(
        operator,
        updated_archive,
        state_1,
    )

    return net


@pytest.fixture
def snakes_io() -> SnakesIO:
    return SnakesIO()


def test__SnakesIO__satisfies_KuripotIOProtocol(snakes_io: SnakesIO) -> None:
    # SnakesIO satisfies the Kuripot I/O protocol because it implements
    # export(net). It does not need to inherit from a shared base class.
    assert isinstance(snakes_io, KuripotIOProtocol)


def test__export__returns_petri_net(
    empty_net: KuripotNet,
    snakes_io: SnakesIO,
) -> None:
    # SnakesIO exports a KuripotNet to a SNAKES PetriNet.
    snakes_net = snakes_io.export(empty_net)

    assert isinstance(snakes_net, PetriNet)
    assert snakes_net.name == "demo_net"


def test__export__adds_places_from_archives(snakes_io: SnakesIO) -> None:
    # Archives become SNAKES places.
    net = KuripotNet(net_id="demo_net")
    archive = KuripotArchive(archive_id="state_archive")

    net.add_archive(archive)

    snakes_net = snakes_io.export(net)

    assert snakes_net.place("state_archive").name == "state_archive"


def test__export__adds_transitions_from_operators(snakes_io: SnakesIO) -> None:
    # Operators become SNAKES transitions.
    net = KuripotNet(net_id="demo_net")
    operator = KuripotOperator(operator_id="operator_generator")

    net.add_operator(operator)

    snakes_net = snakes_io.export(net)

    assert snakes_net.transition("operator_generator").name == "operator_generator"


def test__export__adds_initial_tokens_to_places(
    simple_transition_net: KuripotNet,
    snakes_io: SnakesIO,
) -> None:
    # Archive tokens become initial SNAKES place tokens.
    # Places store the raw KuripotToken objects.
    snakes_net = snakes_io.export(simple_transition_net)

    state_0 = KuripotToken(token_id="state_0")

    assert state_0 in snakes_net.place("state_archive").tokens


def test__export__creates_executable_transition(
    simple_transition_net: KuripotNet,
    snakes_io: SnakesIO,
) -> None:
    # A simple archive -> operator -> archive structure exports to an
    # executable SNAKES Petri net.
    snakes_net = snakes_io.export(simple_transition_net)

    state_0 = KuripotToken(token_id="state_0")
    state_1 = KuripotToken(token_id="state_1")

    transition = snakes_net.transition("operator_generator")
    binding = Substitution()

    assert transition.enabled(binding)

    transition.fire(binding)

    assert state_0 not in snakes_net.place("state_archive").tokens
    assert state_1 in snakes_net.place("updated_state_archive").tokens

def test__export__raises_for_invalid_raw_net(snakes_io: SnakesIO) -> None:
    # SnakesIO validates the semantic net before export.
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
        snakes_io.export(net)