from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

DBModel = TypeVar("DBModel", bound=DeclarativeBase)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
ResponseSchema = TypeVar('ResponseSchema', bound=BaseModel)


class IDBRepository(ABC, Generic[DBModel, CreateSchema, ResponseSchema]):
    """
    Интерфейс абстрактного репозитория для асинхронной работы с базой данных.
    Используется для реализации CRUD-операций.
    """

    @abstractmethod
    async def get(self, _id: Any, **kwargs) -> DBModel | None:
        """Получить объект по его ID."""
        ...

    @abstractmethod
    async def get_all(self, offset: int, limit: int, **kwargs: Any) -> list[DBModel]:
        """Получить список объектов с пагинацией."""
        ...

    @abstractmethod
    async def create(self, schema: CreateSchema) -> DBModel:
        """Создать новый объект на основе схемы."""
        ...

    @abstractmethod
    async def delete(self, instance: ResponseSchema, **kwargs) -> None:
        """Удалить переданный объект из базы данных."""
        ...
