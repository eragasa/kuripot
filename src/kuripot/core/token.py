# kuritpot/core/token.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class KuripotToken():
  id: str
  payload: Any = None
  