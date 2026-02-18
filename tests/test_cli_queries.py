"""Shared query and schema tests for keysso CLI."""

from __future__ import annotations

import json
import secrets
from pathlib import Path
from typing import Any, Callable


def test_openapi_schema_contains_supported_paths_used_by_cli() -> None:
    """CLI tests cannot stay relevant if OpenAPI paths are removed."""
    schema = json.loads(
        (Path(__file__).resolve().parents[1] / "openapi.json").read_text(
            encoding="utf-8"
        )
    )
    supported = {
        "/report/simple/domain_dashboard",
        "/report/simple/keyword_dashboard",
        "/report/simple/context/concurents",
        "/report/simple/context/keywords",
        "/report/simple/context/keywords/byads",
        "/report/simple/context/ads/",
        "/report/simple/context/ads/links",
        "/report/simple/context/ads/facts",
        "/report/simple/direct/domain",
        "/report/simple/direct/ads",
    }
    assert supported.issubset(set(schema["paths"].keys())), (
        "OpenAPI schema unexpectedly does not keep supported CLI paths"
    )


def test_cli_passes_client_options_to_sdk_factory(
    run_cli: Callable[[list[str]], dict[str, Any]],
) -> None:
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
    assert box["kwargs"] == {
        "api_key": f"токен-{stamp}",
        "base_url": f"http://127.0.0.1:{int(stamp[:4], 16)}",
    }, "CLI does not pass explicit client options into SDK factory"
