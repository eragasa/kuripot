# tests/kuripot/core/test_KuripotOperator.py

from __future__ import annotations

from kuripot.core.operator import KuripotOperator


def test__init__with_operator_id() -> None:
    # An operator is created with a stable operator identifier.
    # The identifier names the transformation, not a specific execution run.
    operator = KuripotOperator(operator_id="operator_generator")

    assert operator.operator_id == "operator_generator"