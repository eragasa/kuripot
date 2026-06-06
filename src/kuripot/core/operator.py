# kuripot/core/operator.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class KuripotOperator:
    name: str

    