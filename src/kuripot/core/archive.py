# kuritpot/core/archive.py

from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class KuripotArchive:
    name: str

    