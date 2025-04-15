from typing import TypeVar

from schemas.tables import TableCreate
from .abstract.repo import TableRepository

TableModel = TypeVar("TableModel")


class TableService:
    """Сервис для работы с таблицами. Использует репозиторий `TableRepository` для выполнения операций с таблицами."""

    def __init__(self, repository: TableRepository):
        self._repository = repository

    async def get_table_with_reservations(self) -> list[TableModel]:
        """Получает все таблицы с их бронированиями."""
        return await self._repository.get_all_with_reservations()

    async def get_table(self, table_id: int) -> TableModel:
        """Получает таблицу по её ID."""
        return await self._repository.get(_id=table_id)

    async def get_list_tables(self, offset: int, limit: int) -> list[TableModel]:
        """Получает список таблиц с пагинацией."""
        return await self._repository.get_all(offset, limit)

    async def create_table(self, instance: TableCreate) -> TableModel:
        """Создаёт новую таблицу."""
        return await self._repository.create(schema=instance)

    async def delete_table(self, instance: TableModel) -> None:
        """Удаляет таблицу."""
        await self._repository.delete(instance=instance)
