"""Command line interface for Keysso report simple context endpoints."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Mapping, Sequence
from typing import Any, Callable

from keysso import Keysso


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


class RussianArgumentParser(argparse.ArgumentParser):
    """ArgumentParser with Russian help output."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["add_help"] = False
        kwargs.setdefault("formatter_class", argparse.RawTextHelpFormatter)
        super().__init__(*args, **kwargs)
        self._positionals.title = "позиционные аргументы"
        self._optionals.title = "опции"
        self.add_argument("-h", "--help", action="help", help="показать эту справку и выйти")

    def format_usage(self) -> str:
        """Render usage with a Russian prefix."""
        return super().format_usage().replace("usage: ", "использование: ", 1)

    def format_help(self) -> str:
        """Render full help with a Russian prefix."""
        return super().format_help().replace("usage: ", "использование: ", 1)

    def error(self, message: str) -> None:
        """Render parser errors in Russian."""
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: ошибка: {message}\n")


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


def build_parser() -> argparse.ArgumentParser:
    """Build the full parser tree."""
    parser = RussianArgumentParser(prog="keysso-cli", description="CLI для отчетов по контекстной рекламе Keys.so")
    parser.add_argument("--api-key", dest="api_key", help="Ключ API, по умолчанию из KEYSSO_API_KEY")
    parser.add_argument("--base-url", dest="base_url", help="Переопределить базовый URL API")
    context_group = parser.add_subparsers(dest="context_group", required=True, parser_class=RussianArgumentParser)
    context = context_group.add_parser("context", help="Отчеты по контекстной рекламе для домена")
    context_commands = context.add_subparsers(dest="context_command", required=True)
    concurents = context_commands.add_parser(
        "concurents",
        help="Показать конкурентов домена в контекстной рекламе",
        description="Список конкурентов домена в контекстной рекламе",
        epilog=CONCURENTS_FIELDS,
    )
    add_domain_option(concurents)
    add_query_options(concurents)
    concurents.set_defaults(action="concurents")
    keywords = context_commands.add_parser("keywords", help="Показать ключевые слова из объявлений домена")
    keyword_commands = keywords.add_subparsers(dest="keyword_command", required=True)
    keyword_list = keyword_commands.add_parser(
        "list",
        help="Список ключевых слов контекстной рекламы домена",
        description="Список ключевых слов домена в контекстной рекламе",
        epilog=KEYWORDS_LIST_FIELDS,
    )
    add_domain_option(keyword_list)
    add_query_options(keyword_list)
    keyword_list.set_defaults(action="keywords.list")
    keyword_byads = keyword_commands.add_parser(
        "byads",
        help="Ключевые слова для конкретного объявления",
        description="Ключевые слова, по которым показывается выбранное объявление",
        epilog=KEYWORDS_BYADS_FIELDS,
    )
    add_domain_option(keyword_byads)
    add_query_options(keyword_byads)
    keyword_byads.add_argument("--ads-id", required=True, dest="ads_id", help="Идентификатор объявления")
    keyword_byads.set_defaults(action="keywords.byads")
    ads = context_commands.add_parser("ads", help="Показать объявления и их агрегированные элементы")
    ad_commands = ads.add_subparsers(dest="ad_command", required=True)
    ad_retrieve = ad_commands.add_parser(
        "retrieve",
        help="Список объявлений домена в контекстной рекламе",
        description="Список объявлений домена в контекстной рекламе",
        epilog=ADS_RETRIEVE_FIELDS,
    )
    add_domain_option(ad_retrieve)
    add_query_options(ad_retrieve)
    ad_retrieve.add_argument("--full", action="store_true", help="Добавить массив ключевых слов для каждого объявления")
    ad_retrieve.set_defaults(action="ads.retrieve")
    ad_links = ad_commands.add_parser(
        "links",
        help="Уникальные ссылки из объявлений домена",
        description="Список уникальных ссылок, найденных в объявлениях домена",
        epilog=ADS_LINKS_FIELDS,
    )
    add_domain_option(ad_links)
    add_query_options(ad_links)
    ad_links.set_defaults(action="ads.links")
    ad_facts = ad_commands.add_parser(
        "facts",
        help="Уникальные факты из объявлений домена",
        description="Список уникальных фактов, найденных в объявлениях домена",
        epilog=ADS_FACTS_FIELDS,
    )
    add_domain_option(ad_facts)
    add_query_options(ad_facts)
    ad_facts.set_defaults(action="ads.facts")
    return parser


def collect_query(args: argparse.Namespace) -> dict[str, Any]:
    """Collect shared query options from parsed arguments."""
    query: dict[str, Any] = {}
    for key in ("base", "filter", "page", "per_page", "sort"):
        value = getattr(args, key, None)
        if value is not None:
            query[key] = value
    return query


def invoke(client: Any, args: argparse.Namespace) -> Any:
    """Route parsed arguments to one SDK call."""
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


def emit(payload: Any, stream: Any) -> None:
    """Write one payload to the output stream as JSON."""
    if hasattr(payload, "to_json"):
        stream.write(payload.to_json(indent=2))
        stream.write("\n")
        return
    stream.write(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    stream.write("\n")


def execute(
    argv: Sequence[str] | None = None,
    *,
    client_factory: Callable[..., Any] = Keysso,
    env: Mapping[str, str] | None = None,
    stream: Any = None,
) -> int:
    """Parse args, call SDK, and print JSON response."""
    parser = build_parser()
    args = parser.parse_args(argv)
    source = os.environ if env is None else env
    api_key = args.api_key or source.get("KEYSSO_API_KEY")
    if not api_key:
        parser.error("отсутствует API ключ, передайте --api-key или KEYSSO_API_KEY")
    options: dict[str, Any] = {"api_key": api_key}
    if args.base_url:
        options["base_url"] = args.base_url
    output = sys.stdout if stream is None else stream
    with client_factory(**options) as client:
        emit(invoke(client, args), output)
    return 0


def main() -> None:
    """Run CLI process."""
    raise SystemExit(execute())
