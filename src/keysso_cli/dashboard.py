"""Dashboard command tree and SDK routing."""

from __future__ import annotations

import argparse
from typing import Any

from keysso_cli.query import (
    add_base_option,
    add_domain_option,
    add_query_options,
    collect_query,
)

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


DASHBOARD_AD_HISTORY_FIELDS = """Поля ответа:
  YYYY-MM     — период в формате год-месяц
  adCost      — стоимость рекламы за период
  adsCount    — количество рекламных объявлений
  adTraf      — рекламный трафик
  adKeysCount — количество рекламных ключевых слов"""


DASHBOARD_SIMILARKEYS_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив записей с дополняющими фразами
  word          — ключевая фраза
  cnt           — степень похожести
  ws            — базовая частотность
  wsk           — очень точная частотность
  docs          — количество документов в выдаче
  avbid         — средняя цена клика
  numwords      — количество слов в запросе
  adscnt        — количество объявлений в контексте
  isgeo         — является топонимом
  isquest       — является вопросом
  wizardscount  — число колдунщиков
  wizards       — колдунщики
  serpf         — дата изменения позиции
  kei           — индекс эффективности ключевой фразы"""


DASHBOARD_TOP_VISIBILITY_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив доменов в рейтинге
  id            — идентификатор домена
  name          — домен
  topvis        — позиция по видимости
  it3           — запросов в топ-3
  it5           — запросов в топ-5
  it10          — запросов в топ-10
  it50          — запросов в топ-50
  pagesinindex  — количество страниц в выдаче
  adtraf        — оценка трафика из контекста
  adcost        — оценка бюджета контекста
  adscnt        — количество объявлений в контексте
  adkeyscnt     — количество запросов в контексте"""


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


def add_ad_history_parser(dashboard_commands: Any) -> None:
    """Attach the dashboard ad-history parser."""
    parser = dashboard_commands.add_parser(
        "ad-history",
        help="История рекламных метрик домена",
        description="История рекламных метрик домена по месяцам",
        epilog=DASHBOARD_AD_HISTORY_FIELDS,
    )
    add_domain_option(parser)
    add_base_option(parser)
    parser.set_defaults(action="dashboard.ad_history")


def add_similarkeys_parser(dashboard_commands: Any) -> None:
    """Attach the dashboard similarkeys parser."""
    parser = dashboard_commands.add_parser(
        "similarkeys",
        help="Дополняющие фразы по ключевой фразе",
        description="Список дополняющих фраз для выбранной ключевой фразы",
        epilog=DASHBOARD_SIMILARKEYS_FIELDS,
    )
    parser.add_argument("--keyword", required=True, help="Поисковая фраза")
    add_query_options(parser)
    parser.set_defaults(action="dashboard.similarkeys")


def add_top_visibility_parser(dashboard_commands: Any) -> None:
    """Attach the dashboard top-visibility parser."""
    parser = dashboard_commands.add_parser(
        "top-visibility",
        help="Рейтинг сайтов по видимости",
        description="Список доменов в рейтинге по видимости относительно домена",
        epilog=DASHBOARD_TOP_VISIBILITY_FIELDS,
    )
    add_domain_option(parser)
    add_base_option(parser)
    parser.add_argument("--page", type=int, help="Номер страницы")
    parser.add_argument("--per-page", dest="per_page", type=int, help="Размер страницы")
    parser.add_argument("--sort", help="Параметр сортировки")
    parser.set_defaults(action="dashboard.top_visibility")


def add_parser(commands: Any) -> None:
    """Attach the dashboard parser tree."""
    parser = commands.add_parser(
        "dashboard", help="Дашборды и обзорные отчеты для домена и ключевой фразы"
    )
    dashboard_commands = parser.add_subparsers(dest="dashboard_command", required=True)
    add_domain_parser(dashboard_commands)
    add_keyword_parser(dashboard_commands)
    add_ad_history_parser(dashboard_commands)
    add_similarkeys_parser(dashboard_commands)
    add_top_visibility_parser(dashboard_commands)


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
    if args.action == "dashboard.ad_history":
        payload = {"domain": args.domain}
        if args.base is not None:
            payload["base"] = args.base
        return simple.retrieve_domain_ad_history(**payload)
    if args.action == "dashboard.similarkeys":
        query = collect_query(args)
        return simple.retrieve_similarkeys(keyword=args.keyword, **query)
    if args.action == "dashboard.top_visibility":
        payload = {"domain": args.domain}
        for key in ("base", "page", "per_page", "sort"):
            value = getattr(args, key, None)
            if value is not None:
                payload[key] = value
        return simple.retrieve_top_domain_visibility(**payload)
    raise ValueError(f"Unsupported action: {args.action}")
