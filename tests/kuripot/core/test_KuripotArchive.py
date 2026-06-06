# tests/kuripot/core/test_KuripotArchive.py

from __future__ import annotations

from kuripot.core.archive import KuripotArchive


def test__init__with_archive_id() -> None:
    # An archive is created with a stable archive identifier.
    # The identifier names the state container, not the tokens inside it.
    archive = KuripotArchive(archive_id="state_archive")

    assert archive.archive_id == "state_archive"