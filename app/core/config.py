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

class AppConfig(BaseModel):
    title: str = os.getenv("FAST__APP__TITLE")
    version: str = os.getenv("FAST__APP__VERSION")
    host: str = os.getenv("FAST__APP__HOST")
    port: int = os.getenv("FAST__APP__PORT")


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
    category_list: str = "category-list"
    products_list: str = "products-list"



class RedisConfig(BaseModel):
    host: str = os.getenv("FAST__APP__REDIS__HOST")
    port: int = os.getenv("FAST__APP__REDIS__PORT")
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
    app: AppConfig = AppConfig()
    logging: LoggingConfig = LoggingConfig()
    db: DatabaseConfig = DatabaseConfig()
    http: HttpConfig = HttpConfig()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()


settings = Settings()


