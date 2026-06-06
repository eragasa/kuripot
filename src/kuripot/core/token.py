# src/kuripot/core/token.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class KuripotToken:
    """
    A token represents one concrete state object inside a Kuripot workflow.

    In Petri-net language, a token is the object carried by places and
    consumed or produced by transitions.

    In Kuripot language, a token may represent a dataset, simulation state,
    file path, model identifier, configuration, note, artifact, or derived
    result.

    Parameters
    ----------
    id:
        Stable identifier for the token.

    payload:
        Optional attached Python object. The payload is intentionally generic
        because early Kuripot tokens may wrap strings, dictionaries, paths,
        metadata records, or domain-specific state objects.
    """

    token_id: str
    payload: Any = None