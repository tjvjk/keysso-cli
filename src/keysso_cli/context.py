"""Context command tree and SDK routing."""

from __future__ import annotations

import argparse
from typing import Any

from keysso_cli.query import add_domain_option, add_query_options, collect_query


CONCURENTS_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив записей по конкурентам
  id            — идентификатор домена
  name          — имя домена
  perc          — степень похожести домена (% общих ключей)
  theme         — тематичность домена (% ключей анализируемого домена в ключах домена)
  cnt           — общих ключей в топ-50
  it1           — запросов в топ-1
  it3           — запросов в топ-3
  it5           — запросов в топ-5
  it10          — запросов в топ-10
  it50          — запросов в топ-50
  pagesinindex  — количество страниц сайта в выдаче
  vis           — оценка трафика с поиска
  adscnt        — количество объявлений в контексте
  adkeyscnt     — количество запросов в контексте
  adtraf        — оценка трафика из контекста
  adcost        — оценка бюджета контекста"""


KEYWORDS_LIST_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив записей по ключевым словам
  id            — идентификатор фразы
  word          — ключевая фраза
  ws            — базовая частотность
  wsk           — очень точная частотность
  pos           — позиция в контексте
  avbid         — средняя цена клика
  sr            — блок размещения объявлений (1 — премиум, 0 — остальные)
  aid           — идентификатор объявления
  adscnt        — количество объявлений в контексте
  header        — заголовок объявления
  txt           — текст объявления
  url           — URL объявления
  docs          — количество документов в выдаче
  numwords      — количество слов в запросе
  isgeo         — является топонимом
  isquest       — является вопросом
  serpf         — дата изменения позиции"""


KEYWORDS_BYADS_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив ключевых слов выбранного объявления
  word          — ключевая фраза
  ws            — базовая частотность
  wsk           — очень точная частотность
  superwsk      — суперточная частотность
  pos           — позиция в контексте
  avbid         — средняя цена клика
  sr            — блок размещения объявлений (1 — премиум, 0 — остальные)
  adscnt        — количество объявлений в контексте
  header        — заголовок объявления
  txt           — текст объявления
  docs          — количество документов в выдаче
  numwords      — количество слов в запросе
  isgeo         — является топонимом
  isquest       — является вопросом
  serp          — дата обновления"""


ADS_RETRIEVE_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив объявлений
  id            — идентификатор объявления
  header        — заголовок объявления
  txt           — текст объявления
  links         — массив быстрых ссылок
  facts         — массив фактов
  keyscnt       — количество запросов
  keys          — массив ключевых слов (доступно при --full)
  url           — URL объявления
  legal         — рекламодатель
  serp          — дата обновления"""


ADS_LINKS_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив записей с уникальными ссылками
  links         — уникальные ссылки"""


ADS_FACTS_FIELDS = """Поля ответа:
  current_page  — текущая страница
  per_page      — записей на странице
  last_page     — последняя страница
  total         — всего записей
  data          — массив записей с уникальными фактами
  facts         — уникальные факты"""


def add_concurents_parser(context_commands: Any) -> None:
    """Attach the context concurents parser."""
    parser = context_commands.add_parser(
        "concurents",
        help="Показать конкурентов домена в контекстной рекламе",
        description="Список конкурентов домена в контекстной рекламе",
        epilog=CONCURENTS_FIELDS,
    )
    add_domain_option(parser)
    add_query_options(parser)
    parser.set_defaults(action="concurents")


def add_keywords_list_parser(keyword_commands: Any) -> None:
    """Attach the keywords list parser."""
    parser = keyword_commands.add_parser(
        "list",
        help="Список ключевых слов контекстной рекламы домена",
        description="Список ключевых слов домена в контекстной рекламе",
        epilog=KEYWORDS_LIST_FIELDS,
    )
    add_domain_option(parser)
    add_query_options(parser)
    parser.set_defaults(action="keywords.list")


def add_keywords_byads_parser(keyword_commands: Any) -> None:
    """Attach the keywords byads parser."""
    parser = keyword_commands.add_parser(
        "byads",
        help="Ключевые слова для конкретного объявления",
        description="Ключевые слова, по которым показывается выбранное объявление",
        epilog=KEYWORDS_BYADS_FIELDS,
    )
    add_domain_option(parser)
    add_query_options(parser)
    parser.add_argument("--ads-id", required=True, dest="ads_id", help="Идентификатор объявления")
    parser.set_defaults(action="keywords.byads")


def add_keywords_parser(context_commands: Any) -> None:
    """Attach the keywords parser tree."""
    parser = context_commands.add_parser("keywords", help="Показать ключевые слова из объявлений домена")
    keyword_commands = parser.add_subparsers(dest="keyword_command", required=True)
    add_keywords_list_parser(keyword_commands)
    add_keywords_byads_parser(keyword_commands)


def add_ads_retrieve_parser(ad_commands: Any) -> None:
    """Attach the ads retrieve parser."""
    parser = ad_commands.add_parser(
        "retrieve",
        help="Список объявлений домена в контекстной рекламе",
        description="Список объявлений домена в контекстной рекламе",
        epilog=ADS_RETRIEVE_FIELDS,
    )
    add_domain_option(parser)
    add_query_options(parser)
    parser.add_argument("--full", action="store_true", help="Добавить массив ключевых слов для каждого объявления")
    parser.set_defaults(action="ads.retrieve")


def add_ads_links_parser(ad_commands: Any) -> None:
    """Attach the ads links parser."""
    parser = ad_commands.add_parser(
        "links",
        help="Уникальные ссылки из объявлений домена",
        description="Список уникальных ссылок, найденных в объявлениях домена",
        epilog=ADS_LINKS_FIELDS,
    )
    add_domain_option(parser)
    add_query_options(parser)
    parser.set_defaults(action="ads.links")


def add_ads_facts_parser(ad_commands: Any) -> None:
    """Attach the ads facts parser."""
    parser = ad_commands.add_parser(
        "facts",
        help="Уникальные факты из объявлений домена",
        description="Список уникальных фактов, найденных в объявлениях домена",
        epilog=ADS_FACTS_FIELDS,
    )
    add_domain_option(parser)
    add_query_options(parser)
    parser.set_defaults(action="ads.facts")


def add_ads_parser(context_commands: Any) -> None:
    """Attach the ads parser tree."""
    parser = context_commands.add_parser("ads", help="Показать объявления и их агрегированные элементы")
    ad_commands = parser.add_subparsers(dest="ad_command", required=True)
    add_ads_retrieve_parser(ad_commands)
    add_ads_links_parser(ad_commands)
    add_ads_facts_parser(ad_commands)


def add_parser(commands: Any) -> None:
    """Attach the context parser tree."""
    parser = commands.add_parser("context", help="Отчеты по контекстной рекламе для домена")
    context_commands = parser.add_subparsers(dest="context_command", required=True)
    add_concurents_parser(context_commands)
    add_keywords_parser(context_commands)
    add_ads_parser(context_commands)


def invoke(client: Any, args: argparse.Namespace) -> Any:
    """Route parsed context arguments to one SDK call."""
    context = client.report.simple.context
    query = collect_query(args)
    if args.action == "concurents":
        return context.retrieve_concurents(domain=args.domain, **query)
    if args.action == "keywords.list":
        return context.keywords.list(domain=args.domain, **query)
    if args.action == "keywords.byads":
        return context.keywords.retrieve_byads(domain=args.domain, ads_id=args.ads_id, **query)
    if args.action == "ads.retrieve":
        payload = {"domain": args.domain, **query}
        if args.full:
            payload["full"] = True
        return context.ads.retrieve(**payload)
    if args.action == "ads.links":
        return context.ads.retrieve_links(domain=args.domain, **query)
    if args.action == "ads.facts":
        return context.ads.retrieve_facts(domain=args.domain, **query)
    raise ValueError(f"Unsupported action: {args.action}")
