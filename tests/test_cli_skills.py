"""Skill installation command tests for keysso CLI."""

from __future__ import annotations

from typing import Any

import pytest

from keysso_cli.cli import execute


def test_cli_install_skills_reports_written_paths_in_payload(
    installed_skill_bundle: dict[str, Any],
) -> None:
    """Install command cannot skip payload metadata for generated files."""
    payload = installed_skill_bundle["payload"]
    skill = installed_skill_bundle["skill"]
    skill_file = installed_skill_bundle["skill_file"]
    reference = installed_skill_bundle["reference"]
    dashboard = installed_skill_bundle["dashboard"]
    expected = {str(skill_file), str(dashboard), str(reference)}
    assert (
        payload["status"] == "ok"
        and payload["path"] == str(skill)
        and set(payload["files"]) == expected
    ), "Install command unexpectedly reports invalid payload for generated skill files"


def test_cli_install_skills_creates_expected_files(
    installed_skill_bundle: dict[str, Any],
) -> None:
    """Install command cannot skip writing any required skill file."""
    skill_file = installed_skill_bundle["skill_file"]
    reference = installed_skill_bundle["reference"]
    dashboard = installed_skill_bundle["dashboard"]
    assert skill_file.exists() and dashboard.exists() and reference.exists(), (
        "Install command unexpectedly does not create the expected skill files in current directory"
    )


def test_cli_install_skills_writes_dashboard_and_direct_commands_to_skill_template(
    installed_skill_bundle: dict[str, Any],
) -> None:
    """Skill template cannot miss command cheatsheet rows."""
    skill_text = installed_skill_bundle["skill_file"].read_text(encoding="utf-8")
    assert (
        "keysso-cli dashboard domain --domain <домен>" in skill_text
        and "keysso-cli dashboard keyword --keyword <фраза>" in skill_text
        and "keysso-cli direct domain --domain <домен>" in skill_text
        and "keysso-cli direct ads --kid <id>" in skill_text
        and "keysso-cli direct ads --keyword <фраза>" in skill_text
    ), (
        "Install command unexpectedly does not include required command lines in SKILL.md"
    )


def test_cli_install_skills_writes_dashboard_reference_examples_and_fields(
    installed_skill_bundle: dict[str, Any],
) -> None:
    """Dashboard reference cannot miss examples and field glossary."""
    dashboard_text = installed_skill_bundle["dashboard"].read_text(encoding="utf-8")
    assert (
        "keysso-cli dashboard domain --domain пример.рф --base msk" in dashboard_text
        and 'keysso-cli dashboard keyword --keyword "пластиковые окна" --base msk'
        in dashboard_text
        and "aiAnswersCnt" in dashboard_text
        and "aiState" in dashboard_text
        and "adkeyscnt" in dashboard_text
        and "similar" in dashboard_text
        and "isquest" in dashboard_text
    ), (
        "Install command unexpectedly does not include dashboard docs in dashboard reference"
    )


def test_cli_install_skills_keeps_dashboard_examples_out_of_context_reference(
    installed_skill_bundle: dict[str, Any],
) -> None:
    """Context reference cannot include dashboard command examples."""
    reference_text = installed_skill_bundle["reference"].read_text(encoding="utf-8")
    assert (
        "keysso-cli dashboard domain --domain пример.рф --base msk"
        not in reference_text
        and 'keysso-cli dashboard keyword --keyword "пластиковые окна" --base msk'
        not in reference_text
    ), (
        "Install command unexpectedly mixes dashboard examples into context/direct reference"
    )


def test_cli_install_skills_writes_direct_examples_and_field_docs_to_context_reference(
    installed_skill_bundle: dict[str, Any],
) -> None:
    """Context reference cannot miss direct examples and response field descriptions."""
    reference_text = installed_skill_bundle["reference"].read_text(encoding="utf-8")
    assert (
        "keysso-cli direct domain --domain пример.рф --base msk --page 1 --per-page 25"
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
        "Install command unexpectedly does not include context/direct docs in context reference"
    )


def test_cli_install_cannot_run_without_skills_flag() -> None:
    """Install command cannot accept execution without explicit target flag."""
    with pytest.raises(SystemExit) as error:
        execute(["install"], env={})
    assert error.value.code == 2, (
        "Install command unexpectedly does not fail without --skills"
    )
