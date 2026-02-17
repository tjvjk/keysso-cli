"""Direct command tree and SDK routing."""

from __future__ import annotations

import argparse
from typing import Any

from keysso_cli.query import add_domain_option, add_query_options, collect_query

DIRECT_DOMAIN_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив объявлений
  description   — текст объявления
  domain        — домен объявления
  keys_count    — количество запросов по объявлению
  link          — ссылка на посадочную страницу
  regions       — регионы показа
  title         — заголовок объявления
  updated_at    — дата обновления данных
  uuid          — идентификатор объявления"""


DIRECT_ADS_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив объявлений
  description   — текст объявления
  domain        — домен объявления
  keys_count    — количество запросов по объявлению
  link          — ссылка на посадочную страницу
  regions       — регионы показа
  title         — заголовок объявления
  updated_at    — дата обновления данных
  uuid          — идентификатор объявления"""


def add_domain_parser(direct_commands: Any) -> None:
    """Attach the direct domain parser."""
    parser = direct_commands.add_parser(
        "domain",
        help="Объявления Яндекс Директ по домену",
        description="Список объявлений Яндекс Директ по домену",
        epilog=DIRECT_DOMAIN_FIELDS,
    )
    add_domain_option(parser)
    add_query_options(parser)
    parser.set_defaults(action="direct.domain")


def add_ads_parser(direct_commands: Any) -> None:
    """Attach the direct ads parser."""
    parser = direct_commands.add_parser(
        "ads",
        help="Объявления Яндекс Директ по идентификатору или поисковой фразе",
        description="Список объявлений Яндекс Директ по идентификатору или поисковой фразе",
        epilog=DIRECT_ADS_FIELDS,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--kid", type=int, help="Идентификатор фразы")
    group.add_argument(
        "--keyword", help="Поисковая фраза для автоматического поиска идентификатора"
    )
    add_query_options(parser)
    parser.set_defaults(action="direct.ads")


def add_parser(commands: Any) -> None:
    """Attach the direct parser tree."""
    parser = commands.add_parser("direct", help="Отчеты по объявлениям Яндекс Директ")
    direct_commands = parser.add_subparsers(dest="direct_command", required=True)
    add_domain_parser(direct_commands)
    add_ads_parser(direct_commands)


def invoke(client: Any, args: argparse.Namespace) -> Any:
    """Route parsed direct arguments to one SDK call."""
    direct = client.report.simple.direct
    simple = client.report.simple
    query = collect_query(args)
    if args.action == "direct.domain":
        return direct.retrieve_domain(domain=args.domain, **query)
    if args.action == "direct.ads":
        kid = args.kid
        if kid is None:
            payload: dict[str, Any] = {"keyword": args.keyword}
            if "base" in query:
                payload["base"] = query["base"]
            dashboard = simple.retrieve_keyword_dashboard(**payload)
            kid = dashboard.id
        if kid is None:
            raise ValueError(
                f"Keyword lookup returned empty identifier for keyword: {args.keyword}"
            )
        return direct.retrieve_ads(kid=int(kid), **query)
    raise ValueError(f"Unsupported action: {args.action}")
