# Keysso CLI

Минимальная CLI-обертка для Keysso API.

## Установка

```sh
uv sync
```

## Использование

```sh
KEYSSO_API_KEY="ваш-токен" uv run keysso-cli context concurents --domain пример.рф --base msk
```

```sh
KEYSSO_API_KEY="ваш-токен" uv run keysso-cli context keywords list --domain пример.рф --base msk --page 1 --per-page 25
```

```sh
KEYSSO_API_KEY="ваш-токен" uv run keysso-cli context keywords byads --domain пример.рф --ads-id 42 --base msk
```

```sh
KEYSSO_API_KEY="ваш-токен" uv run keysso-cli context ads retrieve --domain пример.рф --base msk --full
```

```sh
KEYSSO_API_KEY="ваш-токен" uv run keysso-cli context ads links --domain пример.рф --base msk
```

```sh
KEYSSO_API_KEY="ваш-токен" uv run keysso-cli context ads facts --domain пример.рф --base msk
```

```sh
uv run keysso-cli context concurents --help
```

Для расшифровки полей ответа используйте `--help` у каждой команды:

```sh
uv run keysso-cli context keywords list --help
uv run keysso-cli context keywords byads --help
uv run keysso-cli context ads retrieve --help
uv run keysso-cli context ads links --help
uv run keysso-cli context ads facts --help
```
