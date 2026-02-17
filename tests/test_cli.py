"""Tests for the keysso CLI module."""

from __future__ import annotations

import io
import json
import secrets
from contextlib import contextmanager, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator

import pytest

from keysso_cli.cli import execute


def make_factory() -> tuple[dict[str, Any], Any]:
    """Create a fake SDK client factory and a capture box."""
    box: dict[str, Any] = {"calls": [], "kwargs": {}}
    calls: list[tuple[str, dict[str, Any]]] = []

    def make_method(name: str) -> Any:
        """Create one fake SDK method."""

        def call(**kwargs: Any) -> Any:
            """Capture one method call."""
            calls.append((name, kwargs))
            payload = {"action": name, "kwargs": kwargs}
            return SimpleNamespace(to_json=lambda indent=2: json.dumps(payload, ensure_ascii=False, indent=indent))

        return call

    context = SimpleNamespace(
        retrieve_concurents=make_method("concurents"),
        keywords=SimpleNamespace(
            list=make_method("keywords.list"),
            retrieve_byads=make_method("keywords.byads"),
        ),
        ads=SimpleNamespace(
            retrieve=make_method("ads.retrieve"),
            retrieve_links=make_method("ads.links"),
            retrieve_facts=make_method("ads.facts"),
        ),
    )
    direct = SimpleNamespace(
        retrieve_domain=make_method("direct.domain"),
        retrieve_ads=make_method("direct.ads"),
    )
    report = SimpleNamespace(simple=SimpleNamespace(context=context, direct=direct))

    @contextmanager
    def factory(**kwargs: Any) -> Iterator[Any]:
        """Yield one fake SDK client."""
        box["kwargs"] = kwargs
        box["calls"] = calls
        yield SimpleNamespace(report=report)

    return box, factory


def run_cli(args: list[str]) -> dict[str, Any]:
    """Run CLI with a fake client and return captured data."""
    box, factory = make_factory()
    stream = io.StringIO()
    with redirect_stdout(stream):
        execute(args, client_factory=factory)
    box["stdout"] = stream.getvalue()
    return box


def test_openapi_schema_contains_supported_paths_used_by_cli() -> None:
    """CLI tests cannot stay relevant if OpenAPI paths are removed."""
    schema = json.loads((Path(__file__).resolve().parents[1] / "openapi.json").read_text(encoding="utf-8"))
    supported = {
        "/report/simple/context/concurents",
        "/report/simple/context/keywords",
        "/report/simple/context/keywords/byads",
        "/report/simple/context/ads/",
        "/report/simple/context/ads/links",
        "/report/simple/context/ads/facts",
        "/report/simple/direct/domain",
        "/report/simple/direct/ads",
    }
    assert supported.issubset(set(schema["paths"].keys())), "OpenAPI schema unexpectedly does not keep supported CLI paths"


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
    assert box["calls"] == [(action, expected)], "CLI unexpectedly does not map context command arguments into SDK call parameters"


@pytest.mark.parametrize(
    ("tail", "action", "with_domain", "with_kid"),
    [
        (["domain"], "direct.domain", True, False),
        (["ads"], "direct.ads", False, True),
    ],
)
def test_cli_routes_direct_commands_to_expected_sdk_calls(
    tail: list[str],
    action: str,
    with_domain: bool,
    with_kid: bool,
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
    box = run_cli(args)
    assert box["calls"] == [(action, expected)], "CLI unexpectedly does not map direct command arguments into SDK call parameters"


def test_cli_passes_client_options_to_sdk_factory() -> None:
    """SDK client options cannot drift from CLI arguments."""
    stamp = secrets.token_hex(4)
    box = run_cli(
        [
            "--api-key",
            f"токен-{stamp}",
            "--base-url",
            f"http://127.0.0.1:{int(stamp[:4], 16)}",
            "context",
            "concurents",
            "--domain",
            f"домен-{stamp}.рф",
        ]
    )
    assert box["kwargs"] == {"api_key": f"токен-{stamp}", "base_url": f"http://127.0.0.1:{int(stamp[:4], 16)}"}, "CLI does not pass explicit client options into SDK factory"


def test_cli_cannot_fail_to_show_help_for_context_ads() -> None:
    """Help output should still be reachable for nested ads commands."""
    with pytest.raises(SystemExit) as error:
        execute(["context", "ads", "--help"])
    assert error.value.code == 0, "CLI help output unexpectedly does not exit with success"


def test_cli_cannot_fail_to_show_help_for_direct_commands() -> None:
    """Help output should still be reachable for direct commands."""
    with pytest.raises(SystemExit) as error:
        execute(["direct", "--help"])
    assert error.value.code == 0, "CLI help output unexpectedly does not exit with success for direct command tree"


def test_cli_displays_help_in_russian_for_context_level(capsys: pytest.CaptureFixture[str]) -> None:
    """Help output cannot remain partially English."""
    with pytest.raises(SystemExit):
        execute(["context", "--help"])
    output = capsys.readouterr().out
    assert "использование:" in output and "позиционные аргументы:" in output and "опции:" in output, "CLI help unexpectedly is not translated to Russian"


@pytest.mark.parametrize(
    ("args", "tokens"),
    [
        (["context", "concurents", "--help"], ("Поля ответа:", "pagesinindex", "adkeyscnt", "theme")),
        (["context", "keywords", "list", "--help"], ("Поля ответа:", "word", "serpf", "aid")),
        (["context", "keywords", "byads", "--help"], ("Поля ответа:", "word", "superwsk", "serp")),
        (["context", "ads", "retrieve", "--help"], ("Поля ответа:", "keyscnt", "legal", "links")),
        (["context", "ads", "links", "--help"], ("Поля ответа:", "links", "data", "total")),
        (["context", "ads", "facts", "--help"], ("Поля ответа:", "facts", "data", "total")),
        (["direct", "domain", "--help"], ("Поля ответа:", "keys_count", "updated_at", "uuid")),
        (["direct", "ads", "--help"], ("Поля ответа:", "keys_count", "updated_at", "uuid")),
    ],
)
def test_cli_displays_field_descriptions_in_help_for_each_command(
    args: list[str],
    tokens: tuple[str, ...],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Command help cannot miss response field descriptions."""
    with pytest.raises(SystemExit):
        execute(args)
    output = capsys.readouterr().out
    assert all(token in output for token in tokens), "CLI help unexpectedly does not show field description glossary for the selected command"


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
    skill_text = skill_file.read_text(encoding="utf-8")
    reference_text = reference.read_text(encoding="utf-8")
    expected = {
        str(skill_file),
        str(reference),
    }
    assert (
        payload["status"] == "ok"
        and payload["path"] == str(skill)
        and set(payload["files"]) == expected
        and skill_file.exists()
        and reference.exists()
        and "keysso-cli direct domain --domain <домен>" in skill_text
        and "keysso-cli direct ads --kid <id>" in skill_text
        and "keysso-cli direct domain --domain пример.рф --base msk --page 1 --per-page 25" in reference_text
        and "keysso-cli direct ads --kid 17222067 --base msk --page 1 --per-page 25" in reference_text
    ), "Install command unexpectedly does not create the expected skill files in current directory"


def test_cli_install_cannot_run_without_skills_flag() -> None:
    """Install command cannot accept execution without explicit target flag."""
    with pytest.raises(SystemExit) as error:
        execute(["install"], env={})
    assert error.value.code == 2, "Install command unexpectedly does not fail without --skills"
