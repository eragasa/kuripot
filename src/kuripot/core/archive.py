# src/kuripot/core/archive.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KuripotArchive:
    """
    An archive represents a state container in a Kuripot workflow.

    In Petri-net language, an archive corresponds to a place.

    In Kuripot language, an archive stores tokens that represent concrete
    states, datasets, models, configurations, artifacts, or derived outputs.

    Parameters
    ----------
    archive_id:
        Stable identifier for the archive.
    """

    archive_id: str