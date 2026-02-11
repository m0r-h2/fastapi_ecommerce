from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import categories, products, users, reviews
from .log import log_middleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    print("REDIS INIT")
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="FastAPI Интернет-магазин", version="0.1.0", lifespan=lifespan)


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
