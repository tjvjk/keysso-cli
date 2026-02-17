"""Shared argument helpers for report commands."""

from __future__ import annotations

import argparse
from typing import Any


def add_query_options(parser: argparse.ArgumentParser) -> None:
    """Attach shared query options."""
    parser.add_argument("--base", help="Региональная база")
    parser.add_argument("--filter", help="Фильтр запроса")
    parser.add_argument("--page", type=int, help="Номер страницы")
    parser.add_argument("--per-page", dest="per_page", type=int, help="Размер страницы")
    parser.add_argument("--sort", help="Параметр сортировки")


def add_domain_option(parser: argparse.ArgumentParser) -> None:
    """Attach required domain option."""
    parser.add_argument("--domain", required=True, help="Имя домена")


def collect_query(args: argparse.Namespace) -> dict[str, Any]:
    """Collect shared query options from parsed arguments."""
    query: dict[str, Any] = {}
    for key in ("base", "filter", "page", "per_page", "sort"):
        value = getattr(args, key, None)
        if value is not None:
            query[key] = value
    return query
