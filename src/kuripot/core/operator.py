# src/kuripot/core/operator.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KuripotOperator:
    """
    An operator represents an executable transformation in a Kuripot workflow.

    In Petri-net language, an operator corresponds to a transition.

    In Kuripot language, an operator consumes tokens from input archives and
    produces tokens in output archives. The operator may represent a simulation,
    analysis step, data transformation, model update, validation routine, or
    artifact generator.

    Parameters
    ----------
    operator_id:
        Stable identifier for the operator.
    """

    operator_id: str