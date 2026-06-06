# tests/smoke_import.py

from __future__ import annotations

def test_import_kuripot() -> None:
    import kuripot
    assert kuripot is not None