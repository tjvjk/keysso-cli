# Keysso CLI

`keysso-cli` — CLI-клиент для работы с Keysso API из терминала.

- Общая документация API: https://apidoc.keys.so/
- Поддержаны разделы «Контекстная реклама» и «Реклама» (Yandex Direct): https://apidoc.keys.so/

## Установка skill в текущей директории

Команда ниже создает `.claude/skills/keysso-cli` в текущем каталоге и добавляет:

- `SKILL.md` с общим описанием skill
- `references/context-ads.md` с подробным описанием раздела `context`

```sh
keysso-cli install --skills
```

## Использование

```sh
export KEYSSO_API_KEY="ваш-токен"
```

```sh
keysso-cli context concurents --domain пример.рф --base msk
```

```sh
keysso-cli context keywords list --domain пример.рф --base msk --page 1 --per-page 25
```

```sh
keysso-cli context keywords byads --domain пример.рф --ads-id 42 --base msk
```

```sh
keysso-cli context ads retrieve --domain пример.рф --base msk --full
```

```sh
keysso-cli context ads links --domain пример.рф --base msk
```

```sh
keysso-cli context ads facts --domain пример.рф --base msk
```

```sh
keysso-cli direct domain --domain пример.рф --base msk --page 1 --per-page 25
```

```sh
keysso-cli direct ads --kid 17222067 --base msk --page 1 --per-page 25
```

```sh
keysso-cli context concurents --help
```

Для расшифровки полей ответа используйте `--help` у каждой команды:

```sh
keysso-cli context keywords list --help
keysso-cli context keywords byads --help
keysso-cli context ads retrieve --help
keysso-cli context ads links --help
keysso-cli context ads facts --help
keysso-cli direct domain --help
keysso-cli direct ads --help
```

## Региональные базы (`--base`)

Региональная база данных, по которой происходит выборка:

### Яндекс

- `msk` - Москва
- `rnd` - Ростов-на-Дону
- `ekb` - Екатеринбург
- `ufa` - Уфа
- `sar` - Саратов
- `krr` - Краснодар
- `prm` - Пермь
- `sam` - Самара
- `kry` - Красноярск
- `oms` - Омск
- `kzn` - Казань
- `che` - Челябинск
- `nsk` - Новосибирск
- `nnv` - Н. Новгород
- `vlg` - Волгоград
- `vrn` - Воронеж
- `spb` - Санкт-Петербург
- `mns` - Минск
- `tmn` - Тюмень
- `tom` - Томск

### Google

- `gru` - Москва
- `gkv` - Киев
- `gmns` - Минск
- `gny` - New York

### Дзен

- `zen`

## Установка для разработки

```sh
uv sync
```

## Установка в систему (без `uv run`)

Из директории `keysso-cli`:

```sh
uv tool install --editable .
```

Если команда `keysso-cli` не находится, добавьте `~/.local/bin` в `PATH`:

```sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Обновление глобальной установки

Если `keysso-cli` установлен из текущей директории как editable, используйте принудительную переустановку:

```sh
uv tool install --editable . --force
```

Если `keysso-cli` установлен как обычный пакет, используйте обновление:

```sh
uv tool upgrade keysso-cli
```

Проверить список глобально установленных инструментов:

```sh
uv tool list
```

## TODO

- Добавить поддержку остальных разделов API из https://apidoc.keys.so/

## Лицензия

Этот проект распространяется по лицензии MIT.
Текст лицензии: https://opensource.org/license/mit/
