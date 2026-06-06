# tests/kuripot/core/test_KuripotToken.py

from __future__ import annotations

from kuripot.core.token import KuripotToken


def test__init__without_payload() -> None:
    # A token may be created with only a stable token identifier.
    # In this case, the payload defaults to None.
    token = KuripotToken(token_id="state_0")

    assert token.token_id == "state_0"
    assert token.payload is None


def test__init__with_payload() -> None:
    # A token may optionally carry an attached payload.
    # The payload is intentionally generic because tokens may represent
    # paths, metadata records, state objects, datasets, or derived artifacts.
    token = KuripotToken(
        token_id="state_1",
        payload={"path": "data/state_1.json"},
    )

    assert token.token_id == "state_1"
    assert token.payload == {"path": "data/state_1.json"}