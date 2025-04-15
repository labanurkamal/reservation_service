from typing import Type, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from services.abstract.interface import IDBRepository
from services.abstract.repo import DBModel


class FactoryRegister:
    """
    Фабрика для регистрации репозиториев по переданной модели.

    Позволяет создавать экземпляры репозиториев, передавая модель SQLAlchemy.

    :param session: Асинхронная сессия SQLAlchemy.
    :param repository_cls: Класс репозитория, принимающий сессию и модель.
    """

    def __init__(self, session: AsyncSession, repository_cls: Callable[[AsyncSession, Type[DBModel]], IDBRepository]):
        self._session = session
        self._repository_cls = repository_cls

    def register(self, model: Type[DBModel]) -> IDBRepository:
        """
        Создаёт и возвращает экземпляр репозитория для указанной модели.

        :param model: Модель SQLAlchemy, для которой требуется репозиторий.
        :return: Экземпляр репозитория.
        """
        return self._repository_cls(self._session, model)
