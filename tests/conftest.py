"""Pytest hooks and shared fixtures for keysso-cli tests."""

from __future__ import annotations

import io
import json
import logging
import os
import time
from contextlib import contextmanager, redirect_stdout
from types import SimpleNamespace
from typing import Any, Callable, Iterator, Mapping

import pytest

from keysso_cli.cli import execute


def pytest_configure() -> None:
    """Disable logging in tests."""
    logging.disable(logging.CRITICAL)


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
            return SimpleNamespace(
                to_json=lambda indent=2: json.dumps(
                    payload, ensure_ascii=False, indent=indent
                )
            )

        return call

    def dashboard_method(**kwargs: Any) -> Any:
        """Capture keyword dashboard lookup and return keyword payload."""
        calls.append(("keyword_dashboard", kwargs))
        payload = {
            "id": 17222067,
            "word": str(kwargs.get("keyword", "")),
        }
        return SimpleNamespace(
            id=payload["id"],
            to_json=lambda indent=2: json.dumps(
                payload, ensure_ascii=False, indent=indent
            ),
        )

    def domain_dashboard_method(**kwargs: Any) -> Any:
        """Capture domain dashboard lookup and return domain payload."""
        calls.append(("domain_dashboard", kwargs))
        payload = {
            "id": 29918348,
            "name": str(kwargs.get("domain", "")),
        }
        return SimpleNamespace(
            id=payload["id"],
            to_json=lambda indent=2: json.dumps(
                payload, ensure_ascii=False, indent=indent
            ),
        )

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
    report = SimpleNamespace(
        simple=SimpleNamespace(
            context=context,
            direct=direct,
            retrieve_domain_dashboard=domain_dashboard_method,
            retrieve_keyword_dashboard=dashboard_method,
        )
    )

    @contextmanager
    def factory(**kwargs: Any) -> Iterator[Any]:
        """Yield one fake SDK client."""
        box["kwargs"] = kwargs
        box["calls"] = calls
        yield SimpleNamespace(report=report)

    return box, factory


@pytest.fixture
def run_cli() -> Callable[[list[str]], dict[str, Any]]:
    """Provide one helper to run CLI with fake SDK client."""

    def run(args: list[str]) -> dict[str, Any]:
        """Run CLI once with fake dependencies."""
        box, factory = make_factory()
        stream = io.StringIO()
        with redirect_stdout(stream):
            execute(args, client_factory=factory)
        box["stdout"] = stream.getvalue()
        return box

    return run


def run_live_cli(
    args: list[str],
    env: Mapping[str, str],
    *,
    retries: int = 3,
) -> dict[str, Any]:
    """Run CLI against the live API and return parsed JSON."""
    error: Exception | None = None
    for index in range(retries):
        stream = io.StringIO()
        time.sleep(1.1)
        try:
            execute(args, env=env, stream=stream)
            return json.loads(stream.getvalue())
        except Exception as failure:
            error = failure
            if index + 1 < retries:
                time.sleep(float(index + 2))
    raise RuntimeError("Live API request failed after retries") from error


@pytest.fixture(scope="session")
def run_live() -> Callable[[list[str], Mapping[str, str]], dict[str, Any]]:
    """Provide one helper to run CLI against live API."""
    return run_live_cli


@pytest.fixture(scope="session")
def e2e_case() -> dict[str, Any]:
    """Prepare one live testing context for all e2e command checks."""
    if os.getenv("KEYSSO_RUN_E2E") != "1":
        pytest.skip("E2E tests are disabled; set KEYSSO_RUN_E2E=1")
    token = os.getenv("KEYSSO_API_KEY")
    if not token:
        pytest.skip("E2E tests require KEYSSO_API_KEY")
    env = {"KEYSSO_API_KEY": token}
    domain = os.getenv("KEYSSO_E2E_DOMAIN", "wildberries.ru")
    base = os.getenv("KEYSSO_E2E_BASE", "msk")
    keywords = run_live_cli(
        [
            "context",
            "keywords",
            "list",
            "--domain",
            domain,
            "--base",
            base,
            "--page",
            "1",
            "--per-page",
            "10",
        ],
        env,
    )
    rows = keywords.get("data", [])
    if not rows:
        pytest.skip("E2E seed command returned empty keyword list")
    row = next((item for item in rows if item.get("aid")), rows[0])
    ads = row.get("aid")
    keyword = os.getenv("KEYSSO_E2E_KEYWORD") or row.get("word")
    if ads is None:
        pytest.skip("E2E seed command did not return ads id")
    if not keyword:
        pytest.skip("E2E seed command did not return keyword")
    return {
        "env": env,
        "domain": domain,
        "base": base,
        "ads_id": str(ads),
        "keyword": str(keyword),
        "keywords_payload": keywords,
    }
