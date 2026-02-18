"""Skill file templates and installer for keysso-cli."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from keysso_cli.context import (
    ADS_FACTS_FIELDS,
    ADS_LINKS_FIELDS,
    ADS_RETRIEVE_FIELDS,
    CONCURENTS_FIELDS,
    KEYWORDS_BYADS_FIELDS,
    KEYWORDS_LIST_FIELDS,
)
from keysso_cli.dashboard import DASHBOARD_DOMAIN_FIELDS, DASHBOARD_KEYWORD_FIELDS
from keysso_cli.direct import DIRECT_ADS_FIELDS, DIRECT_DOMAIN_FIELDS

SKILL_TEMPLATE = """---
name: keysso-cli
description: Скилл для работы со всем сервисом Keys.so — сервисом анализа конкурентов в SEO и PPC. Используйте skill, когда нужно собрать команды, подобрать параметры, интерпретировать ответы API и выстроить рабочий процесс через локальную команду keysso-cli.
---

# keysso-cli

Используйте этот skill для практической работы с локальной командой `keysso-cli`.
Подробное описание разделов находится в `references/dashboard.md` и `references/context-ads.md`.

## Ограничения API

- Лимит: 1 запрос в секунду
- Пакетный режим: можно отправить до 10 запросов подряд
- После пакета из 10 запросов следующий запрос сработает только через 10 секунд

## Дашборд

Доступные команды раздела `dashboard`:

- `keysso-cli dashboard domain --domain <домен>` # сводка по домену
- `keysso-cli dashboard keyword --keyword <фраза>` # сводка по ключевой фразе

## Контекстная реклама

Доступные команды раздела `context`:

- `keysso-cli context concurents --domain <домен>` # конкуренты домена в контекстной рекламе
- `keysso-cli context keywords list --domain <домен>` # ключевые слова домена в контекстной рекламе
- `keysso-cli context keywords byads --domain <домен> --ads-id <id>` # ключевые слова конкретного объявления
- `keysso-cli context ads retrieve --domain <домен>` # объявления домена
- `keysso-cli context ads links --domain <домен>` # уникальные ссылки из объявлений
- `keysso-cli context ads facts --domain <домен>` # уникальные факты из объявлений

## Яндекс Директ

Доступные команды раздела `direct`:

- `keysso-cli direct domain --domain <домен>` # объявления Яндекс Директ по домену
- `keysso-cli direct ads --kid <id>` # объявления Яндекс Директ по идентификатору фразы
- `keysso-cli direct ads --keyword <фраза>` # объявления Яндекс Директ по поисковой фразе

## Региональные базы (`--base`)

- `msk` # Яндекс, Москва
- `rnd` # Яндекс, Ростов-на-Дону
- `ekb` # Яндекс, Екатеринбург
- `ufa` # Яндекс, Уфа
- `sar` # Яндекс, Саратов
- `krr` # Яндекс, Краснодар
- `prm` # Яндекс, Пермь
- `sam` # Яндекс, Самара
- `kry` # Яндекс, Красноярск
- `oms` # Яндекс, Омск
- `kzn` # Яндекс, Казань
- `che` # Яндекс, Челябинск
- `nsk` # Яндекс, Новосибирск
- `nnv` # Яндекс, Н. Новгород
- `vlg` # Яндекс, Волгоград
- `vrn` # Яндекс, Воронеж
- `spb` # Яндекс, Санкт-Петербург
- `mns` # Яндекс, Минск
- `tmn` # Яндекс, Тюмень
- `tom` # Яндекс, Томск
- `gru` # Google, Москва
- `gkv` # Google, Киев
- `gmns` # Google, Минск
- `gny` # Google, New York
- `zen` # Дзен
"""

CONTEXT_ADS_REFERENCE = f"""# Разделы «Контекстная реклама» и «Яндекс Директ» в keysso-cli

Этот файл описывает текущую структуру `keysso-cli` для разделов `context` и `direct`.

## Базовый запуск

- Передайте токен через `--api-key` или переменную окружения `KEYSSO_API_KEY`
- Основной формат: `keysso-cli context ...` и `keysso-cli direct ...`

## Дерево команд

```text
keysso-cli
  context
    concurents
    keywords
      list
      byads
    ads
      retrieve
      links
      facts
  direct
    domain
    ads
```

## Общие аргументы

- `--domain` обязателен для всех команд внутри `context` и для `direct domain`
- `--keyword` альтернатива `--kid` для команды `direct ads`
- `--kid` обязателен для команды `direct ads`
- `--base` региональная база (`msk`, `spb`, `zen`, `gru` и другие)
- `--filter` фильтр запроса
- `--page` номер страницы
- `--per-page` размер страницы
- `--sort` сортировка

## Команды и особенности

### `context concurents`

- Назначение: получить список конкурентов домена в контекстной рекламе
- Пример: `keysso-cli context concurents --domain пример.рф --base msk`

Поля ответа API:

```text
{CONCURENTS_FIELDS}
```

### `context keywords list`

- Назначение: получить ключевые слова домена в контексте
- Пример: `keysso-cli context keywords list --domain пример.рф --base msk --page 1 --per-page 25`

Поля ответа API:

```text
{KEYWORDS_LIST_FIELDS}
```

### `context keywords byads`

- Назначение: получить ключевые слова конкретного объявления
- Дополнительно обязателен `--ads-id`
- Пример: `keysso-cli context keywords byads --domain пример.рф --ads-id 42 --base msk`

Поля ответа API:

```text
{KEYWORDS_BYADS_FIELDS}
```

### `context ads retrieve`

- Назначение: получить объявления домена
- Опция `--full` добавляет массив ключевых слов в каждом объявлении
- Пример: `keysso-cli context ads retrieve --domain пример.рф --base msk --full`

Поля ответа API:

```text
{ADS_RETRIEVE_FIELDS}
```

### `context ads links`

- Назначение: получить уникальные ссылки из объявлений
- Пример: `keysso-cli context ads links --domain пример.рф --base msk`

Поля ответа API:

```text
{ADS_LINKS_FIELDS}
```

### `context ads facts`

- Назначение: получить уникальные факты из объявлений
- Пример: `keysso-cli context ads facts --domain пример.рф --base msk`

Поля ответа API:

```text
{ADS_FACTS_FIELDS}
```

### `direct domain`

- Назначение: получить объявления Яндекс Директ по домену
- Пример: `keysso-cli direct domain --domain пример.рф --base msk --page 1 --per-page 25`

Поля ответа API:

```text
{DIRECT_DOMAIN_FIELDS}
```

### `direct ads`

- Назначение: получить объявления Яндекс Директ по идентификатору фразы
- Нужен один из аргументов: `--kid` или `--keyword`
- Пример: `keysso-cli direct ads --kid 17222067 --base msk --page 1 --per-page 25`
- Пример: `keysso-cli direct ads --keyword "пластиковые окна" --base msk --page 1 --per-page 25`

Поля ответа API:

```text
{DIRECT_ADS_FIELDS}
```

## Практический рабочий процесс

1. Сначала получите конкурентное окружение через `context concurents`
2. Затем соберите семантику через `context keywords list`
3. При необходимости разберите отдельные объявления через `context keywords byads`
4. Для креативов и агрегатов используйте блок `context ads` (`retrieve`, `links`, `facts`)
5. Для анализа Яндекс Директ используйте `direct domain` и `direct ads`
"""

DASHBOARD_REFERENCE = f"""# Раздел «Дашборд» в keysso-cli

Этот файл описывает структуру `keysso-cli` для раздела `dashboard`.

## Базовый запуск

- Передайте токен через `--api-key` или переменную окружения `KEYSSO_API_KEY`
- Основной формат: `keysso-cli dashboard ...`

## Дерево команд

```text
keysso-cli
  dashboard
    domain
    keyword
```

## Общие аргументы

- `--domain` обязателен для `dashboard domain`
- `--keyword` обязателен для `dashboard keyword`
- `--base` региональная база (`msk`, `spb`, `zen`, `gru` и другие)

## Команды и особенности

### `dashboard domain`

- Назначение: получить сводные данные по домену
- Пример: `keysso-cli dashboard domain --domain пример.рф --base msk`

Поля ответа API:

```text
{DASHBOARD_DOMAIN_FIELDS}
```

### `dashboard keyword`

- Назначение: получить сводные данные по ключевой фразе
- Пример: `keysso-cli dashboard keyword --keyword "пластиковые окна" --base msk`

Поля ответа API:

```text
{DASHBOARD_KEYWORD_FIELDS}
```

## Практический рабочий процесс

1. Сначала проверьте обзор домена через `dashboard domain`
2. Для анализа конкретной фразы используйте `dashboard keyword`
"""


def install_skills() -> dict[str, Any]:
    """Create keysso-cli skill files in the current directory."""
    folder = Path.cwd() / ".claude" / "skills" / "keysso-cli"
    files = [
        (folder / "SKILL.md", SKILL_TEMPLATE),
        (folder / "references" / "dashboard.md", DASHBOARD_REFERENCE),
        (folder / "references" / "context-ads.md", CONTEXT_ADS_REFERENCE),
    ]
    written: list[str] = []
    for path, content in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(str(path))
    return {"status": "ok", "path": str(folder), "files": written}
