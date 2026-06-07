# tests/kuripot/test_exports.py

from __future__ import annotations


def test__package_exports__core_classes() -> None:
    # The top-level package should expose the main public API.
    from kuripot import (
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