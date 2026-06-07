# src/kuripot/core/kuripot.py

from __future__ import annotations

from typing import Any

from .archive import KuripotArchive
from .net import KuripotNet
from .operator import KuripotOperator
from .token import KuripotToken


class Kuripot:
    """
    Master facade for creating Kuripot semantic objects.

    Kuripot is not itself a workflow net. It creates backend-independent
    semantic objects and owns a registry of I/O adapters.

    The I/O registry is intentionally simple at this stage. Adapters can be
    registered manually before a configuration system is introduced.
    """

    def __init__(self) -> None:
        self.io_registry: dict[str, Any] = {}

    def register_io(
        self,
        io_id: str,
        adapter: Any,
    ) -> None:
        """
        Register an I/O adapter.

        Parameters
        ----------
        io_id:
            Stable identifier for the adapter.

        adapter:
            Object that implements an ``export(net)`` method.
        """

        self.io_registry[io_id] = adapter

    def create_net(
        self,
        net_id: str,
    ) -> KuripotNet:
        """
        Create a backend-independent workflow net.
        """

        return KuripotNet(net_id=net_id)

    def create_archive(
        self,
        archive_id: str,
    ) -> KuripotArchive:
        """
        Create an archive semantic object.
        """

        return KuripotArchive(archive_id=archive_id)

    def create_operator(
        self,
        operator_id: str,
    ) -> KuripotOperator:
        """
        Create an operator semantic object.
        """

        return KuripotOperator(operator_id=operator_id)

    def create_token(
        self,
        token_id: str,
        payload: Any = None,
    ) -> KuripotToken:
        """
        Create a token semantic object.
        """

        return KuripotToken(
            token_id=token_id,
            payload=payload,
        )

    def export(
        self,
        net: KuripotNet,
        *,
        target: str,
    ) -> Any:
        """
        Export a KuripotNet using a registered I/O adapter.
        """

        if target not in self.io_registry:
            raise ValueError(
                f"Unknown I/O target: {target}. "
                f"Available targets: {list(self.io_registry)}"
            )

        return self.io_registry[target].export(net)