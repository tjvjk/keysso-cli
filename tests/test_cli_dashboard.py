"""Dashboard command tests for keysso CLI."""

from __future__ import annotations

import secrets
from typing import Any, Callable, Mapping

import pytest

from keysso_cli.cli import execute


def test_cli_routes_dashboard_domain_command_to_expected_sdk_call(
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
    """CLI cannot be trusted if dashboard domain route-to-method mapping changes."""
    stamp = secrets.token_hex(4)
    domain = f"пример-{stamp}.рф"
    box = run_cli(
        [
            "--api-key",
            f"токен-{stamp}",
            "dashboard",
            "domain",
            "--domain",
            domain,
            "--base",
            "msk",
        ]
    )
    assert box["calls"] == [("domain_dashboard", {"domain": domain, "base": "msk"})], (
        "CLI unexpectedly does not map dashboard domain command arguments into SDK call parameters"
    )


def test_cli_routes_dashboard_keyword_command_to_expected_sdk_call(
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
    """CLI cannot be trusted if dashboard keyword route-to-method mapping changes."""
    stamp = secrets.token_hex(4)
    keyword = f"поисковая фраза {stamp}"
    box = run_cli(
        [
            "--api-key",
            f"токен-{stamp}",
            "dashboard",
            "keyword",
            "--keyword",
            keyword,
            "--base",
            "msk",
        ]
    )
    assert box["calls"] == [
        ("keyword_dashboard", {"keyword": keyword, "base": "msk"})
    ], (
        "CLI unexpectedly does not map dashboard keyword command arguments into SDK call parameters"
    )


def test_cli_routes_dashboard_ad_history_command_to_expected_sdk_call(
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
    """CLI cannot be trusted if dashboard ad-history route-to-method mapping changes."""
    stamp = secrets.token_hex(4)
    domain = f"пример-{stamp}.рф"
    box = run_cli(
        [
            "--api-key",
            f"токен-{stamp}",
            "dashboard",
            "ad-history",
            "--domain",
            domain,
            "--base",
            "msk",
        ]
    )
    assert box["calls"] == [("domain_ad_history", {"domain": domain, "base": "msk"})], (
        "CLI unexpectedly does not map dashboard ad-history command arguments into SDK call parameters"
    )


def test_cli_routes_dashboard_similarkeys_command_to_expected_sdk_call(
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
    """CLI cannot be trusted if dashboard similarkeys route-to-method mapping changes."""
    stamp = secrets.token_hex(4)
    keyword = f"поисковая фраза {stamp}"
    query = f"keyword:{stamp}"
    box = run_cli(
        [
            "--api-key",
            f"токен-{stamp}",
            "dashboard",
            "similarkeys",
            "--keyword",
            keyword,
            "--base",
            "msk",
            "--filter",
            query,
            "--page",
            "4",
            "--per-page",
            "12",
            "--sort",
            "wsk|asc",
        ]
    )
    assert box["calls"] == [
        (
            "similarkeys",
            {
                "keyword": keyword,
                "base": "msk",
                "filter": query,
                "page": 4,
                "per_page": 12,
                "sort": "wsk|asc",
            },
        )
    ], (
        "CLI unexpectedly does not map dashboard similarkeys command arguments into SDK call parameters"
    )


def test_cli_routes_dashboard_top_visibility_command_to_expected_sdk_call(
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
    """CLI cannot be trusted if dashboard top-visibility route-to-method mapping changes."""
    stamp = secrets.token_hex(4)
    domain = f"пример-{stamp}.рф"
    box = run_cli(
        [
            "--api-key",
            f"токен-{stamp}",
            "dashboard",
            "top-visibility",
            "--domain",
            domain,
            "--base",
            "msk",
            "--page",
            "8",
            "--per-page",
            "15",
            "--sort",
            "topvis|asc",
        ]
    )
    assert box["calls"] == [
        (
            "top_domain_visibility",
            {
                "domain": domain,
                "base": "msk",
                "page": 8,
                "per_page": 15,
                "sort": "topvis|asc",
            },
        )
    ], (
        "CLI unexpectedly does not map dashboard top-visibility command arguments into SDK call parameters"
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
        (
            ["dashboard", "ad-history", "--help"],
            ("Поля ответа:", "adCost", "adKeysCount", "adsCount"),
        ),
        (
            ["dashboard", "similarkeys", "--help"],
            ("Поля ответа:", "wizardscount", "kei", "current_page"),
        ),
        (
            ["dashboard", "top-visibility", "--help"],
            ("Поля ответа:", "topvis", "pagesinindex", "adkeyscnt"),
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


@pytest.mark.e2e
def test_cli_e2e_dashboard_ad_history_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live dashboard ad-history command cannot fail."""
    payload = run_live(
        [
            "dashboard",
            "ad-history",
            "--domain",
            e2e_case["domain"],
            "--base",
            e2e_case["base"],
        ],
        e2e_case["env"],
    )
    assert isinstance(payload, dict), (
        "Live dashboard ad-history unexpectedly returns invalid payload"
    )


@pytest.mark.e2e
def test_cli_e2e_dashboard_similarkeys_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live dashboard similarkeys command cannot fail."""
    payload = run_live(
        [
            "dashboard",
            "similarkeys",
            "--keyword",
            e2e_case["keyword"],
            "--base",
            e2e_case["base"],
            "--page",
            "1",
            "--per-page",
            "5",
        ],
        e2e_case["env"],
    )
    assert "data" in payload and isinstance(payload["data"], list), (
        "Live dashboard similarkeys unexpectedly returns invalid payload"
    )


@pytest.mark.e2e
def test_cli_e2e_dashboard_top_visibility_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live dashboard top-visibility command cannot fail."""
    payload = run_live(
        [
            "dashboard",
            "top-visibility",
            "--domain",
            e2e_case["domain"],
            "--base",
            e2e_case["base"],
            "--page",
            "1",
            "--per-page",
            "5",
        ],
        e2e_case["env"],
    )
    assert "data" in payload and isinstance(payload["data"], list), (
        "Live dashboard top-visibility unexpectedly returns invalid payload"
    )
