# tests/kuripot/io/test_exports.py

from __future__ import annotations


def test__io_exports__protocols_and_adapters() -> None:
    # The kuripot.io namespace should expose public I/O protocols and adapters.
    from kuripot.io import (
        KuripotIOProtocol,
        MermaidIO,
        NetworkXIO,
        SnakesIO,
    )

    assert KuripotIOProtocol.__name__ == "KuripotIOProtocol"
    assert MermaidIO.__name__ == "MermaidIO"
    assert NetworkXIO.__name__ == "NetworkXIO"
    assert SnakesIO.__name__ == "SnakesIO"