# Keysso CLI

Минимальная CLI-обертка для Keysso API.

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

## Использование

```sh
KEYSSO_API_KEY="ваш-токен" keysso-cli context concurents --domain пример.рф --base msk
```

```sh
KEYSSO_API_KEY="ваш-токен" keysso-cli context keywords list --domain пример.рф --base msk --page 1 --per-page 25
```

```sh
KEYSSO_API_KEY="ваш-токен" keysso-cli context keywords byads --domain пример.рф --ads-id 42 --base msk
```

```sh
KEYSSO_API_KEY="ваш-токен" keysso-cli context ads retrieve --domain пример.рф --base msk --full
```

```sh
KEYSSO_API_KEY="ваш-токен" keysso-cli context ads links --domain пример.рф --base msk
```

```sh
KEYSSO_API_KEY="ваш-токен" keysso-cli context ads facts --domain пример.рф --base msk
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
```
