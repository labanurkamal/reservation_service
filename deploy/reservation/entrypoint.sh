#!/bin/bash

set -e

echo "Контейнер стартует"

echo "Применяем миграцию в Reservation..."
cd src
alembic upgrade head
echo "Миграцию успешно применен!"

echo "-------Запуск приложения-------"
exec uvicorn main:app --host 0.0.0.0 --port 8000