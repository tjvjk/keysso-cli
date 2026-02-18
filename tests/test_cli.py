"""Top-level CLI behavior tests for keysso CLI."""

from __future__ import annotations

import io
import json
import sys

import pytest

from keysso_cli.cli import emit, execute, main


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


def test_cli_emit_cannot_break_when_model_to_json_fails() -> None:
    """Emit cannot fail if SDK model JSON serialization raises."""

    class BrokenPayload:
        def to_json(self, indent: int = 2, warnings: bool = False) -> str:
            raise RuntimeError("broken serializer")

        def to_dict(
            self,
            mode: str = "json",
            warnings: bool = False,
        ) -> dict[str, str]:
            return {"status": "ok"}

    stream = io.StringIO()
    emit(BrokenPayload(), stream)
    assert json.loads(stream.getvalue()) == {"status": "ok"}, (
        "Emit unexpectedly does not fallback to dictionary rendering when model JSON serialization fails"
    )
