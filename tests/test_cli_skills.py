"""Skill installation command tests for keysso CLI."""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from keysso_cli.cli import execute


def test_cli_install_skills_creates_skill_files_in_current_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Install command cannot skip creating the skill bundle."""
    monkeypatch.chdir(tmp_path)
    stream = io.StringIO()
    execute(["install", "--skills"], env={}, stream=stream)
    payload = json.loads(stream.getvalue())
    skill = tmp_path / ".claude" / "skills" / "keysso-cli"
    skill_file = skill / "SKILL.md"
    reference = skill / "references" / "context-ads.md"
    dashboard = skill / "references" / "dashboard.md"
    skill_text = skill_file.read_text(encoding="utf-8")
    reference_text = reference.read_text(encoding="utf-8")
    dashboard_text = dashboard.read_text(encoding="utf-8")
    expected = {
        str(skill_file),
        str(dashboard),
        str(reference),
    }
    assert (
        payload["status"] == "ok"
        and payload["path"] == str(skill)
        and set(payload["files"]) == expected
        and skill_file.exists()
        and dashboard.exists()
        and reference.exists()
        and "keysso-cli dashboard domain --domain <домен>" in skill_text
        and "keysso-cli dashboard keyword --keyword <фраза>" in skill_text
        and "keysso-cli direct domain --domain <домен>" in skill_text
        and "keysso-cli direct ads --kid <id>" in skill_text
        and "keysso-cli direct ads --keyword <фраза>" in skill_text
        and "keysso-cli dashboard domain --domain пример.рф --base msk"
        in dashboard_text
        and 'keysso-cli dashboard keyword --keyword "пластиковые окна" --base msk'
        in dashboard_text
        and "aiAnswersCnt" in dashboard_text
        and "aiState" in dashboard_text
        and "adkeyscnt" in dashboard_text
        and "similar" in dashboard_text
        and "isquest" in dashboard_text
        and "keysso-cli dashboard domain --domain пример.рф --base msk"
        not in reference_text
        and 'keysso-cli dashboard keyword --keyword "пластиковые окна" --base msk'
        not in reference_text
        and "keysso-cli direct domain --domain пример.рф --base msk --page 1 --per-page 25"
        in reference_text
        and "keysso-cli direct ads --kid 17222067 --base msk --page 1 --per-page 25"
        in reference_text
        and 'keysso-cli direct ads --keyword "пластиковые окна" --base msk --page 1 --per-page 25'
        in reference_text
        and "Поля ответа API:" in reference_text
        and "data          — массив записей по конкурентам" in reference_text
        and "superwsk      — суперточная частотность" in reference_text
        and "keyscnt       — количество запросов" in reference_text
        and "keys_count    — количество запросов по объявлению" in reference_text
        and "updated_at    — дата обновления данных" in reference_text
        and "uuid          — идентификатор объявления" in reference_text
    ), (
        "Install command unexpectedly does not create the expected skill files in current directory"
    )


def test_cli_install_cannot_run_without_skills_flag() -> None:
    """Install command cannot accept execution without explicit target flag."""
    with pytest.raises(SystemExit) as error:
        execute(["install"], env={})
    assert error.value.code == 2, (
        "Install command unexpectedly does not fail without --skills"
    )
