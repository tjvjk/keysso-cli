"""Dashboard command tests for keysso CLI."""

from __future__ import annotations

import secrets
from typing import Any, Callable, Mapping

import pytest

from keysso_cli.cli import execute


@pytest.mark.parametrize(
    ("tail", "action", "with_domain", "with_keyword"),
    [
        (["domain"], "domain_dashboard", True, False),
        (["keyword"], "keyword_dashboard", False, True),
    ],
)
def test_cli_routes_dashboard_commands_to_expected_sdk_calls(
    tail: list[str],
    action: str,
    with_domain: bool,
    with_keyword: bool,
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
    """CLI cannot be trusted if dashboard route-to-method mapping changes."""
    stamp = secrets.token_hex(4)
    args = [
        "--api-key",
        f"токен-{stamp}",
        "dashboard",
        *tail,
        "--base",
        "msk",
    ]
    expected: dict[str, Any] = {"base": "msk"}
    if with_domain:
        domain = f"пример-{stamp}.рф"
        args.extend(["--domain", domain])
        expected["domain"] = domain
    if with_keyword:
        keyword = f"поисковая фраза {stamp}"
        args.extend(["--keyword", keyword])
        expected["keyword"] = keyword
    box = run_cli(args)
    assert box["calls"] == [(action, expected)], (
        "CLI unexpectedly does not map dashboard command arguments into SDK call parameters"
    )


def test_cli_cannot_fail_to_show_help_for_dashboard_commands() -> None:
    """Help output should still be reachable for dashboard commands."""
    with pytest.raises(SystemExit) as error:
        execute(["dashboard", "--help"])
    assert error.value.code == 0, (
        "CLI help output unexpectedly does not exit with success for dashboard command tree"
    )


@pytest.mark.parametrize(
    ("args", "tokens"),
    [
        (
            ["dashboard", "domain", "--help"],
            ("Поля ответа:", "aiAnswersCnt", "adkeyscnt", "history"),
        ),
        (
            ["dashboard", "keyword", "--help"],
            ("Поля ответа:", "word", "similar", "isquest"),
        ),
    ],
)
def test_cli_displays_dashboard_field_descriptions_in_help(
    args: list[str],
    tokens: tuple[str, ...],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Dashboard command help cannot miss response field descriptions."""
    with pytest.raises(SystemExit):
        execute(args)
    output = capsys.readouterr().out
    assert all(token in output for token in tokens), (
        "CLI help unexpectedly does not show field description glossary for the selected dashboard command"
    )


@pytest.mark.e2e
def test_cli_e2e_dashboard_domain_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live dashboard domain command cannot fail."""
    payload = run_live(
        [
            "dashboard",
            "domain",
            "--domain",
            e2e_case["domain"],
            "--base",
            e2e_case["base"],
        ],
        e2e_case["env"],
    )
    assert "id" in payload and isinstance(payload.get("name"), str), (
        "Live dashboard domain unexpectedly returns invalid payload"
    )


@pytest.mark.e2e
def test_cli_e2e_dashboard_keyword_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live dashboard keyword command cannot fail."""
    payload = run_live(
        [
            "dashboard",
            "keyword",
            "--keyword",
            e2e_case["keyword"],
            "--base",
            e2e_case["base"],
        ],
        e2e_case["env"],
    )
    assert "id" in payload and isinstance(payload.get("word"), str), (
        "Live dashboard keyword unexpectedly returns invalid payload"
    )
