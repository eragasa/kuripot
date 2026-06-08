# tests/kuripot/io/mermaid/test_MermaidIO_validation.py

from __future__ import annotations

import pytest

from kuripot.core.net import KuripotNet
from kuripot.io.io_mermaid import MermaidIO


def test__export__calls_validate(
    validate_spy_net,
    mermaid_io: MermaidIO,
) -> None:
    # Adapter-boundary contract: export must validate before reading structure.
    mermaid_io.export(validate_spy_net)

    assert validate_spy_net.validate_was_called


def test__export__raises_for_invalid_raw_net(
    invalid_raw_net: KuripotNet,
    mermaid_io: MermaidIO,
) -> None:
    # Malformed raw/imported nets must fail before export.
    with pytest.raises(ValueError, match="unknown operator"):
        mermaid_io.export(invalid_raw_net)