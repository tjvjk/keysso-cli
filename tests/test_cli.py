"""Top-level CLI behavior tests for keysso CLI."""

from __future__ import annotations

import sys

import pytest

from keysso_cli.cli import execute, main


def test_cli_displays_help_in_russian_for_root_level(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Root help output cannot remain partially English."""
    with pytest.raises(SystemExit):
        execute(["--help"])
    output = capsys.readouterr().out
    assert (
        "использование:" in output
        and "позиционные аргументы:" in output
        and "опции:" in output
    ), "CLI root help unexpectedly is not translated to Russian"


def test_cli_cannot_run_api_commands_without_api_key() -> None:
    """Report commands cannot run without explicit API key source."""
    with pytest.raises(SystemExit) as error:
        execute(["context", "concurents", "--domain", "пример.рф"], env={})
    assert error.value.code == 2, (
        "CLI unexpectedly allows report command execution without API key"
    )


def test_cli_main_exits_with_success_for_install_skills(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    """Main entrypoint cannot skip wrapping execution in SystemExit."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["keysso-cli", "install", "--skills"])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 0, (
        "CLI main entrypoint unexpectedly does not return success for install command"
    )
