"""Dashboard command tree and SDK routing."""

from __future__ import annotations

import argparse
from typing import Any

from keysso_cli.query import add_base_option, add_domain_option

DASHBOARD_DOMAIN_FIELDS = """Поля ответа:
  id            — идентификатор домена
  name          — имя домена
  dr            — рейтинг домена
  childsCount   — количество поддоменов
  it1           — запросов в топ-1
  it3           — запросов в топ-3
  it5           — запросов в топ-5
  it10          — запросов в топ-10
  it50          — запросов в топ-50
  vis           — оценка органического трафика
  adtraf        — оценка трафика из контекста
  adcost        — оценка бюджета контекста
  adscnt        — количество объявлений в контексте
  adkeyscnt     — количество запросов в контексте
  history       — история изменения метрик
  aiAnswersCnt  — упоминания в ИИ-ответах
  aiState       — статус ИИ-отчета"""


DASHBOARD_KEYWORD_FIELDS = """Поля ответа:
  id       — идентификатор ключевой фразы
  word     — ключевая фраза
  ws       — базовая частотность
  wsk      — очень точная частотность
  isgeo    — является топонимом
  isquest  — является вопросом
  top      — топ доменов в органике
  ads      — объявления в контексте
  similar  — дополняющие фразы"""


def add_domain_parser(dashboard_commands: Any) -> None:
    """Attach the dashboard domain parser."""
    parser = dashboard_commands.add_parser(
        "domain",
        help="Дашборд домена",
        description="Сводные данные по домену",
        epilog=DASHBOARD_DOMAIN_FIELDS,
    )
    add_domain_option(parser)
    add_base_option(parser)
    parser.set_defaults(action="dashboard.domain")


def add_keyword_parser(dashboard_commands: Any) -> None:
    """Attach the dashboard keyword parser."""
    parser = dashboard_commands.add_parser(
        "keyword",
        help="Дашборд ключевой фразы",
        description="Сводные данные по ключевой фразе",
        epilog=DASHBOARD_KEYWORD_FIELDS,
    )
    parser.add_argument("--keyword", required=True, help="Поисковая фраза")
    add_base_option(parser)
    parser.set_defaults(action="dashboard.keyword")


def add_parser(commands: Any) -> None:
    """Attach the dashboard parser tree."""
    parser = commands.add_parser("dashboard", help="Дашборды домена и ключевой фразы")
    dashboard_commands = parser.add_subparsers(dest="dashboard_command", required=True)
    add_domain_parser(dashboard_commands)
    add_keyword_parser(dashboard_commands)


def invoke(client: Any, args: argparse.Namespace) -> Any:
    """Route parsed dashboard arguments to one SDK call."""
    simple = client.report.simple
    if args.action == "dashboard.domain":
        payload: dict[str, Any] = {"domain": args.domain}
        if args.base is not None:
            payload["base"] = args.base
        return simple.retrieve_domain_dashboard(**payload)
    if args.action == "dashboard.keyword":
        payload = {"keyword": args.keyword}
        if args.base is not None:
            payload["base"] = args.base
        return simple.retrieve_keyword_dashboard(**payload)
    raise ValueError(f"Unsupported action: {args.action}")
