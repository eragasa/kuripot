# tests/kuripot/io/test_KuripotIOProtocol.py

from __future__ import annotations

from kuripot.io.io_base import KuripotIOProtocol
from kuripot.io.io_networkx import NetworkXIO


def test__NetworkXIO__satisfies_KuripotIOProtocol() -> None:
    # NetworkXIO satisfies the Kuripot I/O protocol because it implements
    # export(net). It does not need to inherit from a shared base class.
    adapter = NetworkXIO()

    assert isinstance(adapter, KuripotIOProtocol)