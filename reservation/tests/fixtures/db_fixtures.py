import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from tests.settings import test_db_settings


class TestDatabase:
    def __init__(self, settings):
        self.engine = create_async_engine(
            settings.dsn, echo=settings.echo
        )
        self.SessionLocal = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def clean_tables(self):
        async with self.engine.begin() as conn:
            await conn.execute(text("TRUNCATE TABLE reservations RESTART IDENTITY CASCADE;"))
            await conn.execute(text("TRUNCATE TABLE tables RESTART IDENTITY CASCADE;"))


pytest_db = TestDatabase(settings=test_db_settings)


@pytest_asyncio.fixture(scope='class', autouse=True)
async def clean_table():
    yield
    await pytest_db.clean_tables()
