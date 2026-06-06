# tests/kuripot/core/test_KuripotToken.py

from __future__ import annotations

from kuripot.core.token import KuripotToken


def test_create_token() -> None:
    token = KuripotToken(id="state_0")
    assert token.id == "state_0"
    assert token.payload is None