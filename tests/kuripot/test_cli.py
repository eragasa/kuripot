# tests/kuripot/test_cli.py

from __future__ import annotations

from kuripot.cli import main


def test__main__prints_package_name(capsys) -> None:
    # The CLI entry point should run and print a minimal package identifier.
    main()

    captured = capsys.readouterr()

    assert captured.out == "kuripot\n"
    assert captured.err == ""