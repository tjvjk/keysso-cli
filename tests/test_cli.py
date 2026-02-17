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
    report = SimpleNamespace(simple=SimpleNamespace(context=context))

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


def test_openapi_schema_contains_context_paths_used_by_cli() -> None:
    """CLI tests cannot stay relevant if OpenAPI paths are removed."""
    schema = json.loads((Path(__file__).resolve().parents[1] / "openapi.json").read_text(encoding="utf-8"))
    supported = {
        "/report/simple/context/concurents",
        "/report/simple/context/keywords",
        "/report/simple/context/keywords/byads",
        "/report/simple/context/ads/",
        "/report/simple/context/ads/links",
        "/report/simple/context/ads/facts",
    }
    assert supported.issubset(set(schema["paths"].keys())), "OpenAPI schema unexpectedly does not keep supported context paths"


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
