# kuripot/config.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import importlib
import tomllib


@dataclass(frozen=True)
class IOAdapterSpec:
    name: str
    enabled: bool
    module: str
    class_name: str
    description: str = ""


@dataclass(frozen=True)
class KuripotConfig:
    raw: dict[str, Any]
    default_io: str
    default_engine: str
    io_adapters: dict[str, IOAdapterSpec]


def load_kuripot_config(path: str | Path) -> KuripotConfig:
    path = Path(path)

    with path.open("rb") as f:
        raw = tomllib.load(f)

    io_adapters: dict[str, IOAdapterSpec] = {}

    for name, spec in raw.get("io", {}).items():
        if not isinstance(spec, dict):
            continue

        io_adapters[name] = IOAdapterSpec(
            name=name,
            enabled=spec.get("enabled", False),
            module=spec["module"],
            class_name=spec["class"],
            description=spec.get("description", ""),
        )

    return KuripotConfig(
        raw=raw,
        default_io=raw["core"]["default_io"],
        default_engine=raw["execution"]["default_engine"],
        io_adapters=io_adapters,
    )


def instantiate_adapter(spec: IOAdapterSpec):
    module = importlib.import_module(spec.module)
    cls = getattr(module, spec.class_name)
    return cls()