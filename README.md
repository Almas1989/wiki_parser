# Wikipedia Parser with AI Summary

Проект для парсинга статей Wikipedia с рекурсивным обходом ссылок и генерацией summary с помощью OpenAI.

## Возможности

- Рекурсивный парсинг статей Wikipedia (до 5 уровней вложенности)
- Сохранение статей в PostgreSQL
- Генерация summary с помощью OpenAI GPT
- Асинхронная обработка
- Docker-контейнеризация
- FastAPI с dependency injection

## Установка и запуск

### 1. Клонирование и подготовка

```bash
git clone <your-repo-url>
cd wikipedia_parser