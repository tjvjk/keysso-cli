"""Context command tests for keysso CLI."""

from __future__ import annotations

import secrets
from typing import Any, Callable, Mapping

import pytest

from keysso_cli.cli import execute


@pytest.mark.parametrize(
    ("tail", "action", "with_ads_id", "with_full"),
    [
        (["concurents"], "concurents", False, False),
        (["keywords", "list"], "keywords.list", False, False),
        (["keywords", "byads"], "keywords.byads", True, False),
        (["ads", "retrieve"], "ads.retrieve", False, True),
        (["ads", "links"], "ads.links", False, False),
        (["ads", "facts"], "ads.facts", False, False),
    ],
)
def test_cli_routes_context_commands_to_expected_sdk_calls(
    tail: list[str],
    action: str,
    with_ads_id: bool,
    with_full: bool,
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
    """CLI cannot be trusted if route-to-method mapping changes."""
    stamp = secrets.token_hex(4)
    domain = f"пример-{stamp}.рф"
    query = f"ключ:{stamp}"
    args = [
        "--api-key",
        f"токен-{stamp}",
        "context",
        *tail,
        "--domain",
        domain,
        "--base",
        "msk",
        "--filter",
        query,
        "--page",
        "7",
        "--per-page",
        "11",
        "--sort",
        "cnt|desc",
    ]
    expected: dict[str, Any] = {
        "domain": domain,
        "base": "msk",
        "filter": query,
        "page": 7,
        "per_page": 11,
        "sort": "cnt|desc",
    }
    if with_ads_id:
        ads = f"объявление-{stamp}"
        args.extend(["--ads-id", ads])
        expected["ads_id"] = ads
    if with_full:
        args.append("--full")
        expected["full"] = True
    box = run_cli(args)
    assert box["calls"] == [(action, expected)], (
        "CLI unexpectedly does not map context command arguments into SDK call parameters"
    )


def test_cli_cannot_fail_to_show_help_for_context_ads() -> None:
    """Help output should still be reachable for nested ads commands."""
    with pytest.raises(SystemExit) as error:
        execute(["context", "ads", "--help"])
    assert error.value.code == 0, (
        "CLI help output unexpectedly does not exit with success"
    )


def test_cli_displays_help_in_russian_for_context_level(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Help output cannot remain partially English."""
    with pytest.raises(SystemExit):
        execute(["context", "--help"])
    output = capsys.readouterr().out
    assert (
        "использование:" in output
        and "позиционные аргументы:" in output
        and "опции:" in output
    ), "CLI help unexpectedly is not translated to Russian"


@pytest.mark.parametrize(
    ("args", "tokens"),
    [
        (
            ["context", "concurents", "--help"],
            ("Поля ответа:", "pagesinindex", "adkeyscnt", "theme"),
        ),
        (
            ["context", "keywords", "list", "--help"],
            ("Поля ответа:", "word", "serpf", "aid"),
        ),
        (
            ["context", "keywords", "byads", "--help"],
            ("Поля ответа:", "word", "superwsk", "serp"),
        ),
        (
            ["context", "ads", "retrieve", "--help"],
            ("Поля ответа:", "keyscnt", "legal", "links"),
        ),
        (
            ["context", "ads", "links", "--help"],
            ("Поля ответа:", "links", "data", "total"),
        ),
        (
            ["context", "ads", "facts", "--help"],
            ("Поля ответа:", "facts", "data", "total"),
        ),
    ],
)
def test_cli_displays_context_field_descriptions_in_help(
    args: list[str],
    tokens: tuple[str, ...],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Context command help cannot miss response field descriptions."""
    with pytest.raises(SystemExit):
        execute(args)
    output = capsys.readouterr().out
    assert all(token in output for token in tokens), (
        "CLI help unexpectedly does not show field description glossary for the selected context command"
    )


@pytest.mark.e2e
def test_cli_e2e_context_keywords_list_without_mocks(
    e2e_case: dict[str, Any],
) -> None:
    """Live context keywords command cannot return malformed data."""
    payload = e2e_case["keywords_payload"]
    assert "data" in payload and payload["data"], (
        "Live context keywords list unexpectedly returns empty data"
    )


@pytest.mark.e2e
def test_cli_e2e_context_concurents_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live context concurents command cannot fail."""
    payload = run_live(
        [
            "context",
            "concurents",
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
        "Live context concurents unexpectedly returns invalid payload"
    )


@pytest.mark.e2e
def test_cli_e2e_context_keywords_byads_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live context keywords byads command cannot fail."""
    payload = run_live(
        [
            "context",
            "keywords",
            "byads",
            "--domain",
            e2e_case["domain"],
            "--ads-id",
            e2e_case["ads_id"],
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
        "Live context keywords byads unexpectedly returns invalid payload"
    )


@pytest.mark.e2e
def test_cli_e2e_context_ads_retrieve_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live context ads retrieve command cannot fail."""
    payload = run_live(
        [
            "context",
            "ads",
            "retrieve",
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
        "Live context ads retrieve unexpectedly returns invalid payload"
    )


@pytest.mark.e2e
def test_cli_e2e_context_ads_links_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live context ads links command cannot fail."""
    payload = run_live(
        [
            "context",
            "ads",
            "links",
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
        "Live context ads links unexpectedly returns invalid payload"
    )


@pytest.mark.e2e
def test_cli_e2e_context_ads_facts_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live context ads facts command cannot fail."""
    payload = run_live(
        [
            "context",
            "ads",
            "facts",
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
        "Live context ads facts unexpectedly returns invalid payload"
    )
