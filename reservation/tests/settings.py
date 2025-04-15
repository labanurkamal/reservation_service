from functools import cached_property
from typing import Annotated
from urllib.parse import urljoin

from dotenv import find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv('.env_test'),
        env_file_encoding='utf-8',
        extra='ignore'
    )


class TestSettings(ModelConfig):
    url: Annotated[str, Field('localhost', alias="SERVICE_URL")]

    @cached_property
    def endpoint_table(self) -> str:
        return urljoin(self.url, '/api/v1/tables')

    @cached_property
    def endpoint_reservation(self) -> str:
        return urljoin(self.url, '/api/v1/reservations')

    @cached_property
    def endpoint_healthcheck(self) -> str:
        return urljoin(self.url, '/api/v1/healthcheck')


class TestDBSettings(ModelConfig):
    host: Annotated[str, Field('localhost', alias='SQL_HOST')]
    port: Annotated[str, Field('5432', alias='SQL_PORT')]
    db_name: Annotated[str, Field(..., alias='POSTGRES_DB')]
    user: Annotated[str, Field('postgres', alias='POSTGRES_USER')]
    password: Annotated[str, Field(..., alias='POSTGRES_PASSWORD')]
    echo: Annotated[bool, Field(False, alias='ECHO')]

    @cached_property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


test_settings = TestSettings()
test_db_settings = TestDBSettings()
