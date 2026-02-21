from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
#"postgresql+asyncpg://magazine_user:2532@db:5432/magazine_db"
DATABASE_URL = settings.db.async_url

print()
async_engine = create_async_engine(
    DATABASE_URL,
    echo=settings.db.sqla.echo,
    pool_size=settings.db.sqla.pool_size,
    max_overflow=settings.db.sqla.max_overflow
)



async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=settings.db.sqla.expire_on_commit,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass
