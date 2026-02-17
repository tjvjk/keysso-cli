# Раздел «Контекстная реклама» в keysso-cli

Этот файл описывает только текущую структуру `keysso-cli` для раздела `context`.

## Базовый запуск

- Передайте токен через `--api-key` или переменную окружения `KEYSSO_API_KEY`
- Основной формат: `keysso-cli context ...`

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
```

## Общие аргументы

- `--domain` обязателен для всех команд внутри `context`
- `--base` региональная база (`msk`, `spb`, `zen`, `gru` и другие)
- `--filter` фильтр запроса
- `--page` номер страницы
- `--per-page` размер страницы
- `--sort` сортировка

## Команды и особенности

### `context concurents`

- Назначение: получить список конкурентов домена в контекстной рекламе
- Пример: `keysso-cli context concurents --domain пример.рф --base msk`

### `context keywords list`

- Назначение: получить ключевые слова домена в контексте
- Пример: `keysso-cli context keywords list --domain пример.рф --base msk --page 1 --per-page 25`

### `context keywords byads`

- Назначение: получить ключевые слова конкретного объявления
- Дополнительно обязателен `--ads-id`
- Пример: `keysso-cli context keywords byads --domain пример.рф --ads-id 42 --base msk`

### `context ads retrieve`

- Назначение: получить объявления домена
- Опция `--full` добавляет массив ключевых слов в каждом объявлении
- Пример: `keysso-cli context ads retrieve --domain пример.рф --base msk --full`

### `context ads links`

- Назначение: получить уникальные ссылки из объявлений
- Пример: `keysso-cli context ads links --domain пример.рф --base msk`

### `context ads facts`

- Назначение: получить уникальные факты из объявлений
- Пример: `keysso-cli context ads facts --domain пример.рф --base msk`

## Практический рабочий процесс

1. Сначала получите конкурентное окружение через `context concurents`
2. Затем соберите семантику через `context keywords list`
3. При необходимости разберите отдельные объявления через `context keywords byads`
4. Для креативов и агрегатов используйте блок `context ads` (`retrieve`, `links`, `facts`)
