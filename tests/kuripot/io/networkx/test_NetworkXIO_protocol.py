# tests/kuripot/io/networkx/test_NetworkXIO_protocol.py

from __future__ import annotations

from kuripot.io.io_base import KuripotIOProtocol
from kuripot.io.io_networkx import NetworkXIO


def test__NetworkXIO__satisfies_KuripotIOProtocol(
    networkx_io: NetworkXIO,
) -> None:
    # NetworkXIO satisfies the Kuripot I/O protocol because it implements
    # export(net).
    assert isinstance(networkx_io, KuripotIOProtocol)