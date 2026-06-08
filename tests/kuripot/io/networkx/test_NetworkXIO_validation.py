# tests/kuripot/io/networkx/test_NetworkXIO_validation.py

from __future__ import annotations

import pytest

from kuripot.core.net import KuripotNet
from kuripot.io.io_networkx import NetworkXIO


def test__export__calls_validate(
    validate_spy_net,
    networkx_io: NetworkXIO,
) -> None:
    # NetworkXIO validates the semantic net before export.
    networkx_io.export(validate_spy_net)

    assert validate_spy_net.validate_was_called


def test__export__raises_for_invalid_raw_net(
    invalid_raw_net: KuripotNet,
    networkx_io: NetworkXIO,
) -> None:
    # NetworkXIO validates the semantic net before export.
    # This protects imported, deserialized, or manually modified nets.
    with pytest.raises(ValueError, match="unknown operator"):
        networkx_io.export(invalid_raw_net)