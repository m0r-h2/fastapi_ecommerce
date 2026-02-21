from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import categories, products, users, reviews
from .log import log_middleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from app.core.config import settings
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix
    )
    yield


app = FastAPI(title=settings.app.title,
              version=settings.app.version,
              port=settings.app.port,
              host=settings.app.host,
              lifespan=lifespan)


app.middleware("http")(log_middleware)


app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API интернет-магазина!"}


@app.get("/debug")
@cache(expire=60)
async def debug():
    print("EXECUTED")
    return {"ok": True}
