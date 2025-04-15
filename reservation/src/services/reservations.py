from datetime import timedelta
from typing import TypeVar

from pydantic import BaseModel

from exceptions.base import ReservationConflictError
from .abstract.repo import ReservationRepository

ReservationModel = TypeVar('ReservationModel')
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)


class ReservationService:
    """
    Сервис для работы с бронированиями. Использует репозиторий
    `ReservationRepository` для выполнения операций с бронированиями.
    """

    def __init__(self, repository: ReservationRepository):
        self._repository = repository

    async def get_reservation(self, reservation_id: int) -> ReservationModel:
        """Получает бронирование по ID."""
        return await self._repository.get(_id=reservation_id)

    async def create_reservation(self, schema: CreateSchema) -> ReservationModel:
        """Создает новое бронирование, проверяя наличие конфликтов."""
        table_id = schema.table_id
        reservation_time = schema.reservation_time
        reservation_end = schema.reservation_time + timedelta(minutes=schema.duration_minutes)

        conflict = await self._repository.check_conflicts(schema.table_id, reservation_time, reservation_end)
        if conflict:
            raise ReservationConflictError(table_id)

        return await self._repository.create(schema)

    async def get_list_reservation(self, offset: int, limit: int) -> list[ReservationModel]:
        """Получает список бронирований с пагинацией."""
        return await self._repository.get_all(offset=offset, limit=limit)

    async def delete_reservation(self, instance: ReservationModel) -> None:
        """Удаляет бронирование."""
        return await self._repository.delete(instance=instance)
