from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import DBSettings
from models.reservations import Reservation
from models.tables import Table
from services.abstract.repo import ReservationRepository, TableRepository
from services.reservations import ReservationService
from services.tables import TableService
from .register import FactoryRegister


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.v1.tables", "api.v1.reservations"])
    config = providers.Singleton(DBSettings)
    engine = providers.Singleton(
        create_async_engine, url=config.provided.dsn, echo=False,
    )
    async_session_factory = providers.Singleton(
        async_sessionmaker, bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async_session = providers.Singleton(
        lambda factory: factory(), factory=async_session_factory
    )

    base_factory = providers.Factory(
        FactoryRegister,
        session=async_session,
        repository_cls=TableRepository
    )

    reservation_factory = providers.Factory(
        FactoryRegister,
        session=async_session,
        repository_cls=ReservationRepository
    )

    table_service = providers.Factory(
        TableService,
        repository=base_factory.provided.register.call(Table)
    )

    reservation_service = providers.Factory(
        ReservationService,
        repository=reservation_factory.provided.register.call(Reservation)
    )
