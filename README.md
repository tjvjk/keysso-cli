# Keysso CLI

Minimal CLI wrapper around the Python SDK for `report.simple.context` endpoints.

## Install

```sh
uv sync
```

## Usage

```sh
KEYSSO_API_KEY="your-token" uv run keysso-cli context concurents --domain пример.рф --base msk
```

```sh
KEYSSO_API_KEY="your-token" uv run keysso-cli context keywords list --domain пример.рф --base msk --page 1 --per-page 25
```

```sh
KEYSSO_API_KEY="your-token" uv run keysso-cli context keywords byads --domain пример.рф --ads-id 42 --base msk
```

```sh
KEYSSO_API_KEY="your-token" uv run keysso-cli context ads retrieve --domain пример.рф --base msk --full
```

```sh
KEYSSO_API_KEY="your-token" uv run keysso-cli context ads links --domain пример.рф --base msk
```

```sh
KEYSSO_API_KEY="your-token" uv run keysso-cli context ads facts --domain пример.рф --base msk
```
