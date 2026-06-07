# tests/kuripot/core/test_exports.py

from __future__ import annotations

def test__core_exports__semantic_classes() -> None:
    # The kuripot.core namespace should expose semantic model classes.
    from kuripot.core import (
        Kuripot,
        KuripotArchive,
        KuripotNet,
        KuripotOperator,
        KuripotToken,
    )

    assert Kuripot.__name__ == "Kuripot"
    assert KuripotArchive.__name__ == "KuripotArchive"
    assert KuripotNet.__name__ == "KuripotNet"
    assert KuripotOperator.__name__ == "KuripotOperator"
    assert KuripotToken.__name__ == "KuripotToken"