# Wikipedia Parser with AI Summary

Проект для парсинга статей Wikipedia с рекурсивным обходом ссылок и генерацией summary с помощью OpenAI.

## Возможности

- Рекурсивный парсинг статей Wikipedia (до 5 уровней вложенности)
- Сохранение статей в PostgreSQL
- Генерация summary с помощью OpenAI GPT
- Асинхронная обработка
# Wikipedia Parser

## 📄 Описание проекта

Wikipedia Parser — это сервис для рекурсивного парсинга статей Wikipedia с сохранением данных в базу PostgreSQL и генерацией краткого summary с помощью нейросети DeepSeek.

## 🚀 Функциональность

- ✅ Рекурсивный парсинг Wikipedia до 5 уровней вложенности
- ✅ Сохранение статей в PostgreSQL
- ✅ Генерация краткого summary с помощью DeepSeek API
- ✅ REST API на FastAPI
- ✅ Асинхронные запросы к БД через SQLAlchemy
- ✅ Alembic для миграций базы данных
- ✅ Полностью контейнеризированный проект (Docker + Docker Compose)
- ✅ Покрытие тестами (pytest)

## ⚙️ Переменные окружения

Создайте файл `.env` в корне проекта.

Пример `.env`:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=wikipedia_parser
POSTGRES_HOST=db
POSTGRES_PORT=5432

DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

MAX_RECURSION_DEPTH=5
```

🔑 Получите API ключ для DeepSeek на сайте [https://deepseek.com/](https://deepseek.com/)

## 🐳 Как запустить проект

### 1️⃣ Сборка и запуск контейнеров

```bash
docker-compose up --build
```

Проект будет доступен по адресу:

```
http://localhost:8000
```

Swagger-документация API:

```
http://localhost:8000/docs
```

### 2️⃣ Миграции базы данных

Выполнить миграции:

```bash
docker-compose exec app alembic upgrade head
```

Создать новую миграцию после изменения моделей:

```bash
docker-compose exec app alembic revision --autogenerate -m "описание_миграции"
```

## ✅ Использование API

### 🔍 Запуск парсинга

**POST** `/api/v1/parse`

Тело запроса:

```json
{
  "url": "https://ru.wikipedia.org/wiki/Python"
}
```

Ответ:

```json
{
  "message": "Парсинг запущен в фоновом режиме",
  "url": "https://ru.wikipedia.org/wiki/Python"
}
```

### 📄 Получение summary

**GET** `/api/v1/summary?url=https://ru.wikipedia.org/wiki/Python`

Ответ:

```json
{
  "url": "https://ru.wikipedia.org/wiki/Python",
  "title": "Python",
  "summary": "Краткое summary статьи...",
  "children_count": 3
}
```

## 🗄️ Работа с базой данных

Подключение к базе внутри контейнера:

```bash
docker-compose exec db psql -U postgres -d wikipedia_parser
```

Пример SQL-запроса:

```sql
SELECT * FROM articles;
```

## 🧪 Запуск тестов

```bash
docker-compose exec app pytest -v
```

## 📦 Структура проекта

```
app/
├── api/               # Endpoints FastAPI
├── models/            # SQLAlchemy модели
├── repositories/      # Работа с базой
├── schemas/           # Pydantic схемы
├── services/          # Логика парсера и генерации summary
├── database.py        # Подключение к БД
├── config.py          # Конфигурация проекта
alembic/               # Миграции базы данных
tests/                 # Юнит-тесты
docker-compose.yml     # Docker Compose конфигурация
Dockerfile             # Dockerfile для приложения
.env.example           # Шаблон .env
```

## 💡 Примечания

- Парсер работает только с русскоязычной Википедией.
- Summary генерируется только для корневых статей (без parent).
- Максимальная глубина парсинга регулируется переменной `MAX_RECURSION_DEPTH`.

## 🧠 Автор

- [Almas1989](https://github.com/Almas1989)

---

# Wikipedia Parser

## 📄 Project Description

Wikipedia Parser is a service for recursive parsing of Wikipedia articles, storing them into a PostgreSQL database, and generating concise summaries using the DeepSeek AI model.

## 🚀 Features

- ✅ Recursive parsing of Wikipedia up to 5 depth levels
- ✅ Storing articles in PostgreSQL
- ✅ Summary generation via DeepSeek API
- ✅ REST API with FastAPI
- ✅ Asynchronous database operations with SQLAlchemy
- ✅ Database migrations with Alembic
- ✅ Fully containerized (Docker + Docker Compose)
- ✅ Unit tests included (pytest)

## ⚙️ Environment Variables

Create a `.env` file in the root directory.

Example `.env`:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=wikipedia_parser
POSTGRES_HOST=db
POSTGRES_PORT=5432

DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

MAX_RECURSION_DEPTH=5
```

🔑 Get your API key from [https://deepseek.com/](https://deepseek.com/)

## 🐳 How to Run

### 1️⃣ Build and Start Containers

```bash
docker-compose up --build
```

The service will be available at:

```
http://localhost:8000
```

Swagger API Docs:

```
http://localhost:8000/docs
```

### 2️⃣ Database Migrations

Apply migrations:

```bash
docker-compose exec app alembic upgrade head
```

Create a new migration after modifying models:

```bash
docker-compose exec app alembic revision --autogenerate -m "migration_description"
```

## ✅ API Usage

### 🔍 Start Parsing

**POST** `/api/v1/parse`

Request body:

```json
{
  "url": "https://ru.wikipedia.org/wiki/Python"
}
```

Response:

```json
{
  "message": "Parsing started in background",
  "url": "https://ru.wikipedia.org/wiki/Python"
}
```

### 📄 Get Summary

**GET** `/api/v1/summary?url=https://ru.wikipedia.org/wiki/Python`

Response:

```json
{
  "url": "https://ru.wikipedia.org/wiki/Python",
  "title": "Python",
  "summary": "Short summary of the article...",
  "children_count": 3
}
```

## 🗄️ Database Access

Connect to PostgreSQL inside the container:

```bash
docker-compose exec db psql -U postgres -d wikipedia_parser
```

Example SQL query:

```sql
SELECT * FROM articles;
```

## 🧪 Run Tests

```bash
docker-compose exec app pytest -v
```

## 📦 Project Structure

```
app/
├── api/               # FastAPI endpoints
├── models/            # SQLAlchemy models
├── repositories/      # Database layer
├── schemas/           # Pydantic schemas
├── services/          # Parsing and AI logic
├── database.py        # Database connection
├── config.py          # Project configuration
alembic/               # Database migrations
tests/                 # Unit tests
docker-compose.yml     # Docker Compose file
Dockerfile             # App Dockerfile
.env.example           # Example environment file
```

## 💡 Notes

- The parser currently works only with Russian Wikipedia.
- Summary is generated only for root articles (with no parent).
- Maximum parsing depth is controlled via `MAX_RECURSION_DEPTH`.

## 🧠 Author

- [Almas1989](https://github.com/Almas1989)

- Docker-контейнеризация
- FastAPI с dependency injection

## Установка и запуск

### 1. Клонирование и подготовка

```bash
git clone <your-repo-url>
cd wikipedia_parser