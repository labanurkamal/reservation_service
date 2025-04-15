from datetime import datetime
from typing import Type, Any

from sqlalchemy import select, Result, and_, func, exists, cast, literal
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from exceptions.base import EntityNotFoundError, EntityAlreadyExistsError
from .interface import IDBRepository, DBModel, CreateSchema, ResponseSchema


class SqlAlchemyRepository(IDBRepository):
    """
    Репозиторий для работы с базой данных через асинхронный SQLAlchemy `AsyncSession`.
    Реализует основные операции CRUD для заданной модели.
    """

    def __init__(self, session: AsyncSession, model: Type[DBModel]):
        """
        Инициализирует репозиторий с сессией и моделью.

        Аргументы:
            session (AsyncSession): Асинхронная сессия для работы с базой данных.
            model (Type[DBModel]): Модель SQLAlchemy, представляющая таблицу в базе данных.
        """
        self._session = session
        self._model = model

    async def get(self, _id: Any, **kwargs) -> DBModel:
        """Получает экземпляр модели по ID."""
        instance = await self._session.get(self._model, _id, **kwargs)
        if instance is None:
            raise EntityNotFoundError(self._model.__name__, _id)
        return instance

    async def get_all(self, offset: int, limit: int, **kwargs) -> list[DBModel]:
        """Получает все экземпляры модели с пагинацией."""
        smtp = select(self._model).offset(offset).limit(limit)
        result: Result = await self._session.execute(smtp)
        return list(result.unique().scalars().all())

    async def create(self, schema: CreateSchema) -> DBModel:
        """Создает новый экземпляр модели и сохраняет его в базе данных."""
        try:
            instance = self._model(**schema.model_dump())
            self._session.add(instance)
            await self._session.commit()
            await self._session.refresh(instance)
            return instance
        except IntegrityError:
            await self._session.rollback()
            raise EntityAlreadyExistsError(self._model.__name__)

    async def delete(self, instance: ResponseSchema, **kwargs) -> None:
        """Удаляет указанный экземпляр модели из базы данных."""
        await self._session.delete(instance)
        await self._session.commit()


class ReservationRepository(SqlAlchemyRepository):

    async def check_conflicts(self, table_id: int, start_time: datetime, end_time: datetime) -> bool:
        """
        Проверяет наличие конфликтов для заданного времени бронирования.
        """
        reservation_end = self._model.reservation_time + cast(
            func.concat(self._model.duration_minutes, literal(" minutes")), INTERVAL
        )
        stmp = select(exists().where(
            and_(
                self._model.table_id == table_id,
                start_time < reservation_end,
                end_time > self._model.reservation_time
            )
        ))
        return await self._session.scalar(stmp)


class TableRepository(SqlAlchemyRepository):

    async def get_all_with_reservations(self):
        """
        Получает все экземпляры модели стола с соответствующими бронированиями.
        """
        result: Result = await self._session.execute(
            select(self._model).options(joinedload(self._model.reservations))
        )
        return result.unique().scalars().all()
