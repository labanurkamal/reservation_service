# 🍽️ Reservation API

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.40-blue)
![dependency--injector](https://img.shields.io/badge/dependency_injector-4.46.0-blue)
![pytest](https://img.shields.io/badge/pytest-8.3.5-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Reservation API** — это REST API для бронирования столиков в ресторане. Сервис позволяет создавать, просматривать и удалять брони, а также управлять столиками. Реализована проверка конфликтов бронирований, чтобы предотвратить пересечения по времени для одного столика.

---

## 📌 О проекте

Этот проект разработан в рамках тестового задания для создания API-сервиса бронирования столиков. Он включает:

- **Модели данных**: Столики (`Table`) и брони (`Reservation`).
- **API-методы**: CRUD-операции для столов и броней.
- **Бизнес-логика**: Проверка конфликтов бронирований по времени и столикам.
- **Технологии**: FastAPI, SQLAlchemy, PostgreSQL, Alembic, Docker, pytest.

---

## 🎯 Функциональные возможности

### Модели

- **Table** (Столик):
  - `id`: int (уникальный идентификатор)
  - `name`: str (например, "Table 1")
  - `seats`: int (количество мест)
  - `location`: str (например, "зал у окна")

- **Reservation** (Бронь):
  - `id`: int (уникальный идентификатор)
  - `customer_name`: str (имя клиента)
  - `table_id`: int (внешний ключ на `Table`)
  - `reservation_time`: datetime (время брони)
  - `duration_minutes`: int (длительность в минутах)

### API-эндпоинты
- **Проверка состояния сервиса**
  - `GET /api/v1/healthcheck/` — Проверка состояния сервиса.
- **Столики**:
  - `GET /api/v1/tables/reservations/` — Список столиков с бронями.
  - `GET /api/v1/tables/` — получить список всех столов.
  - `POST /api/v1/tables/` — создать новый столик.
  - `DELETE /api/v1/tables/{id}` — удалить столик по ID.
- **Брони**:
  - `GET /api/v1/reservations/` — получить список всех броней.
  - `POST /api/v1/reservations/` — создать новую бронь (с проверкой конфликтов).
  - `DELETE /api/v1/reservations/{id}` — удалить бронь по ID.

### Бизнес-логика
- Нельзя создать бронь, если столик занят в указанный временной слот (проверка пересечений по времени и `table_id`).
- Валидации обрабатываются на уровне API с возвратом понятных ошибок (например, HTTP 400 при конфликте).


## 🚀 Установка и запуск

### Требования
- Docker
- Docker Compose

1. **Клонируйте репозиторий**:

```bash
git clone git@github.com:labanurkamal/reservation_service.git
cd reservation_service
```

2. **Создайте файл окружения**:

Создайте файл `.env` в корне проекта на основе `.env.example`:
Создайте файл `.env_test` в корне проекта на основе `.env_test.example`:

3. **Запустите приложение**:

```bash
cd deploy
docker-compose up --build -d
```

Это соберет образы и запустит как приложение, так и базу данных.

4. **Доступ к API**:
   - API endpoint: http://localhost:8000
   - Документация Swagger UI: http://localhost:8000/api/openapi


## 🧪 Тестирование

Приложение включает в себя комплексные тесты для всех эндпоинтов и бизнес-логики. Тесты выполняются в отдельной среде с изолированной тестовой базой данных.

**Запуск тестов**:

```bash
docker compose -f docker-compose-reservation-test.yaml up --build -d
```