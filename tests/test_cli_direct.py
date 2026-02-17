"""Direct command tests for keysso CLI."""

from __future__ import annotations

import secrets
from typing import Any, Callable, Mapping

import pytest

from keysso_cli.cli import execute


@pytest.mark.parametrize(
    ("tail", "action", "with_domain", "with_kid", "with_keyword"),
    [
        (["domain"], "direct.domain", True, False, False),
        (["ads"], "direct.ads", False, True, False),
        (["ads"], "direct.ads", False, False, True),
    ],
)
def test_cli_routes_direct_commands_to_expected_sdk_calls(
    tail: list[str],
    action: str,
    with_domain: bool,
    with_kid: bool,
    with_keyword: bool,
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
    """CLI cannot be trusted if direct route-to-method mapping changes."""
    stamp = secrets.token_hex(4)
    query = f"direct:{stamp}"
    args = [
        "--api-key",
        f"токен-{stamp}",
        "direct",
        *tail,
        "--base",
        "msk",
        "--filter",
        query,
        "--page",
        "3",
        "--per-page",
        "9",
        "--sort",
        "keys_count|desc",
    ]
    expected: dict[str, Any] = {
        "base": "msk",
        "filter": query,
        "page": 3,
        "per_page": 9,
        "sort": "keys_count|desc",
    }
    if with_domain:
        domain = f"пример-{stamp}.рф"
        args.extend(["--domain", domain])
        expected["domain"] = domain
    if with_kid:
        kid = int(stamp[:6], 16)
        args.extend(["--kid", str(kid)])
        expected["kid"] = kid
    if with_keyword:
        keyword = f"поисковая фраза {stamp}"
        args.extend(["--keyword", keyword])
        expected["kid"] = 17222067
    box = run_cli(args)
    if with_keyword:
        expected_calls = [
            ("keyword_dashboard", {"keyword": keyword, "base": "msk"}),
            (action, expected),
        ]
    else:
        expected_calls = [(action, expected)]
    assert box["calls"] == expected_calls, (
        "CLI unexpectedly does not map direct command arguments into SDK call parameters"
    )


def test_cli_cannot_fail_to_show_help_for_direct_commands() -> None:
    """Help output should still be reachable for direct commands."""
    with pytest.raises(SystemExit) as error:
        execute(["direct", "--help"])
    assert error.value.code == 0, (
        "CLI help output unexpectedly does not exit with success for direct command tree"
    )


def test_cli_displays_keyword_option_for_direct_ads(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Direct ads help cannot miss the keyword lookup option."""
    with pytest.raises(SystemExit):
        execute(["direct", "ads", "--help"])
    output = capsys.readouterr().out
    assert "--keyword" in output and "--kid" in output, (
        "Direct ads help unexpectedly does not show both kid and keyword options"
    )


@pytest.mark.parametrize(
    ("args", "tokens"),
    [
        (
            ["direct", "domain", "--help"],
            ("Поля ответа:", "keys_count", "updated_at", "uuid"),
        ),
        (
            ["direct", "ads", "--help"],
            ("Поля ответа:", "keys_count", "updated_at", "uuid"),
        ),
    ],
)
def test_cli_displays_direct_field_descriptions_in_help(
    args: list[str],
    tokens: tuple[str, ...],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Direct command help cannot miss response field descriptions."""
    with pytest.raises(SystemExit):
        execute(args)
    output = capsys.readouterr().out
    assert all(token in output for token in tokens), (
        "CLI help unexpectedly does not show field description glossary for the selected direct command"
    )


@pytest.mark.e2e
def test_cli_e2e_direct_domain_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live direct domain command cannot fail."""
    payload = run_live(
        [
            "direct",
            "domain",
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
        "Live direct domain unexpectedly returns invalid payload"
    )


@pytest.mark.e2e
def test_cli_e2e_direct_ads_without_mocks(
    e2e_case: dict[str, Any],
    run_live: Callable[[list[str], Mapping[str, str]], dict[str, Any]],
) -> None:
    """Live direct ads command cannot fail."""
    payload = run_live(
        [
            "direct",
            "ads",
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
        "Live direct ads unexpectedly returns invalid payload"
    )
