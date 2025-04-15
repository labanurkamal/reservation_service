from functools import cached_property
from typing import Annotated

from dotenv import find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv('.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )


class Settings(ModelConfig):
    project_name: Annotated[str, Field('', alias='PROJECT_NAME')]
    version: Annotated[str, Field('', alias='VERSION')]
    debug: Annotated[bool, Field(False, alias='DEBUG')]


class DBSettings(ModelConfig):
    host: Annotated[str, Field('localhost', alias='SQL_HOST')]
    port: Annotated[str, Field('5432', alias='SQL_PORT')]
    db_name: Annotated[str, Field(..., alias='POSTGRES_DB')]
    user: Annotated[str, Field('postgres', alias='POSTGRES_USER')]
    password: Annotated[str, Field(..., alias='POSTGRES_PASSWORD')]
    echo: Annotated[bool, Field(False, alias='ECHO')]

    @cached_property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


settings = Settings()
db_settings = DBSettings()
