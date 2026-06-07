# src/kuripot/io/io_base.py

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from kuripot.core.net import KuripotNet


@runtime_checkable
class KuripotIOProtocol(Protocol):
    """
    Structural interface for Kuripot I/O adapters.

    An I/O adapter translates a backend-independent KuripotNet into an
    external representation, such as a NetworkX graph, SNAKES Petri net,
    PM4Py structure, Mermaid diagram, or serialized file format.

    Implementations are not required to inherit from this protocol. They only
    need to provide the same method signature.
    """

    def export(
        self,
        net: KuripotNet,
    ) -> Any:
        """
        Export a KuripotNet to an external representation.
        """
        ...