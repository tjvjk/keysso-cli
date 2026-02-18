"""Command line interface for Keysso report simple endpoints."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Mapping, Sequence
from typing import Any, Callable

from keysso import Keysso

from keysso_cli.context import add_parser as add_context_parser
from keysso_cli.context import invoke as invoke_context
from keysso_cli.dashboard import add_parser as add_dashboard_parser
from keysso_cli.dashboard import invoke as invoke_dashboard
from keysso_cli.direct import add_parser as add_direct_parser
from keysso_cli.direct import invoke as invoke_direct
from keysso_cli.skills import install_skills


class RussianArgumentParser(argparse.ArgumentParser):
    """ArgumentParser with Russian help output."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["add_help"] = False
        kwargs.setdefault("formatter_class", argparse.RawTextHelpFormatter)
        super().__init__(*args, **kwargs)
        self._positionals.title = "позиционные аргументы"
        self._optionals.title = "опции"
        self.add_argument(
            "-h", "--help", action="help", help="показать эту справку и выйти"
        )

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


def add_install_parser(commands: Any) -> None:
    """Attach the install parser."""
    parser = commands.add_parser(
        "install",
        help="Установить локальные ресурсы keysso-cli",
        description="Установка локальных ресурсов keysso-cli",
    )
    parser.add_argument(
        "--skills",
        action="store_true",
        help="Установить skill keysso-cli в .claude/skills",
    )
    parser.set_defaults(action="install")


def build_parser() -> argparse.ArgumentParser:
    """Build the full parser tree."""
    parser = RussianArgumentParser(
        prog="keysso-cli",
        description="CLI для отчетов дашборда, контекстной рекламы в Keys.so",
    )
    parser.add_argument(
        "--api-key", dest="api_key", help="Ключ API, по умолчанию из KEYSSO_API_KEY"
    )
    parser.add_argument(
        "--base-url", dest="base_url", help="Переопределить базовый URL API"
    )
    commands = parser.add_subparsers(
        dest="command", required=True, parser_class=RussianArgumentParser
    )
    add_dashboard_parser(commands)
    add_context_parser(commands)
    add_direct_parser(commands)
    add_install_parser(commands)
    return parser


def invoke(client: Any, args: argparse.Namespace) -> Any:
    """Route parsed arguments to one SDK call."""
    if args.command == "dashboard":
        return invoke_dashboard(client, args)
    if args.command == "context":
        return invoke_context(client, args)
    if args.command == "direct":
        return invoke_direct(client, args)
    raise ValueError(f"Unsupported command: {args.command}")


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
    output = sys.stdout if stream is None else stream
    if args.command == "install":
        if not args.skills:
            parser.error("для команды install требуется флаг --skills")
        emit(install_skills(), output)
        return 0
    source = os.environ if env is None else env
    api_key = args.api_key or source.get("KEYSSO_API_KEY")
    if not api_key:
        parser.error("отсутствует API ключ, передайте --api-key или KEYSSO_API_KEY")
    options: dict[str, Any] = {"api_key": api_key}
    if args.base_url:
        options["base_url"] = args.base_url
    with client_factory(**options) as client:
        emit(invoke(client, args), output)
    return 0


def main() -> None:
    """Run CLI process."""
    raise SystemExit(execute())
