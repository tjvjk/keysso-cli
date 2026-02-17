---
name: keysso-cli
description: Работа с отчетами Keys.so по контекстной рекламе через локальную команду keysso-cli. Используйте skill, когда нужно собрать команды, подобрать параметры, интерпретировать ответы и выстроить рабочий процесс для context concurents, context keywords list/byads и context ads retrieve/links/facts.
---

# keysso-cli

Используйте этот skill для практической работы с локальной командой `keysso-cli`.
Подробное описание раздела контекстной рекламы, дерева команд, опций и сценариев запуска находится в `references/context-ads.md`.

## Контекстная реклама

Доступные команды раздела `context`:

- `keysso-cli context concurents --domain <домен>` # конкуренты домена в контекстной рекламе
- `keysso-cli context keywords list --domain <домен>` # ключевые слова домена в контекстной рекламе
- `keysso-cli context keywords byads --domain <домен> --ads-id <id>` # ключевые слова конкретного объявления
- `keysso-cli context ads retrieve --domain <домен>` # объявления домена
- `keysso-cli context ads links --domain <домен>` # уникальные ссылки из объявлений
- `keysso-cli context ads facts --domain <домен>` # уникальные факты из объявлений

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
