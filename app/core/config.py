from pathlib import Path
from typing import Literal
from logging import getLevelNamesMapping
from pydantic import BaseModel, SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)
from sqlalchemy import URL

import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = Path(__file__).resolve().parent
ENVS_DIR = CONFIG_DIR / "envs"
YAML_DIR = CONFIG_DIR / "yaml"


class AppConfig(BaseModel):
    title: str = "FastAPI Internet-Shop"
    version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000


class SQLAlchemyConfig(BaseModel):
    pool_size: int = 20
    max_overflow: int = 5
    echo: bool = True
    expire_on_commit: bool = False


class DatabaseConfig(BaseModel):
    name: str = os.getenv("FAST__APP__DB__NAME")
    host: str = os.getenv("FAST__APP__DB__HOST")
    port: int = os.getenv("FAST__APP__DB__PORT")
    user: str = os.getenv("FAST__APP__DB__USER")
    password: str = os.getenv("FAST__APP__DB__PASSWORD")

    sqla: SQLAlchemyConfig = SQLAlchemyConfig()

    @property
    def async_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            database=self.name,
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password
        )


class RedisDB(BaseModel):
    cache: int = 0

class CacheNamespace(BaseModel):
    user_list: str = "users-list"


class RedisConfig(BaseModel):
    host: str = "redis"
    port: int = 6379
    db: RedisDB = RedisDB()


class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()


class LoggingConfig(BaseModel):
    format: str = "Log: [{extra[log_id]}:{time} - {level} - {message}]"
    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    @property
    def log_lvl(self) ->int:
        return getLevelNamesMapping()[self.level]


class HttpConfig(BaseModel):
    proxy: bool = False


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_prefix="FAST__",
    #     case_sensitive=False,
    #     env_nested_delimiter="__",
    #     env_file=(
    #         ENVS_DIR / ".env.template",
    #         ENVS_DIR / ".env"
    #     ),
    #     yaml_config_section="FAST",
    #     yaml_file=(YAML_DIR / "default.yaml",
    #                YAML_DIR / "local.yaml")
    # )
    app: AppConfig = AppConfig()
    logging: LoggingConfig = LoggingConfig()
    db: DatabaseConfig = DatabaseConfig()
    http: HttpConfig = HttpConfig()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()

    # @classmethod
    # def settings_customise_sources(
    #     cls,
    #     settings_cls: type[BaseSettings],
    #     init_settings: PydanticBaseSettingsSource,
    #     env_settings: PydanticBaseSettingsSource,
    #     dotenv_settings: PydanticBaseSettingsSource,
    #     file_secret_settings: PydanticBaseSettingsSource,
    # ) -> tuple[PydanticBaseSettingsSource, ...]:
    #     return (
    #         init_settings,
    #         env_settings,
    #         dotenv_settings,
    #         YamlConfigSettingsSource(settings_cls),)


settings = Settings()


