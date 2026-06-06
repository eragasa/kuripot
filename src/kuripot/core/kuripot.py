# kuripot/core/kuripot.py

from __future__ import annotations

from typing import Any

from kuripot.config import load_kuripot_config, instantiate_adapter

from .archive import KuripotArchive
from .operator import KuripotOperator
from .token import KuripotToken
from .net import KuripotNet


class Kuripot:
    def __init__(self):
        self.io_registry: dict[str, Any] = {}

    @classmethod
    def from_toml(cls, path: str):
        kuripot = cls()
        config = load_kuripot_config(path)

        for name, spec in config.io_adapters.items():
            if not spec.enabled:
                continue

            adapter = instantiate_adapter(spec)
            kuripot.register_io(name, adapter)

        return kuripot

    def register_io(
        self,
        name: str,
        adapter: Any,
    ) -> None:
        self.io_registry[name] = adapter

    def create_net(
        self,
        name: str,
    ) -> KuripotNet:
        return KuripotNet(name=name)

    def create_archive(
        self,
        name: str,
    ) -> KuripotArchive:
        return KuripotArchive(name=name)

    def create_operator(
        self,
        name: str,
    ) -> KuripotOperator:
        return KuripotOperator(name=name)

    def create_token(
        self,
        id: str,
        payload: Any = None,
    ) -> KuripotToken:
        return KuripotToken(
            id=id,
            payload=payload,
        )

    def export(
        self,
        net: KuripotNet,
        *,
        target: str,
    ) -> Any:
        if target not in self.io_registry:
            raise ValueError(
                f"Unknown IO target: {target}. "
                f"Available targets: {list(self.io_registry)}"
            )

        return self.io_registry[target].export(net)