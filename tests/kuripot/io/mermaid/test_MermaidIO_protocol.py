# tests/kuripot/io/mermaid/test_MermaidIO_protocol.py

from __future__ import annotations

from kuripot.io.io_base import KuripotIOProtocol
from kuripot.io.io_mermaid import MermaidIO


def test__MermaidIO__satisfies_KuripotIOProtocol(
    mermaid_io: MermaidIO,
) -> None:
    # MermaidIO satisfies the Kuripot I/O protocol because it implements
    # export(net).
    assert isinstance(mermaid_io, KuripotIOProtocol)